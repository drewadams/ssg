import unittest
from src.parentnode import ParentNode
from src.leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_eq(self):
        child1 = LeafNode("p", "child1", {"class": "test-class", "id": "test-id"})
        child_nested = LeafNode("p", "child_nested", {"class": "test-class", "id": "test-id"})
        child_nested2 = LeafNode("p", "child_nested2", {"class": "test-class", "id": "test-id-2"})
        child_parent = ParentNode("div", "child2", [child_nested, child_nested2], {"class": "test-class", "id": "test-id"})
        node = ParentNode("div", "test value", [child1, child_parent], {"class": "test-class", "id": "test-id"})
        node2 = ParentNode("div", "test value", [child1, child_parent], {"class": "test-class", "id": "test-id"})
        node3 = ParentNode("div", "test value", [child1, child_nested2], {"class": "test-class", "id": "test-id-2"})
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
        
    def test_html(self):
        child1 = LeafNode("p", "child1", {"class": "test-class", "id": "test-id"})
        child_nested = LeafNode("p", "child_nested", {"class": "test-class", "id": "test-id"})
        child_nested2 = LeafNode("p", "child_nested2", {"class": "test-class", "id": "test-id-2"})
        child_parent = ParentNode("div", "child2", [child_nested, child_nested2], {"class": "test-class", "id": "test-id"})
        node = ParentNode("div", "test value", [child1, child_parent], {"class": "test-class", "id": "test-id"})
        self.assertEqual(node.to_html(), '<div class="test-class" id="test-id"><p class="test-class" id="test-id">child1</p><div class="test-class" id="test-id"><p class="test-class" id="test-id">child_nested</p><p class="test-class" id="test-id-2">child_nested2</p></div></div>')

    def test_repr(self):
        child1 = LeafNode("p", "child1", {"class": "test-class", "id": "test-id"})
        child_nested = LeafNode("p", "child_nested", {"class": "test-class", "id": "test-id"})
        child_nested2 = LeafNode("p", "child_nested2", {"class": "test-class", "id": "test-id-2"})
        child_parent = ParentNode("div", "child2", [child_nested, child_nested2], {"class": "test-class", "id": "test-id"})
        node = ParentNode("div", "test value", [child1, child_parent], {"class": "test-class", "id": "test-id"})
        # print(repr(node))
        self.assertEqual(repr(node), "ParentNode(div, test value, [LeafNode(p, child1, {'class': 'test-class', 'id': 'test-id'}), ParentNode(div, child2, [LeafNode(p, child_nested, {'class': 'test-class', 'id': 'test-id'}), LeafNode(p, child_nested2, {'class': 'test-class', 'id': 'test-id-2'})], {'class': 'test-class', 'id': 'test-id'})], {'class': 'test-class', 'id': 'test-id'})")