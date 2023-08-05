import ast
import logging
from typing import List, Set

from grimp.application.ports.importscanner import AbstractImportScanner
from grimp.domain.valueobjects import DirectImport, Module
from grimp import exceptions

logger = logging.getLogger(__name__)


class NotAnImport(Exception):
    pass


class ImportScanner(AbstractImportScanner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # We gain a big performance increase by building the set of root modules once,
        # instead of letting each node parser figure them out from the internal modules.
        self._root_modules = {module.root for module in self.modules}

    def scan_for_imports(self, module: Module) -> Set[DirectImport]:
        """
        Note: this method only analyses the module in question and will not load any other
        code, so it relies on self.modules to deduce which modules it imports. (This is
        because you can't know whether "from foo.bar import baz" is importing a module
        called  `baz`, or a function `baz` from the module `bar`.)
        """
        direct_imports: Set[DirectImport] = set()

        module_filename = self._determine_module_filename(module)
        is_package = self._module_is_package(module_filename)
        module_contents = self._read_module_contents(module_filename)
        module_lines = module_contents.splitlines()
        try:
            ast_tree = ast.parse(module_contents)
        except SyntaxError as e:
            raise exceptions.SourceSyntaxError(
                filename=module_filename,
                lineno=e.lineno,
                text=e.text,
            )
        for node in ast.walk(ast_tree):
            direct_imports |= self._parse_direct_imports_from_node(
                node, module, module_lines, is_package
            )

        return direct_imports

    def _parse_direct_imports_from_node(
        self, node: ast.AST, module: Module, module_lines: List[str], is_package: bool
    ) -> Set[DirectImport]:
        """
        Parse an ast node into a set of DirectImports.
        """
        try:
            parser = _get_node_parser(
                node=node,
                module=module,
                internal_modules=self.modules,
                root_modules=self._root_modules,
                is_package=is_package,
            )
        except NotAnImport:
            return set()

        direct_imports: Set[DirectImport] = set()

        for imported in parser.determine_imported_modules(
            include_external_packages=self.include_external_packages
        ):
            direct_imports.add(
                DirectImport(
                    importer=module,
                    imported=imported,
                    line_number=node.lineno,
                    line_contents=module_lines[node.lineno - 1].strip(),
                )
            )

        return direct_imports

    def _determine_module_filename(self, module: Module) -> str:
        """
        Work out the full filename of the given module.

        Any given module can either be a straight Python file (foo.py) or else a package
        (in which case the file is an __init__.py within a directory).
        """
        module_components = module.name.split(".")
        package_directory = self._lookup_module_package_directory(module)
        package_directory_parts = self.file_system.split(package_directory)
        assert (
            module_components[0] == package_directory_parts[-1]
        ), "The package directory should be the same as the first part of the module name."

        filename_root = self.file_system.join(package_directory, *module_components[1:])
        candidate_filenames = (
            f"{filename_root}.py",
            self.file_system.join(filename_root, "__init__.py"),
        )
        for candidate_filename in candidate_filenames:
            if self.file_system.exists(candidate_filename):
                return candidate_filename
        raise FileNotFoundError(f"Could not find module {module}.")

    def _lookup_module_package_directory(self, module: Module) -> str:
        for package_directory, modules in self.modules_by_package_directory.items():
            if module in modules:
                return package_directory
        raise KeyError(f"{module} was not present in the scanner.")

    def _read_module_contents(self, module_filename: str) -> str:
        """
        Read the file contents of the module.
        """
        return self.file_system.read(module_filename)

    def _module_is_package(self, module_filename: str) -> bool:
        """
        Whether or not the supplied module filename is a package.
        """
        return self.file_system.split(module_filename)[-1] == "__init__.py"


class _BaseNodeParser:
    """
    Works out from an AST node what the imported modules are.
    """

    def __init__(
        self,
        node: ast.AST,
        module: Module,
        internal_modules: Set[Module],
        root_modules: Set[Module],
        is_package: bool,
    ) -> None:
        self.node = node
        self.module = module
        self.internal_modules = internal_modules
        self.root_modules = root_modules
        self.module_is_package = is_package

    def determine_imported_modules(
        self, include_external_packages: bool
    ) -> Set[Module]:
        """
        Return the imported modules in the statement.
        """
        raise NotImplementedError

    def _is_internal_module(self, module: Module) -> bool:
        return module.root in self.root_modules


class _ImportNodeParser(_BaseNodeParser):
    """
    Parser for statements in the form 'import x'.
    """

    node_class = ast.Import

    def determine_imported_modules(
        self, include_external_packages: bool
    ) -> Set[Module]:
        imported_modules: Set[Module] = set()

        assert isinstance(self.node, self.node_class)  # For type checker.
        for alias in self.node.names:
            module_from_alias = Module(alias.name)

            if self._is_internal_module(module_from_alias):
                imported_module = module_from_alias
            else:
                if include_external_packages:
                    imported_module = Module(module_from_alias.package_name)
                else:
                    continue

            imported_modules.add(imported_module)

        return imported_modules


class _ImportFromNodeParser(_BaseNodeParser):
    """
    Parser for statements in the form 'from x import ...'.
    """

    node_class = ast.ImportFrom

    def determine_imported_modules(
        self, include_external_packages: bool
    ) -> Set[Module]:
        imported_modules: Set[Module] = set()
        assert isinstance(self.node, self.node_class)  # For type checker.
        assert isinstance(self.node.level, int)  # For type checker.

        if self.node.level == 0:
            # Absolute import.
            # Let the type checker know we expect node.module to be set here.
            assert isinstance(self.node.module, str)
            node_module = Module(self.node.module)
            if not self._is_internal_module(node_module):
                if include_external_packages:
                    # Just return the top level package of the external module.
                    return {Module(node_module.package_name)}
                else:
                    return set()
            # Don't include imports of modules outside this package.

            module_base = self.node.module
        elif self.node.level >= 1:
            # Relative import. The level corresponds to how high up the tree it goes;
            # for example 'from ... import foo' would be level 3.
            importing_module_components = self.module.name.split(".")
            # TODO: handle level that is too high.
            # Trim the base module by the number of levels.
            if self.module_is_package:
                # If the scanned module an __init__.py file, we don't want
                # to go up an extra level.
                number_of_levels_to_trim_by = self.node.level - 1
            else:
                number_of_levels_to_trim_by = self.node.level

            if number_of_levels_to_trim_by:
                module_base = ".".join(
                    importing_module_components[:-number_of_levels_to_trim_by]
                )
            else:
                module_base = ".".join(importing_module_components)
            if self.node.module:
                module_base = ".".join([module_base, self.node.module])

        # node.names corresponds to 'a', 'b' and 'c' in 'from x import a, b, c'.
        for alias in self.node.names:
            full_module_name = ".".join([module_base, alias.name])
            try:
                imported_module = self._trim_to_internal_module(
                    untrimmed_module=Module(full_module_name)
                )
            except FileNotFoundError:
                logger.warning(
                    f"Could not find {full_module_name} when scanning {self.module}. "
                    "This may be due to a missing __init__.py file in the parent package."
                )
            else:
                imported_modules.add(imported_module)
        return imported_modules

    def _trim_to_internal_module(self, untrimmed_module: Module) -> Module:
        """
        Raises FileNotFoundError if it could not find a valid module.
        """
        if untrimmed_module in self.internal_modules:
            return untrimmed_module
        else:
            # The module isn't in the internal modules. This is because it's something *within*
            # a module (e.g. a function): the result of something like 'from .subpackage
            # import my_function'. So we trim the components back to the module.
            components = untrimmed_module.name.split(".")[:-1]
            trimmed_module = Module(".".join(components))

            if trimmed_module in self.internal_modules:
                return trimmed_module
            else:
                raise FileNotFoundError()


def _get_node_parser(
    node: ast.AST,
    module: Module,
    internal_modules: Set[Module],
    root_modules: Set[Module],
    is_package: bool,
) -> _BaseNodeParser:
    """
    Return a NodeParser instance for the supplied node.

    Raises NotAnImport if the supplied node is not an import statement.
    """
    parser_class_map = {
        ast.ImportFrom: _ImportFromNodeParser,
        ast.Import: _ImportNodeParser,
    }
    for node_class, parser_class in parser_class_map.items():
        if isinstance(node, node_class):
            return parser_class(
                node=node,
                module=module,
                internal_modules=internal_modules,
                root_modules=root_modules,
                is_package=is_package,
            )
    raise NotAnImport
