import unittest
from hieroglyph.nodes import Node, Arg

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

    def test_create_with_lines(self):
        node = Arg(5, 10, 'foo')
        self.assertEqual(node.indent, 5)
        self.assertEqual(node.child_indent, 10)
        self.assertEqual(node.name, 'foo')
        self.assertEqual(node.lines, [])
        self.assertIsNone(node.parent)

    # TODO: Is lines ever modified here?

    def test_repr(self):
        node = Arg(5, 10, 'foo')
        actual = repr(node)
        expected = "Arg('foo', None, children=[])"
        self.assertEqual(expected, actual)

    # TODO test_render_rst

