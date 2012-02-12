import unittest
from hieroglyph.nodes import Node

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

    def test_create_with_children(self):
        root = Node()
        node = Node(parent=root)
        self.assertEqual(node.indent, 0)
        self.assertEqual(node.lines, [])
        self.assertIs(node.parent, root)

    def test_repr(self):
        node = Node(5, ['One', 'Two', 'Three'])
        actual = repr(node)
        expected = "Node(5, ['One', 'Two', 'Three'], children=[])"
        self.assertEqual(actual, expected)

    # TODO: Test add_child

    # TODO: Test render

