import unittest

from src.htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("h1", "test value", ["child1", "child2"], {"class": "test-class", "id": "test-id"})
        node2 = HTMLNode("h1", "test value", ["child1", "child2"], {"class": "test-class", "id": "test-id"})
        node3 = HTMLNode("h2", "test value", ["child1", "child2"], {"class": "test-class", "id": "test-id"})
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
    def test_repr(self):
        node = HTMLNode("h1", "test value", ["child1", "child2"], {"class": "test-class", "id": "test-id"})
        self.assertEqual(repr(node), "HTMLNode(h1, test value, ['child1', 'child2'], {'class': 'test-class', 'id': 'test-id'})")
    def test_props_to_html(self):
        node = HTMLNode("h1", "test value", ["child1", "child2"], {"class": "test-class", "id": "test-id"})
        self.assertEqual(node.props_to_html(), ' class="test-class" id="test-id"')
    def test_to_html(self):
        node = HTMLNode("h1", "test value", ["child1", "child2"], {"class": "test-class", "id": "test-id"})
        self.assertRaises(NotImplementedError, node.to_html)
        
