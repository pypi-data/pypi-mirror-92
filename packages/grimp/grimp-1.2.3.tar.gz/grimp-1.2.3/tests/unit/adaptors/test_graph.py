import re

import pytest  # type: ignore
from grimp.adaptors.graph import ImportGraph
from grimp.exceptions import ModuleNotPresent


class TestRepr:
    """
    Because sets are unordered, it's difficult to test the repr in a deterministic way,
    so we use regular expressions instead.
    """

    def test_no_modules(self):
        assert "<ImportGraph: empty>" == repr(ImportGraph())

    def test_untruncated(self):
        modules = ["one", "two", "three", "four", "five"]
        graph = ImportGraph()
        for module in modules:
            graph.add_module(module)

        # Assert something in the form <ImportGraph: 'one', 'two', 'three', 'four', 'five'>
        # (but not necessarily in that order).
        re_part = "(" + "|".join(modules) + ")"
        assert re.match(
            f"<ImportGraph: '{re_part}', '{re_part}', '{re_part}', '{re_part}', '{re_part}'>",
            repr(graph),
        )

    def test_truncated(self):
        modules = ["one", "two", "three", "four", "five", "six"]
        graph = ImportGraph()
        for module in modules:
            graph.add_module(module)

        re_part = "(" + "|".join(modules) + ")"
        assert re.match(
            f"<ImportGraph: '{re_part}', '{re_part}', '{re_part}', "
            f"'{re_part}', '{re_part}', ...>",
            repr(graph),
        )


def test_modules_when_empty():
    graph = ImportGraph()
    assert graph.modules == set()


def test_find_modules_directly_imported_by():
    graph = ImportGraph()
    a, b, c = "foo", "bar", "baz"
    d, e, f = "foo.one", "bar.one", "baz.one"

    graph.add_import(importer=a, imported=b)
    graph.add_import(importer=a, imported=c)
    graph.add_import(importer=a, imported=d)
    graph.add_import(importer=b, imported=e)
    graph.add_import(importer=f, imported=a)

    assert {b, c, d} == graph.find_modules_directly_imported_by("foo")


def test_find_modules_that_directly_import():
    graph = ImportGraph()
    a, b, c = "foo", "bar", "baz"
    d, e, f = "foo.one", "bar.one", "baz.one"

    graph.add_import(importer=a, imported=b)
    graph.add_import(importer=a, imported=c)
    graph.add_import(importer=a, imported=d)
    graph.add_import(importer=b, imported=e)
    graph.add_import(importer=f, imported=b)

    assert {a, f} == graph.find_modules_that_directly_import("bar")


@pytest.mark.parametrize(
    "importer, imported, as_packages, expected_result",
    (
        # as_packages=False:
        ("a.one.green", "a.two.green", False, True),  # Direct import.
        ("a.two.green", "a.three.blue", False, True),  # Direct import.
        ("a.one.green", "a.three.blue", False, False),  # Indirect import.
        ("a.two.green", "a.one.green", False, False),  # Reverse direct import.
        ("a.one", "a.two", False, False),  # Direct import - parents.
        ("a.two", "a.two.green", False, True),  # Direct import - parent to child.
        # as_packages=True:
        ("a.one.green", "a.two.green", True, True),  # Direct import.
        ("a.one.green", "a.three.blue", True, False),  # Indirect import.
        ("a.one", "a.two", True, True),  # Direct import - parents.
        ("a.one", "a.three", True, False),  # Indirect import - parents.
        # Direct import - importer child, imported actual.
        ("a.four.green", "a.two.green", True, True),
        # Direct import - importer actual, imported child.
        ("a.five", "a.four", True, True),
        # Direct import - importer grandchild, imported child.
        ("a.four", "a.two", True, True),
        # Exceptions - doesn't make sense to ask about direct imports within package
        # when as_packages=True.
        ("a.two", "a.two.green", True, ValueError()),
        ("a.two.green", "a.two", True, ValueError()),
    ),
)
def test_direct_import_exists(importer, imported, as_packages, expected_result):
    """
    Build a graph to analyse for chains. This is much easier to debug visually,
    so here is the dot syntax for the graph, which can be viewed using a dot file viewer.

        digraph {
            a;
            a_one;
            a_one_green;
            a_one_blue;
            a_two;
            a_two_green;
            a_two_blue;
            a_three;
            a_three_green;
            a_three_blue;
            a_four;
            a_four_green;
            a_four_green_alpha;
            a_five;

            a_one_green -> a_two_green;
            a_two -> a_two_green;
            a_two_green -> a_three_blue;
            a_five -> a_four_green_alpha;
            a_four_green_alpha -> a_two_green;
        }
    """
    graph = ImportGraph()
    all_modules = (
        a,
        a_one,
        a_one_green,
        a_one_blue,
        a_two,
        a_two_green,
        a_two_blue,
        a_three,
        a_three_green,
        a_three_blue,
        a_four,
        a_four_green,
        a_four_green_alpha,
        a_five,
    ) = (
        "a",
        "a.one",
        "a.one.green",
        "a.one.blue",
        "a.two",
        "a.two.green",
        "a.two.blue",
        "a.three",
        "a.three.green",
        "a.three.blue",
        "a.four",
        "a.four.green",
        "a.four.green.alpha",
        "a.five",
    )

    for module_to_add in all_modules:
        graph.add_module(module_to_add)

    for _importer, _imported in (
        (a_one_green, a_two_green),
        (a_two, a_two_green),
        (a_two_green, a_three_blue),
        (a_five, a_four_green_alpha),
        (a_four_green_alpha, a_two_green),
    ):
        graph.add_import(importer=_importer, imported=_imported)

    if isinstance(expected_result, Exception):
        with pytest.raises(expected_result.__class__):
            graph.direct_import_exists(
                importer=importer, imported=imported, as_packages=as_packages
            )
    else:
        assert expected_result == graph.direct_import_exists(
            importer=importer, imported=imported, as_packages=as_packages
        )


@pytest.mark.parametrize(
    "imports, expected_count",
    (
        ((), 0),
        ((("foo.one", "foo.two"),), 1),
        ((("foo.one", "foo.two"), ("foo.three", "foo.two")), 2),
        (
            (
                ("foo.one", "foo.two"),
                ("foo.three", "foo.two"),
                ("foo.three", "foo.two"),  # Duplicate should not increase the number.
            ),
            2,
        ),
    ),
)
def test_count_imports(imports, expected_count):
    graph = ImportGraph()

    for importer, imported in imports:
        graph.add_import(importer=importer, imported=imported)

    assert expected_count == graph.count_imports()


@pytest.mark.parametrize(
    "module, as_package, expected_result",
    (
        ("foo.a", False, {"foo.b", "foo.c", "foo.a.d", "foo.b.e"}),
        ("foo.b.e", False, set()),
        ("foo.a", True, {"foo.b", "foo.c", "foo.b.e", "foo.b.g"}),
        ("foo.b.e", True, set()),
        ("bar", True, {"foo.a.d", "foo.b.e"}),
        ("bar", False, {"foo.a.d", "foo.b.e"}),
    ),
)
def test_find_downstream_modules(module, as_package, expected_result):
    graph = ImportGraph()
    a, b, c = "foo.a", "foo.b", "foo.c"
    d, e, f = "foo.a.d", "foo.b.e", "foo.a.f"
    g = "foo.b.g"
    external = "bar"

    graph.add_module(external, is_squashed=True)

    graph.add_import(imported=a, importer=b)
    graph.add_import(imported=a, importer=c)
    graph.add_import(imported=c, importer=d)
    graph.add_import(imported=d, importer=e)
    graph.add_import(imported=f, importer=b)
    graph.add_import(imported=f, importer=g)
    graph.add_import(imported=external, importer=d)

    assert expected_result == graph.find_downstream_modules(
        module, as_package=as_package
    )


@pytest.mark.parametrize(
    "module, as_package, expected_result",
    (
        ("foo.d", False, {"foo.d.c", "foo.a"}),
        ("foo.b.g", False, set()),
        ("foo.d", True, {"foo.a", "foo.a.f", "foo.b.g"}),
        ("foo.b.g", True, set()),
        ("bar", True, {"foo.a.f", "foo.b.g"}),
        ("bar", False, {"foo.a.f", "foo.b.g"}),
    ),
)
def test_find_upstream_modules(module, as_package, expected_result):
    graph = ImportGraph()
    a, b, c = "foo.a", "foo.d.b", "foo.d.c"
    d, e, f = "foo.d", "foo.c.e", "foo.a.f"
    g = "foo.b.g"
    external = "bar"

    graph.add_module(external, is_squashed=True)

    graph.add_import(imported=a, importer=b)
    graph.add_import(imported=a, importer=c)
    graph.add_import(imported=c, importer=d)
    graph.add_import(imported=d, importer=e)
    graph.add_import(imported=f, importer=b)
    graph.add_import(imported=g, importer=f)
    graph.add_import(imported=f, importer=external)

    assert expected_result == graph.find_upstream_modules(module, as_package=as_package)


@pytest.mark.parametrize(
    "module, expected_result",
    (("foo", {"foo.a", "foo.b", "foo.c"}), ("foo.a", {"foo.a.one"}), ("foo.c", set())),
)
def test_find_children(module, expected_result):
    graph = ImportGraph()
    foo, bar = "foo", "bar"
    a, b, c = "foo.a", "foo.b", "foo.c"
    d, e, f = "foo.a.one", "foo.b.one", "bar.g"
    for module_to_add in (foo, bar, a, b, c, d, e, f):
        graph.add_module(module_to_add)

    assert expected_result == graph.find_children(module)


def test_find_children_raises_exception_for_squashed_module():
    graph = ImportGraph()
    module = "foo"

    graph.add_module(module, is_squashed=True)

    with pytest.raises(ValueError, match="Cannot find children of a squashed module."):
        graph.find_children(module)


@pytest.mark.parametrize(
    "module, expected_result",
    (
        ("foo", {"foo.a", "foo.b", "foo.c", "foo.a.one", "foo.b.one"}),
        ("foo.a", {"foo.a.one"}),
        ("foo.c", set()),
    ),
)
def test_find_descendants(module, expected_result):
    graph = ImportGraph()
    foo, bar = "foo", "bar"
    a, b, c = "foo.a", "foo.b", "foo.c"
    d, e, f = "foo.a.one", "foo.b.one", "bar.g"

    for module_to_add in (foo, bar, a, b, c, d, e, f):
        graph.add_module(module_to_add)

    assert expected_result == graph.find_descendants(module)


def test_find_descendants_raises_exception_for_squashed_module():
    graph = ImportGraph()
    module = "foo"

    graph.add_module(module, is_squashed=True)

    with pytest.raises(
        ValueError, match="Cannot find descendants of a squashed module."
    ):
        graph.find_descendants(module)


def test_find_shortest_chain_when_exists():
    graph = ImportGraph()
    a, b, c = "foo", "bar", "baz"
    d, e, f = "long", "way", "around"

    # Add short path.
    graph.add_import(importer=a, imported=b)
    graph.add_import(importer=b, imported=c)

    # Add longer path.
    graph.add_import(importer=a, imported=d)
    graph.add_import(importer=d, imported=e)
    graph.add_import(importer=e, imported=f)
    graph.add_import(importer=f, imported=c)

    assert (a, b, c) == graph.find_shortest_chain(importer=a, imported=c)


def test_find_shortest_chain_returns_none_if_not_exists():
    graph = ImportGraph()
    a, b, c = "foo", "bar", "baz"

    graph.add_import(importer=a, imported=b)
    graph.add_import(importer=b, imported=c)

    assert None is graph.find_shortest_chain(importer=c, imported=a)


class TestFindShortestChains:
    def test_top_level_import(self):
        graph = ImportGraph()
        graph.add_import(importer="green", imported="blue")

        result = graph.find_shortest_chains(importer="green", imported="blue")

        assert result == {("green", "blue")}

    def test_first_level_child_import(self):
        graph = ImportGraph()
        graph.add_module("green")
        graph.add_module("blue")
        graph.add_import(importer="green.foo", imported="blue.bar")

        result = graph.find_shortest_chains(importer="green", imported="blue")

        assert result == {("green.foo", "blue.bar")}

    def test_no_results_in_reverse_direction(self):
        graph = ImportGraph()
        graph.add_module("green")
        graph.add_module("blue")
        graph.add_import(importer="green.foo", imported="blue.bar")

        result = graph.find_shortest_chains(importer="blue", imported="green")

        assert result == set()

    def test_grandchildren_import(self):
        graph = ImportGraph()
        graph.add_module("green")
        graph.add_module("blue")
        graph.add_import(importer="green.foo.one", imported="blue.bar.two")

        result = graph.find_shortest_chains(importer="green", imported="blue")

        assert result == {("green.foo.one", "blue.bar.two")}

    def test_import_between_child_and_top_level(self):
        graph = ImportGraph()
        graph.add_module("green")
        graph.add_import(importer="green.foo", imported="blue")

        result = graph.find_shortest_chains(importer="green", imported="blue")

        assert result == {("green.foo", "blue")}

    def test_import_between_top_level_and_child(self):
        graph = ImportGraph()
        graph.add_module("blue")
        graph.add_import(importer="green", imported="blue.foo")

        result = graph.find_shortest_chains(importer="green", imported="blue")

        assert result == {("green", "blue.foo")}

    def test_short_indirect_import(self):
        graph = ImportGraph()
        graph.add_module("green")
        graph.add_module("blue")
        graph.add_import(importer="green.indirect", imported="purple")
        graph.add_import(importer="purple", imported="blue.foo")

        result = graph.find_shortest_chains(importer="green", imported="blue")

        assert result == {("green.indirect", "purple", "blue.foo")}

    def test_long_indirect_import(self):
        graph = ImportGraph()
        graph.add_module("green")
        graph.add_module("blue")
        graph.add_import(importer="green.baz", imported="yellow.three")
        graph.add_import(importer="yellow.three", imported="yellow.two")
        graph.add_import(importer="yellow.two", imported="yellow.one")
        graph.add_import(importer="yellow.one", imported="blue.foo")

        result = graph.find_shortest_chains(importer="green", imported="blue")

        assert result == {
            ("green.baz", "yellow.three", "yellow.two", "yellow.one", "blue.foo")
        }

    def test_chains_via_importer_package_dont_stop_longer_chains_being_included(self):
        graph = ImportGraph()

        graph.add_module("green")
        graph.add_module("blue")

        # Chain via importer package.
        graph.add_import(importer="green.foo", imported="blue.foo")
        graph.add_import(importer="green.baz", imported="green.foo")

        # Long indirect import.
        graph.add_import(importer="green.baz", imported="yellow.three")
        graph.add_import(importer="yellow.three", imported="yellow.two")
        graph.add_import(importer="yellow.two", imported="yellow.one")
        graph.add_import(importer="yellow.one", imported="blue.bar")

        result = graph.find_shortest_chains(importer="green", imported="blue")
        assert result == {
            ("green.foo", "blue.foo"),
            ("green.baz", "yellow.three", "yellow.two", "yellow.one", "blue.bar"),
        }

    def test_chains_that_reenter_importer_package_dont_stop_longer_chains_being_included(
        self,
    ):
        graph = ImportGraph()

        graph.add_module("green")
        graph.add_module("blue")

        # Chain that reenters importer package.
        graph.add_import(importer="green.baz", imported="brown")
        graph.add_import(importer="brown", imported="green.foo")
        graph.add_import(importer="green.foo", imported="blue.foo")

        # Long indirect import.
        graph.add_import(importer="green.baz", imported="yellow.three")
        graph.add_import(importer="yellow.three", imported="yellow.two")
        graph.add_import(importer="yellow.two", imported="yellow.one")
        graph.add_import(importer="yellow.one", imported="blue.foo")

        result = graph.find_shortest_chains(importer="green", imported="blue")
        assert result == {
            ("green.foo", "blue.foo"),
            ("green.baz", "yellow.three", "yellow.two", "yellow.one", "blue.foo"),
        }

    def test_chains_that_reenter_imported_package_dont_stop_longer_chains_being_included(
        self,
    ):
        graph = ImportGraph()

        graph.add_module("green")
        graph.add_module("blue")

        # Chain that reenters imported package.
        graph.add_import(importer="green.foo", imported="blue.foo")
        graph.add_import(importer="blue.foo", imported="brown")
        graph.add_import(importer="brown", imported="blue.bar")

        # Long indirect import.
        graph.add_import(importer="green.foo", imported="yellow.four")
        graph.add_import(importer="yellow.four", imported="yellow.three")
        graph.add_import(importer="yellow.three", imported="yellow.two")
        graph.add_import(importer="yellow.two", imported="yellow.one")
        graph.add_import(importer="yellow.one", imported="blue.bar")

        result = graph.find_shortest_chains(importer="green", imported="blue")
        assert result == {
            ("green.foo", "blue.foo"),
            (
                "green.foo",
                "yellow.four",
                "yellow.three",
                "yellow.two",
                "yellow.one",
                "blue.bar",
            ),
        }


@pytest.mark.parametrize(
    "importer, imported, as_packages, expected_result",
    (
        # This block: as_packages not supplied.
        ("a.two", "a.one", None, True),  # Importer directly imports imported.
        ("a.three", "a.one", None, True),  # Importer indirectly imports imported.
        # Importer does not import the imported, even indirectly.
        ("a.two.green", "a.one", None, False),
        ("b.two", "c.one", None, False),  # Importer imports the child of the imported.
        (
            "b.two",
            "b",
            None,
            False,
        ),  # Importer is child of imported (but doesn't import).
        # Importer's child imports imported's child.
        ("b.two", "a.one", None, False),
        # Importer's grandchild directly imports imported's grandchild.
        ("b", "a", None, False),
        # Importer's grandchild indirectly imports imported's grandchild.
        ("d", "a", None, False),
        # 'Weak dependency': importer's child imports module that does not import imported
        # (even directly). However another module in the intermediate subpackage *does*
        # import the upstream module.
        # The chains are: e.one -> b.one; b.two -> c.one.green; c.one -> a.two.
        ("e", "a", None, False),
        # This block: as_packages=False (should be identical to block above).
        ("a.two", "a.one", False, True),
        ("a.three", "a.one", False, True),
        ("a.two.green", "a.one", False, False),
        ("b.two", "c.one", False, False),
        ("b.two", "b", False, False),
        ("b.two", "a.one", False, False),
        ("b", "a", False, False),
        ("d", "a", False, False),
        ("e", "a", False, False),
        # This block: as_packages=True.
        ("a.two", "a.one", True, True),  # Importer directly imports imported.
        ("a.three", "a.one", True, True),  # Importer indirectly imports imported.
        # Importer does not import the imported, even indirectly.
        ("a.two.green", "a.one", True, False),
        # Importer imports the child of the imported (b.two -> c.one.green).
        ("b.two", "c.one", True, True),
        # Importer is child of imported (but doesn't import). This doesn't
        # make sense if as_packages is True, so it should raise an exception.
        ("b.two", "b", True, ValueError()),
        # Importer's child imports imported's child (b.two.green -> a.one.green).
        ("b.two", "a.one", True, True),
        # Importer's grandchild directly imports imported's grandchild
        # (b.two.green -> a.one.green).
        ("b", "a", True, True),
        # Importer's grandchild indirectly imports imported's grandchild.
        # (d.one.green -> b.two.green -> a.one.green).
        ("d", "a", True, True),
        # 'Weak dependency': importer's child imports module that does not import imported
        # (even directly). However another module in the intermediate subpackage *does*
        # import the upstream module. We treat this as False as it's not really a dependency.
        # The chains are: e.one -> b.one; b.two -> c.one.green; c.one -> a.two.
        ("e", "a", True, False),
        # Squashed modules.
        ("a.three", "squashed", False, True),  # Direct import of squashed module.
        ("a.three", "squashed", True, True),
        ("squashed", "a.two", False, True),  # Direct import by squashed module.
        ("squashed", "a.two", True, True),
        ("squashed", "a.one", False, True),  # Indirect import by squashed module.
        ("squashed", "a.one", True, True),
        ("a", "squashed", False, False),  # Package involving squashed module.
        ("a", "squashed", True, True),  # Package involving squashed module.
    ),
)
def test_chain_exists(importer, imported, as_packages, expected_result):
    """
    Build a graph to analyse for chains. This is much easier to debug visually,
    so here is the dot syntax for the graph, which can be viewed using a dot file viewer.

        digraph {
            a;
            a_one;
            a_one_green;
            a_two -> a_one;
            a_two_green;
            a_three -> c_one;
            b;
            b_one;
            b_two -> c_one_green;
            b_two_green -> b_one;
            b_two_green -> a_one_green;
            c;
            c_one -> a_two;
            c_one_green;
            d;
            d_one;
            d_one_green -> b_two_green;
            e;
            e_one -> b_one;
            squashed -> a_two;
            a_three -> squashed;

    """
    graph = ImportGraph()
    a, a_one, a_one_green, a_two, a_two_green, a_three = (
        "a",
        "a.one",
        "a.one.green",
        "a.two",
        "a.two.green",
        "a.three",
    )
    b, b_one, b_two, b_two_green = ("b", "b.one", "b.two", "b.two.green")
    c, c_one, c_one_green = "c", "c.one", "c.one.green"
    d, d_one, d_one_green = "d", "d.one", "d.one.green"
    e, e_one = "e", "e.one"
    squashed = "squashed"

    for module_to_add in (
        a,
        a_one,
        a_one_green,
        a_two,
        a_two_green,
        a_three,
        b,
        b_one,
        b_two,
        b_two_green,
        c,
        c_one,
        c_one_green,
        d,
        d_one,
        d_one_green,
        e,
        e_one,
    ):
        graph.add_module(module_to_add)
    graph.add_module(squashed, is_squashed=True)

    for _importer, _imported in (
        (a_two, a_one),
        (c_one, a_two),
        (a_three, c_one),
        (b_two, c_one_green),
        (b_two_green, b_one),
        (b_two_green, a_one_green),
        (d_one_green, b_two_green),
        (e_one, b_one),
        (squashed, a_two),
        (a_three, squashed),
    ):
        graph.add_import(importer=_importer, imported=_imported)

    kwargs = dict(imported=imported, importer=importer)
    if as_packages is not None:
        kwargs["as_packages"] = as_packages

    if isinstance(expected_result, Exception):
        with pytest.raises(expected_result.__class__):
            graph.chain_exists(**kwargs)
    else:
        assert expected_result == graph.chain_exists(**kwargs)


def test_add_module():
    graph = ImportGraph()
    module = "foo"

    graph.add_module(module)

    assert graph.modules == {module}


def test_remove_module():
    graph = ImportGraph()
    a, b = {"mypackage.blue", "mypackage.green"}

    graph.add_module(a)
    graph.add_module(b)
    graph.add_import(importer=a, imported=b)

    graph.remove_module(b)
    assert {a} == graph.modules

    # Removing a non-existent module doesn't cause an error.
    graph.remove_module("mypackage.yellow")


class TestAddSquashedModule:
    def test_can_repeatedly_add_same_squashed_module(self):
        graph = ImportGraph()
        module = "foo"

        graph.add_module(module, is_squashed=True)
        graph.add_module(module, is_squashed=True)

        assert graph.modules == {module}

    def test_cannot_add_squashed_module_if_already_same_unsquashed_module(self):
        graph = ImportGraph()
        module = "foo"

        graph.add_module(module)

        with pytest.raises(
            ValueError,
            match=(
                "Cannot add a squashed module when it is already present in the graph as an "
                "unsquashed module, or vice versa."
            ),
        ):
            graph.add_module(module, is_squashed=True)

    def test_cannot_add_unsquashed_module_if_already_same_squashed_module(self):
        graph = ImportGraph()
        module = "foo"

        graph.add_module(module, is_squashed=True)

        with pytest.raises(
            ValueError,
            match=(
                "Cannot add a squashed module when it is already present in the graph as an "
                "unsquashed module, or vice versa."
            ),
        ):
            graph.add_module(module)

    @pytest.mark.parametrize(
        "module_name", ("mypackage.foo.one", "mypackage.foo.one.alpha")
    )
    def test_cannot_add_descendant_of_squashed_module(self, module_name):
        graph = ImportGraph()

        graph.add_module("mypackage.foo", is_squashed=True)

        with pytest.raises(
            ValueError, match="Module is a descendant of squashed module mypackage.foo."
        ):
            graph.add_module(module_name)


@pytest.mark.parametrize("add_module", (True, False))
def test_add_import(add_module):
    graph = ImportGraph()
    a, b = "foo", "bar"

    # Adding the module should make no difference to the result.
    if add_module:
        graph.add_module(a)

    graph.add_import(importer=a, imported=b)

    assert {a, b} == graph.modules
    assert {b} == graph.find_modules_directly_imported_by(a)
    assert set() == graph.find_modules_directly_imported_by(b)


def test_remove_import():
    graph = ImportGraph()
    a, b, c = "foo", "bar", "baz"
    graph.add_import(importer=a, imported=b)
    graph.add_import(importer=a, imported=c)

    graph.remove_import(importer=a, imported=b)

    assert {a, b, c} == graph.modules
    assert {c} == graph.find_modules_directly_imported_by(a)


class TestGetImportDetails:
    def test_happy_path(self):
        graph = ImportGraph()

        imports_info = [
            dict(
                importer="mypackage.foo",
                imported="mypackage.bar",
                line_number=1,
                line_contents="from . import bar",
            ),
            dict(
                importer="mypackage.foo",
                imported="mypackage.bar",
                line_number=10,
                line_contents="from .bar import a_function",
            ),
        ]
        for import_info in imports_info:
            graph.add_import(**import_info)

        assert imports_info == graph.get_import_details(
            importer="mypackage.foo", imported="mypackage.bar"
        )

    def test_returns_empty_list_when_no_import(self):
        graph = ImportGraph()

        assert [] == graph.get_import_details(importer="foo", imported="bar")

    def test_returns_empty_list_when_import_but_no_available_details(self):
        graph = ImportGraph()

        importer, imported = "foo", "bar"
        graph.add_import(importer=importer, imported=imported),

        assert [] == graph.get_import_details(importer=importer, imported=imported)

    def test_returns_only_relevant_imports(self):
        graph = ImportGraph()

        imports_info = [
            dict(
                importer="mypackage.foo",
                imported="mypackage.bar",
                line_number=1,
                line_contents="from . import bar",
            )
        ]
        graph.add_import(**imports_info[0])

        # Also add a different import in the same module.
        graph.add_import(
            importer="mypackage.foo",
            imported="mypackage.baz",
            line_number=2,
            line_contents="from . import baz",
        )

        assert imports_info == graph.get_import_details(
            importer="mypackage.foo", imported="mypackage.bar"
        )


class TestIsModuleSquashed:
    def test_returns_true_for_module_added_with_is_squashed(self):
        graph = ImportGraph()
        graph.add_module("foo", is_squashed=True)

        assert graph.is_module_squashed("foo")

    def test_returns_false_for_module_added_without_is_squashed(self):
        graph = ImportGraph()
        graph.add_module("foo", is_squashed=False)

        assert not graph.is_module_squashed("foo")

    def test_raises_module_not_present_for_nonexistent_module(self):
        graph = ImportGraph()

        with pytest.raises(ModuleNotPresent):
            assert not graph.is_module_squashed("foo")


class TestSquashModule:
    def test_marks_module_as_squashed(self):
        graph = ImportGraph()
        modules_to_squash = {
            "foo",
            "foo.green",
        }
        for module in modules_to_squash:
            graph.add_module(module)

        graph.squash_module("foo")

        assert graph.is_module_squashed("foo")

    def test_updates_modules_in_graph(self):
        graph = ImportGraph()
        modules_to_squash = {
            "foo",
            "foo.green",
            "foo.blue",
            "foo.blue.alpha",
        }
        other_modules = {
            "bar",
            "bar.black",
            "baz",
        }
        for module in modules_to_squash | other_modules:
            graph.add_module(module)

        graph.squash_module("foo")

        assert {"foo"} | other_modules == graph.modules

    def test_keeps_import_from_squashed_root(self):
        graph = ImportGraph()
        for module in [
            "foo",
            "foo.green",
            "bar.blue",
        ]:
            graph.add_module(module)
        graph.add_import(importer="foo", imported="bar.blue")

        graph.squash_module("foo")

        assert graph.direct_import_exists(importer="foo", imported="bar.blue")

    def test_keeps_import_of_squashed_root(self):
        graph = ImportGraph()
        for module in [
            "foo",
            "foo.green",
            "bar.blue",
        ]:
            graph.add_module(module)
        graph.add_import(importer="bar.blue", imported="foo")

        graph.squash_module("foo")

        assert graph.direct_import_exists(importer="bar.blue", imported="foo")

    def test_contracts_import_from_descendant(self):
        graph = ImportGraph()
        for module in [
            "foo",
            "foo.green",
            "bar.blue",
        ]:
            graph.add_module(module)
        graph.add_import(importer="foo.green", imported="bar.blue")

        graph.squash_module("foo")

        assert graph.direct_import_exists(importer="foo", imported="bar.blue")

    def test_contracts_import_to_descendant(self):
        graph = ImportGraph()
        for module in [
            "foo",
            "foo.green",
            "bar.blue",
        ]:
            graph.add_module(module)
        graph.add_import(importer="bar.blue", imported="foo.green")

        graph.squash_module("foo")

        assert graph.direct_import_exists(importer="bar.blue", imported="foo")

    def test_doesnt_error_if_imports_within_module(self):
        graph = ImportGraph()
        for module in [
            "foo",
            "foo.green",
            "foo.blue",
        ]:
            graph.add_module(module)
        graph.add_import(importer="foo.blue", imported="foo.green")

        graph.squash_module("foo")

    def test_import_details_from_squashed_root_are_preserved(self):
        graph = ImportGraph()
        for module in [
            "foo",
            "foo.green",
            "bar.blue",
        ]:
            graph.add_module(module)
        import_details = dict(
            importer="foo",
            imported="bar.blue",
            line_number=1,
            line_contents="from . import bar",
        )
        graph.add_import(**import_details)

        graph.squash_module("foo")

        assert [import_details] == graph.get_import_details(
            importer="foo", imported="bar.blue"
        )

    def test_import_details_to_squashed_root_are_preserved(self):
        graph = ImportGraph()
        for module in [
            "foo",
            "foo.green",
            "bar.blue",
        ]:
            graph.add_module(module)
        import_details = dict(
            importer="bar.blue",
            imported="foo",
            line_number=1,
            line_contents="from . import foo",
        )
        graph.add_import(**import_details)

        graph.squash_module("foo")

        assert [import_details] == graph.get_import_details(
            importer="bar.blue", imported="foo"
        )

    def test_import_details_from_descendant_are_lost(self):
        graph = ImportGraph()
        for module in [
            "foo",
            "foo.green",
            "bar.blue",
        ]:
            graph.add_module(module)

        graph.add_import(
            importer="foo.green",
            imported="bar.blue",
            line_number=1,
            line_contents="from . import bar.blue",
        )

        graph.squash_module("foo")

        assert [] == graph.get_import_details(importer="foo", imported="bar.blue")

    def test_import_details_to_descendant_are_lost(self):
        graph = ImportGraph()
        for module in [
            "foo",
            "foo.green",
            "bar.blue",
        ]:
            graph.add_module(module)

        graph.add_import(
            importer="bar.blue",
            imported="foo.green",
            line_number=1,
            line_contents="from foo import green",
        )

        graph.squash_module("foo")

        assert [] == graph.get_import_details(importer="bar.blue", imported="foo")

    def test_does_nothing_if_module_is_already_squashed(self):
        graph = ImportGraph()
        graph.add_module("foo", is_squashed=True)
        graph.add_import(importer="foo", imported="bar")

        graph.squash_module("foo")

        assert graph.direct_import_exists(importer="foo", imported="bar")

    def test_raises_module_not_present_if_no_module(self):
        graph = ImportGraph()

        with pytest.raises(ModuleNotPresent):
            graph.squash_module("foo")


class TestFindAllSimpleChains:
    def test_raise_module_not_present_if_importer_missing(self):
        graph = ImportGraph()
        graph.add_module("bar")

        with pytest.raises(ModuleNotPresent):
            graph.find_all_simple_chains(importer="foo", imported="bar")

    def test_raise_module_not_present_if_imported_missing(self):
        graph = ImportGraph()
        graph.add_module("foo")

        with pytest.raises(ModuleNotPresent):
            graph.find_all_simple_chains(importer="foo", imported="bar")

    def test_finds_no_paths_if_none_exist(self):
        graph = ImportGraph()
        graph.add_module("foo")
        graph.add_module("bar")

        result = list(graph.find_all_simple_chains(importer="foo", imported="bar"))

        assert [] == result

    def test_finds_no_paths_if_wrong_direction(self):
        graph = ImportGraph()
        self._add_chain(graph, "foo", "bar")

        result = list(graph.find_all_simple_chains(importer="bar", imported="foo"))

        assert [] == result

    def test_finds_no_paths_if_importer_but_not_imported(self):
        graph = ImportGraph()
        self._add_chain(graph, "foo", "bar")
        graph.add_module("baz")

        result = list(graph.find_all_simple_chains(importer="foo", imported="baz"))

        assert [] == result

    def test_finds_no_paths_if_imported_but_not_importer(self):
        graph = ImportGraph()
        self._add_chain(graph, "foo", "bar")
        graph.add_module("baz")

        result = list(graph.find_all_simple_chains(importer="baz", imported="bar"))

        assert [] == result

    def test_finds_single_step_path(self):
        graph = ImportGraph()
        self._add_chain(graph, "foo", "bar")

        result = tuple(graph.find_all_simple_chains(importer="foo", imported="bar"))

        assert (("foo", "bar"),) == result

    def test_finds_two_step_path(self):
        graph = ImportGraph()
        self._add_chain(graph, "foo", "bar", "baz")

        result = tuple(graph.find_all_simple_chains(importer="foo", imported="baz"))

        assert (("foo", "bar", "baz"),) == result

    def test_finds_long_path(self):
        graph = ImportGraph()
        long_path = ("one", "two", "three", "four", "five")
        self._add_chain(graph, *long_path)

        result = tuple(graph.find_all_simple_chains(importer="one", imported="five"))

        assert (long_path,) == result

    def test_finds_multiple_paths(self):
        graph = ImportGraph()
        paths = (
            ("foo", "blue", "bar"),
            ("foo", "green", "bar"),
            ("foo", "red", "yellow", "bar"),
            ("foo", "brown", "purple", "grey", "pink", "bar"),
        )
        for path in paths:
            self._add_chain(graph, *path)

        result = set(graph.find_all_simple_chains(importer="foo", imported="bar"))

        assert set(paths) == result

    def test_includes_redundant_paths(self):
        # I'm not definitely sure we want this behaviour, but this is what networkx's
        # all_simple_paths gives us at the moment.
        graph = ImportGraph()
        paths = (
            ("foo", "blue", "bar"),
            ("foo", "green", "bar"),
            ("foo", "green", "blue", "bar"),
        )
        for path in paths:
            self._add_chain(graph, *path)

        result = set(graph.find_all_simple_chains(importer="foo", imported="bar"))

        assert set(paths) == result

    def _add_chain(self, graph, *modules):
        for index in range(len(modules) - 1):
            graph.add_import(
                importer=modules[index], imported=modules[index + 1],
            )
