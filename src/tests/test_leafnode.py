import unittest

from src.leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("h1", "test value", {"class": "test-class", "id": "test-id"})
        node2 = LeafNode("h1", "test value", {"class": "test-class", "id": "test-id"})
        self.assertEqual(node, node2)
    def test_to_html(self):
        node = LeafNode("h1", "test value", {"class": "test-class", "id": "test-id"})
        self.assertEqual(node.to_html(), '<h1 class="test-class" id="test-id">test value</h1>')
        node_no_tag = LeafNode(None, "test value", {"class": "test-class", "id": "test-id"})
        self.assertEqual(node_no_tag.to_html(), 'test value')
