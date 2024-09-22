import unittest

from src.mdconverter import MDConverter
from src.textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node_with_italic = TextNode("This is a *test* node", "text_type_text")
        node_with_block2 = TextNode("This is a *test* node *woohoo* *test*", "text_type_text")
        node_with_code = TextNode("This is a `test` node", "text_type_text")
        converter = MDConverter()
        new_nodes = converter.split_nodes_delimiter([node_with_italic, node_with_block2], "*", "text_type_italic")
        another_nodes = converter.split_nodes_delimiter([node_with_code], "`", "text_type_code")
        self.assertEqual(new_nodes, [TextNode('This is a ', 'text_type_text', None), TextNode('test', 'text_type_italic', None), TextNode(' node', 'text_type_text', None), TextNode('This is a ', 'text_type_text', None), TextNode('test', 'text_type_italic', None), TextNode(' node ', 'text_type_text', None), TextNode('woohoo', 'text_type_italic', None), TextNode(' ', 'text_type_text', None), TextNode('test', 'text_type_italic', None), TextNode('', 'text_type_text', None)])
        self.assertEqual(another_nodes, [TextNode('This is a ', 'text_type_text', None), TextNode('test', 'text_type_code', None), TextNode(' node', 'text_type_text', None)])