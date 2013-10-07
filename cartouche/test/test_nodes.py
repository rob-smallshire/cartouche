import unittest
from cartouche.nodes import (Node, Arg, Raises, Except, Returns, Warning,
                             Note, Yields, Attribute, Usage)

__author__ = 'Robert Smallshire'

class NodeTests(unittest.TestCase):

    def test_create_default_node(self):
        node = Node()
        self.assertEqual(node.indent, 0)
        self.assertEqual(node.lines, [])
        self.assertIsNone(node.parent)

    def test_create_with_indent(self):
        node = Node(indent=4)
        self.assertEqual(node.indent, 4)
        self.assertEqual(node.lines, [])
        self.assertIsNone(node.parent)

    def test_create_with_lines(self):
        node = Node(lines= ['First', 'Second', 'Third'])
        self.assertEqual(node.indent, 0)
        self.assertEqual(node.lines, ['First', 'Second', 'Third'])
        self.assertIsNone(node.parent)

    def test_repr(self):
        node = Node(5, ['One', 'Two', 'Three'])
        actual = repr(node)
        expected = "Node(5, ['One', 'Two', 'Three'], children=[])"
        self.assertEqual(expected, actual)

    def test_add_one_child(self):
        node = Node()
        child = Node(parent=node)
        node.add_child(child)
        self.assertIs(node.children[0], child)

    def test_add_two_children(self):
        node = Node()
        child0 = Node(parent=node)
        child1 = Node(parent=node)
        node.add_child(child0)
        node.add_child(child1)
        self.assertIs(node.children[0], child0)
        self.assertIs(node.children[1], child1)

    def test_render_rst_empty(self):
        node = Node()
        rst = node.render_rst()
        self.assertEqual(len(rst), 0)

    def test_render_rst_indent(self):
        node = Node(indent=4)
        rst = node.render_rst()
        self.assertEqual(len(rst), 0)

    def test_render_rst_lines(self):
        node = Node(lines= ['First',
                            'Second',
                            'Third'])
        rst = node.render_rst()
        self.assertEqual(rst, ['First',
                               'Second',
                               'Third'])

    def test_render_rst_indented_lines(self):
        node = Node(indent=3, lines= ['First',
                                      'Second',
                                      'Third'])
        rst = node.render_rst()
        self.assertEqual(rst, ['   First',
                               '   Second',
                               '   Third'])

    def test_render_rst_with_child(self):
        node = Node(indent=4, lines=["Parent"])
        child = Node(indent=8, lines=["Child"], parent=node)
        node.add_child(child)
        rst = node.render_rst()
        self.assertEqual(rst, ['    Parent',
                               '        Child'])

    def test_render_rst_with_children(self):
        node = Node(indent=4, lines=["Parent"])
        child_a = Node(indent=8, lines=["ChildA"], parent=node)
        node.add_child(child_a)
        child_b = Node(indent=6, lines=["ChildB"], parent=node)
        node.add_child(child_b)
        rst = node.render_rst()
        self.assertEqual(rst, ['    Parent',
                               '        ChildA',
                               '      ChildB'])


class ArgTests(unittest.TestCase):

    def test_create(self):
        node = Arg(5, 'foo')
        self.assertEqual(node.indent, 5)
        self.assertEqual(node.name, 'foo')
        self.assertEqual(node.lines, [])
        self.assertIsNone(node.parent)

    def test_set_type(self):
        node = Arg(5, 'foo')
        node.type = 'str'
        self.assertEqual(node.type, 'str')

    def test_add_one_child(self):
        node = Arg(5, 'foo')
        child = Node(parent=node)
        node.add_child(child)
        self.assertIs(node.children[0], child)

    def test_add_two_children(self):
        node = Arg(5, 'foo')
        child0 = Node(parent=node)
        child1 = Node(parent=node)
        node.add_child(child0)
        node.add_child(child1)
        self.assertIs(node.children[0], child0)
        self.assertIs(node.children[1], child1)

    def test_repr(self):
        node = Arg(5, 'foo')
        actual = repr(node)
        expected = "Arg('foo', None, children=[])"
        self.assertEqual(expected, actual)

    def test_render_rst_empty(self):
        node = Arg(5, 'bar')
        rst = node.render_rst()
        self.assertEqual(rst, ['     :param bar: ',
                               ''])

    def test_render_rst_with_child(self):
        node = Arg(5, 'bar')
        child = Node(indent=10, lines=["Description"], parent=node)
        node.add_child(child)
        rst = node.render_rst()
        self.assertEqual(rst, ['     :param bar: Description',
                               ''])

    def test_render_rst_with_children(self):
        node = Arg(5, 'bar')
        child_a = Node(indent=10, lines=["ChildA"], parent=node)
        node.add_child(child_a)
        child_b = Node(indent=10, lines=["ChildB"], parent=node)
        node.add_child(child_b)
        rst = node.render_rst()
        self.assertEqual(rst, ['     :param bar: ChildA',
                               '          ChildB',
                               ''])

    def test_render_rst_with_type(self):
        node = Arg(5, 'bar')
        node.type = 'str'
        rst = node.render_rst()
        self.assertEqual(rst, ['     :param bar: ',
                               '     :type bar: str',
                               ''])


class RaisesTests(unittest.TestCase):

    def test_create_default_node(self):
        node = Raises()
        self.assertEqual(node.indent, 0)
        self.assertEqual(node.lines, [])
        self.assertIsNone(node.parent)

    def test_create_with_indent(self):
        node = Raises(indent=4)
        self.assertEqual(node.indent, 4)
        self.assertEqual(node.lines, [])
        self.assertIsNone(node.parent)

    def test_repr(self):
        node = Raises(5)
        actual = repr(node)
        expected = "Raises(5, children=[])"
        self.assertEqual(expected, actual)

    def test_add_one_child(self):
        node = Raises()
        child = Node(parent=node)
        node.add_child(child)
        self.assertIs(node.children[0], child)

    def test_add_two_children(self):
        node = Raises()
        child0 = Node(parent=node)
        child1 = Node(parent=node)
        node.add_child(child0)
        node.add_child(child1)
        self.assertIs(node.children[0], child0)
        self.assertIs(node.children[1], child1)

    def test_render_rst_empty(self):
        node = Raises()
        rst = node.render_rst()
        self.assertEqual(rst, [':raises:',
                               ''])

    def test_render_rst_indent(self):
        node = Raises(indent=5)
        rst = node.render_rst()
        self.assertEqual(rst, ['     :raises:',
                               ''])

    def test_render_rst_with_child(self):
        node = Raises(5)
        child = Node(indent=10, lines=["Description"], parent=node)
        node.add_child(child)
        rst = node.render_rst()
        self.assertEqual(rst, ['     :raises:',
                               '          Description',
                               ''])

    def test_render_rst_with_children(self):
        node = Raises(5)
        child_a = Node(indent=10, lines=["ChildA"], parent=node)
        node.add_child(child_a)
        child_b = Node(indent=10, lines=["ChildB"], parent=node)
        node.add_child(child_b)
        rst = node.render_rst()
        self.assertEqual(rst, ['     :raises:',
                               '          ChildA',
                               '          ChildB',
                               ''])


class ExceptTests(unittest.TestCase):

    def test_create(self):
        node = Except(5, 'FooError')
        self.assertEqual(node.indent, 5)
        self.assertEqual(node.type, 'FooError')
        self.assertEqual(node.lines, [])
        self.assertIsNone(node.parent)

    def test_add_one_child(self):
        node = Except(5, 'FooError')
        child = Node(parent=node)
        node.add_child(child)
        self.assertIs(node.children[0], child)

    def test_add_two_children(self):
        node = Except(5, 'FooError')
        child0 = Node(parent=node)
        child1 = Node(parent=node)
        node.add_child(child0)
        node.add_child(child1)
        self.assertIs(node.children[0], child0)
        self.assertIs(node.children[1], child1)

    def test_repr(self):
        node = Except(5,'FooError')
        actual = repr(node)
        expected = "Except('FooError', children=[])"
        self.assertEqual(expected, actual)

    def test_render_rst_empty(self):
        node = Except(5, 'FooError')
        rst = node.render_rst()
        self.assertEqual(rst, ['     * FooError - ',
                               ''])

    def test_render_rst_indent(self):
        node = Except(5, 'FooError')
        rst = node.render_rst()
        self.assertEqual(rst, ['     * FooError - ',
                               ''])

    def test_render_rst_with_child(self):
        node = Except(5, 'FooError')
        child = Node(indent=10, lines=["Description"], parent=node)
        node.add_child(child)
        rst = node.render_rst()
        self.assertEqual(rst, ['     * FooError - Description',
                               ''])

    def test_render_rst_with_children(self):
        node = Except(5, 'FooError')
        child_a = Node(indent=10, lines=["ChildA"], parent=node)
        node.add_child(child_a)
        child_b = Node(indent=10, lines=["ChildB"], parent=node)
        node.add_child(child_b)
        rst = node.render_rst()
        self.assertEqual(rst, ['     * FooError - ChildA',
                               '          ChildB',
                               ''])

class ReturnsTests(unittest.TestCase):

    def test_create(self):
        node = Returns(5)
        self.assertEqual(node.indent, 5)
        self.assertEqual(node.lines, [])
        self.assertIsNone(node.parent)

    def test_add_one_child(self):
        node = Returns(5)
        child = Node(parent=node)
        node.add_child(child)
        self.assertIs(node.children[0], child)

    def test_add_two_children(self):
        node = Returns(5)
        child0 = Node(parent=node)
        child1 = Node(parent=node)
        node.add_child(child0)
        node.add_child(child1)
        self.assertIs(node.children[0], child0)
        self.assertIs(node.children[1], child1)

    def test_repr(self):
        node = Returns(5)
        actual = repr(node)
        expected = "Returns(5, children=[])"
        self.assertEqual(expected, actual)

    def test_render_rst_empty(self):
        node = Returns(indent=4)
        rst = node.render_rst()
        self.assertEqual(rst, ['    :returns: ',
                               ''])

    def test_render_rst_indent(self):
        node = Returns(indent=5)
        rst = node.render_rst()
        self.assertEqual(rst, ['     :returns: ',
                               ''])

    def test_render_rst_with_child(self):
        node = Returns(indent=5)
        child = Node(indent=10, lines=["Description"], parent=node)
        node.add_child(child)
        rst = node.render_rst()
        self.assertEqual(rst, ['     :returns: Description',
                               ''])

    def test_render_rst_with_children(self):
        node = Returns(indent=5)
        child_a = Node(indent=10, lines=["ChildA"], parent=node)
        node.add_child(child_a)
        child_b = Node(indent=10, lines=["ChildB"], parent=node)
        node.add_child(child_b)
        rst = node.render_rst()
        self.assertEqual(rst, ['     :returns: ChildA',
                               '          ChildB',
                               ''])

class YieldsTests(unittest.TestCase):

    def test_create(self):
        node = Yields(5)
        self.assertEqual(node.indent, 5)
        self.assertEqual(node.lines, [])
        self.assertIsNone(node.parent)

    def test_add_one_child(self):
        node = Yields(5)
        child = Node(parent=node)
        node.add_child(child)
        self.assertIs(node.children[0], child)

    def test_add_two_children(self):
        node = Yields(5)
        child0 = Node(parent=node)
        child1 = Node(parent=node)
        node.add_child(child0)
        node.add_child(child1)
        self.assertIs(node.children[0], child0)
        self.assertIs(node.children[1], child1)

    def test_repr(self):
        node = Yields(5)
        actual = repr(node)
        expected = "Yields(5, children=[])"
        self.assertEqual(expected, actual)

    def test_render_rst_empty(self):
        node = Yields(indent=4)
        rst = node.render_rst()
        self.assertEqual(rst, ['    :returns: ',
                               ''])

    def test_render_rst_indent(self):
        node = Yields(indent=5)
        rst = node.render_rst()
        self.assertEqual(rst, ['     :returns: ',
                               ''])

    def test_render_rst_with_child(self):
        node = Yields(indent=5)
        child = Node(indent=10, lines=["Description"], parent=node)
        node.add_child(child)
        rst = node.render_rst()
        self.assertEqual(rst, ['     :returns: Description',
                               ''])

    def test_render_rst_with_children(self):
        node = Yields(indent=5)
        child_a = Node(indent=10, lines=["ChildA"], parent=node)
        node.add_child(child_a)
        child_b = Node(indent=10, lines=["ChildB"], parent=node)
        node.add_child(child_b)
        rst = node.render_rst()
        self.assertEqual(rst, ['     :returns: ChildA',
                               '          ChildB',
                               ''])

class WarningTests(unittest.TestCase):

    def test_create(self):
        node = Warning(5)
        self.assertEqual(node.indent, 5)
        self.assertEqual(node.lines, [])
        self.assertIsNone(node.parent)

    # TODO: test when setting node.line

    def test_add_one_child(self):
        node = Warning(5)
        child = Node(parent=node)
        node.add_child(child)
        self.assertIs(node.children[0], child)

    def test_add_two_children(self):
        node = Warning(5)
        child0 = Node(parent=node)
        child1 = Node(parent=node)
        node.add_child(child0)
        node.add_child(child1)
        self.assertIs(node.children[0], child0)
        self.assertIs(node.children[1], child1)

    def test_repr(self):
        node = Warning(5)
        actual = repr(node)
        expected = "Warning(5, children=[])"
        self.assertEqual(expected, actual)

    def test_render_rst_empty(self):
        node = Warning(indent=4)
        rst = node.render_rst()
        self.assertEqual(rst, ['    .. warning::',
                               '    '])

    def test_render_rst_indent(self):
        node = Warning(indent=5)
        rst = node.render_rst()
        self.assertEqual(rst, ['     .. warning::',
                               '     '])

    def test_render_rst_with_child(self):
        node = Warning(indent=5)
        child = Node(indent=10, lines=["Description"], parent=node)
        node.add_child(child)
        rst = node.render_rst()
        self.assertEqual(rst, ['     .. warning::',
                               '     ',
                               '          Description',
                               ''])

    def test_render_rst_with_children(self):
        node = Warning(indent=5)
        child_a = Node(indent=10, lines=["ChildA"], parent=node)
        node.add_child(child_a)
        child_b = Node(indent=12, lines=["ChildB"], parent=node)
        node.add_child(child_b)
        rst = node.render_rst()
        self.assertEqual(rst, ['     .. warning::',
                               '     ',
                               '          ChildA',
                               '            ChildB',
                               ''])

class NoteTests(unittest.TestCase):

    def test_create(self):
        node = Note(5)
        self.assertEqual(node.indent, 5)
        self.assertEqual(node.lines, [])
        self.assertIsNone(node.parent)

    # TODO: test when setting node.line

    def test_add_one_child(self):
        node = Note(5)
        child = Node(parent=node)
        node.add_child(child)
        self.assertIs(node.children[0], child)

    def test_add_two_children(self):
        node = Note(5)
        child0 = Node(parent=node)
        child1 = Node(parent=node)
        node.add_child(child0)
        node.add_child(child1)
        self.assertIs(node.children[0], child0)
        self.assertIs(node.children[1], child1)

    def test_repr(self):
        node = Note(5)
        actual = repr(node)
        expected = "Note(5, children=[])"
        self.assertEqual(expected, actual)

    def test_repr(self):
        node = Warning(5)
        actual = repr(node)
        expected = "Warning(5, children=[])"
        self.assertEqual(expected, actual)

    def test_render_rst_empty(self):
        node = Note(indent=4)
        rst = node.render_rst()
        self.assertEqual(rst, ['    .. note::',
                               '    '])

    def test_render_rst_indent(self):
        node = Note(indent=5)
        rst = node.render_rst()
        self.assertEqual(rst, ['     .. note::',
                               '     '])

    def test_render_rst_with_child(self):
        node = Note(indent=5)
        child = Node(indent=10, lines=["Description"], parent=node)
        node.add_child(child)
        rst = node.render_rst()
        self.assertEqual(rst, ['     .. note::',
                               '     ',
                               '          Description',
                               ''])

    def test_render_rst_with_children(self):
        node = Note(indent=5)
        child_a = Node(indent=10, lines=["ChildA"], parent=node)
        node.add_child(child_a)
        child_b = Node(indent=12, lines=["ChildB"], parent=node)
        node.add_child(child_b)
        rst = node.render_rst()
        self.assertEqual(rst, ['     .. note::',
                               '     ',
                               '          ChildA',
                               '            ChildB',
                               ''])

class AttributeTests(unittest.TestCase):

    def test_create(self):
        node = Attribute(5, 'foo')
        self.assertEqual(node.indent, 5)
        self.assertEqual(node.name, 'foo')
        self.assertEqual(node.lines, [])
        self.assertIsNone(node.parent)

    def test_set_type(self):
        node = Attribute(5, 'foo')
        node.type = 'str'
        self.assertEqual(node.type, 'str')

    def test_add_one_child(self):
        node = Attribute(5, 'foo')
        child = Node(parent=node)
        node.add_child(child)
        self.assertIs(node.children[0], child)

    def test_add_two_children(self):
        node = Attribute(5, 'foo')
        child0 = Node(parent=node)
        child1 = Node(parent=node)
        node.add_child(child0)
        node.add_child(child1)
        self.assertIs(node.children[0], child0)
        self.assertIs(node.children[1], child1)

    def test_repr(self):
        node = Attribute(5, 'foo')
        actual = repr(node)
        expected = "Attribute('foo', None, children=[])"
        self.assertEqual(expected, actual)

    def test_render_rst_empty(self):
        node = Attribute(5, 'bar')
        rst = node.render_rst()
        self.assertEqual(rst, ['.. py:attribute:: bar',
                               ''])

    def test_render_rst_with_child(self):
        node = Attribute(5, 'bar')
        child = Node(indent=10, lines=["Description"], parent=node)
        node.add_child(child)
        rst = node.render_rst()
        self.assertEqual(rst, ['.. py:attribute:: bar',
                               '',
                               '   Description',
                               ''])

    def test_render_rst_with_children(self):
        node = Attribute(5, 'bar')
        child_a = Node(indent=10, lines=["ChildA"], parent=node)
        node.add_child(child_a)
        child_b = Node(indent=10, lines=["ChildB"], parent=node)
        node.add_child(child_b)
        rst = node.render_rst()
        self.assertEqual(rst, ['.. py:attribute:: bar',
                               '',
                               '   ChildA',
                               '   ChildB',
                               ''])

    def test_render_rst_with_type(self):
        node = Attribute(5, 'bar')
        node.type = 'str'
        rst = node.render_rst()
        self.assertEqual(rst, ['.. py:attribute:: bar',
                               '',
                               '   (str)',
                               ''])

    def test_render_rst_with_type_and_description(self):
        node = Attribute(5, 'bar')
        node.type = 'str'
        child = Node(indent=10, lines=["Description"], parent=node)
        node.add_child(child)
        rst = node.render_rst()
        self.assertEqual(rst, ['.. py:attribute:: bar',
                               '',
                               '   (str) Description',
                               ''])

    def test_render_rst_with_type_and_multi_line_description(self):
        node = Attribute(5, 'bar')
        node.type = 'str'
        child = Node(indent=10, lines=["Description1", "Description2"], parent=node)
        node.add_child(child)
        rst = node.render_rst()
        self.assertEqual(rst, ['.. py:attribute:: bar',
                               '',
                               '   (str) Description1',
                               '   Description2',
                               ''])

class UsageTests(unittest.TestCase):

    def test_create(self):
        node = Usage(5)
        self.assertEqual(node.indent, 5)
        self.assertEqual(node.lines, [])
        self.assertIsNone(node.parent)


    def test_add_one_child(self):
        node = Usage(5)
        child = Node(parent=node)
        node.add_child(child)
        self.assertIs(node.children[0], child)

    def test_add_two_children(self):
        node = Usage(5)
        child0 = Node(parent=node)
        child1 = Node(parent=node)
        node.add_child(child0)
        node.add_child(child1)
        self.assertIs(node.children[0], child0)
        self.assertIs(node.children[1], child1)

    def test_repr(self):
        node = Usage(5)
        actual = repr(node)
        expected = "Usage(5)"
        self.assertEqual(expected, actual)

    def test_render_rst_empty(self):
        node = Usage(5)
        rst = node.render_rst()
        self.assertEqual(rst, [])

    def test_render_rst_with_code(self):
        node = Usage(7)
        child_a = Node(indent=10, lines=['print("Hello, World!")'], parent=node)
        node.add_child(child_a)
        child_b = Node(indent=10, lines=['print("Reticulating splines!")'], parent=node)
        node.add_child(child_b)
        rst = node.render_rst()
        self.assertEqual(rst, ['       .. rubric:: Usage:',
                               '',
                               '       .. code-block:: python',
                               '',
                               '          print("Hello, World!")',
                               '          print("Reticulating splines!")',
                               ''])

    def test_render_rst_with_indented_code(self):
        node = Usage(5)
        child_a = Node(indent=10, lines=['for i in range(100):'], parent=node)
        node.add_child(child_a)
        child_b = Node(indent=14, lines=['print(i)'], parent=node)
        node.add_child(child_b)
        rst = node.render_rst()
        self.assertEqual(rst, ['     .. rubric:: Usage:',
                               '',
                               '     .. code-block:: python',
                               '',
                               '        for i in range(100):',
                               '            print(i)',
                               ''])
