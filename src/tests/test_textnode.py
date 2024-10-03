import unittest

from src.textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
    def test_url(self):
        node = TextNode("Text node 1", "italic", "test url")
        node2 = TextNode("Text node 1", "italic", "test url")
        self.assertEqual(node, node2)
    def test_repr(self):
        node = TextNode("Text node 1", "italic", "test url")
        self.assertEqual(repr(node), "TextNode('Text node 1', 'italic', 'test url')")
    def test_unequal(self):
        node = TextNode("Text node 1", "italic", "test url")
        node2 = TextNode("Text node 2", "italic", "test url")
        node3 = TextNode("Text node 2", "bold", "test url")
        node4 = TextNode("Text node 2", "bold", "test url 4")
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node2, node3)
        self.assertNotEqual(node3, node4)
    def test_unset_url(self):
        node = TextNode("Text node 1", "italic")
        self.assertIsNone(node.url)
    def test_to_html_node(self):
        node = TextNode("This is a text node", "text_type_bold")
        code_node = TextNode("This is a code node", "text_type_code")
        image_node = TextNode("This is an image node", "text_type_image", "test url")
        link_node = TextNode("this is a link node", "text_type_link", "https://www.google.com")
        raw_node = TextNode("This is a raw node", "text_type_text")
        self.assertEqual(node.to_html_node().to_html(), "<b>This is a text node</b>")
        self.assertEqual(code_node.to_html_node().to_html(), "<code>This is a code node</code>")
        self.assertEqual(image_node.to_html_node().to_html(), '<img src="test url" alt="This is an image node">')
        self.assertEqual(link_node.to_html_node().to_html(), '<a href="https://www.google.com">this is a link node</a>')
        self.assertEqual(raw_node.to_html_node().to_html(), "This is a raw node")
