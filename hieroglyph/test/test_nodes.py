import unittest
from hieroglyph.nodes import Node, Arg, Raises, Except, Returns, Warning, Note

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

    # TODO test_render_rst


class ArgTests(unittest.TestCase):

    def test_create(self):
        node = Arg(5, 10, 'foo')
        self.assertEqual(node.indent, 5)
        self.assertEqual(node.child_indent, 10)
        self.assertEqual(node.name, 'foo')
        self.assertEqual(node.lines, [])
        self.assertIsNone(node.parent)

    def test_add_one_child(self):
        node = Arg(5, 10, 'foo')
        child = Node(parent=node)
        node.add_child(child)
        self.assertIs(node.children[0], child)

    def test_add_two_children(self):
        node = Arg(5, 10, 'foo')
        child0 = Node(parent=node)
        child1 = Node(parent=node)
        node.add_child(child0)
        node.add_child(child1)
        self.assertIs(node.children[0], child0)
        self.assertIs(node.children[1], child1)

    def test_repr(self):
        node = Arg(5, 10, 'foo')
        actual = repr(node)
        expected = "Arg('foo', None, children=[])"
        self.assertEqual(expected, actual)

    # TODO test_render_rst


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

    def test_create_with_lines(self):
        node = Raises(lines= ['First', 'Second', 'Third'])
        self.assertEqual(node.indent, 0)
        self.assertEqual(node.lines, ['First', 'Second', 'Third'])
        self.assertIsNone(node.parent)

    def test_repr(self):
        node = Raises(5, ['One', 'Two', 'Three'])
        actual = repr(node)
        expected = "Raises(5, ['One', 'Two', 'Three'], children=[])"
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

class ExceptTests(unittest.TestCase):

    def test_create(self):
        node = Except(5, 10, 'foo')
        self.assertEqual(node.indent, 5)
        self.assertEqual(node.child_indent, 10)
        self.assertEqual(node.type, 'foo')
        self.assertEqual(node.lines, [])
        self.assertIsNone(node.parent)

    def test_add_one_child(self):
        node = Except(5, 10, 'foo')
        child = Node(parent=node)
        node.add_child(child)
        self.assertIs(node.children[0], child)

    def test_add_two_children(self):
        node = Except(5, 10, 'foo')
        child0 = Node(parent=node)
        child1 = Node(parent=node)
        node.add_child(child0)
        node.add_child(child1)
        self.assertIs(node.children[0], child0)
        self.assertIs(node.children[1], child1)

    def test_repr(self):
        node = Except(5, 10, 'foo')
        actual = repr(node)
        expected = "Except('foo', children=[])"
        self.assertEqual(expected, actual)

    # TODO test_render_rst

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

    # TODO test_render_rst

class WarningTests(unittest.TestCase):

    def test_create(self):
        node = Warning(5)
        self.assertEqual(node.indent, 5)
        self.assertEqual(node.lines, [])
        self.assertIsNone(node.parent)

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

        # TODO test_render_rst

class NoteTests(unittest.TestCase):

    def test_create(self):
        node = Note(5)
        self.assertEqual(node.indent, 5)
        self.assertEqual(node.lines, [])
        self.assertIsNone(node.parent)

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

        # TODO test_render_rst
