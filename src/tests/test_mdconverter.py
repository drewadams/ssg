import unittest

from src.htmlnode import HTMLNode
from src.leafnode import LeafNode
from src.parentnode import ParentNode
from src.mdconverter import MDConverter
from src.textnode import TextNode

class TestTextNode(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        node_with_italic = TextNode("This is a *test* node", "text_type_text")
        node_with_bold_and_italics = TextNode("This is a *test* node with some **bold** text", "text_type_text")
        # node_with_block2 = TextNode("This is a *test* node *woohoo* *test*", "text_type_text")
        node_with_code = TextNode("This is a `test` node", "text_type_text")
        converter = MDConverter()
        new_nodes = converter.split_nodes_delimiter([node_with_italic, node_with_bold_and_italics], "**", "text_type_bold")
        new_nodes2 = converter.split_nodes_delimiter(new_nodes, "*", "text_type_italic")
        self.assertEqual(new_nodes2, [TextNode('This is a ', 'text_type_text', None), TextNode('test', 'text_type_italic', None), TextNode(' node', 'text_type_text', None), TextNode('This is a ', 'text_type_text', None), TextNode('test', 'text_type_italic', None), TextNode(' node with some ', 'text_type_text', None), TextNode('bold', 'text_type_bold', None), TextNode(' text', 'text_type_text', None)])
        another_nodes = converter.split_nodes_delimiter([node_with_code], "`", "text_type_code")
        self.assertEqual(another_nodes, [TextNode('This is a ', 'text_type_text', None), TextNode('test', 'text_type_code', None), TextNode(' node', 'text_type_text', None)])
    
    def test_extract_md_images(self):
        converter = MDConverter()
        self.assertEqual(converter.extract_md_image("![image1](https://www.google.com/image1)"), ('image1', 'https://www.google.com/image1'))
        
    def test_extract_md_links(self):
        converter = MDConverter("[link 1](https://www.google.com/link1)")
        self.assertEqual(converter.extract_md_link("[link 1](https://www.google.com/link1)"), ('link 1', 'https://www.google.com/link1'))

    def test_split_nodes_image(self):
        converter = MDConverter()
        node_with_image = TextNode("This is an ![image](https://www.google.com/image) node", "text_type_text")
        new_nodes = converter.split_nodes_image([node_with_image])
        self.assertEqual(new_nodes, [TextNode('This is an ', 'text_type_text', None), TextNode('image', 'text_type_image', 'https://www.google.com/image'), TextNode(' node', 'text_type_text', None)])
        node_with_multiple_images = TextNode("This is an ![image](https://www.google.com/image) node ![image2](https://www.google.com/image2) more text", "text_type_text")
        node_with_no_image = TextNode("This is a regular text node", "text_type_text")
        new_nodes = converter.split_nodes_image([node_with_image, node_with_multiple_images, node_with_no_image])
        self.assertEqual(new_nodes, [TextNode('This is an ', 'text_type_text', None), TextNode('image', 'text_type_image', 'https://www.google.com/image'), TextNode(' node', 'text_type_text', None), TextNode('This is an ', 'text_type_text', None), TextNode('image', 'text_type_image', 'https://www.google.com/image'), TextNode(' node ', 'text_type_text', None), TextNode('image2', 'text_type_image', 'https://www.google.com/image2'), TextNode(' more text', 'text_type_text', None), TextNode('This is a regular text node', 'text_type_text', None)])
        

    def test_split_nodes_link(self):
        converter = MDConverter()
        node_with_link = TextNode("This is a [link](https://www.google.com/link) node", "text_type_text")
        node_with_link2 = TextNode("This is a [link 2](https://www.google.com/link2) node", "text_type_text")
        node_with_multiple_links = TextNode("This is a [link 2](https://www.google.com/link2) node [link 3](https://www.google.com/link3)", "text_type_text")
        node_without_link = TextNode("This is a regular text node", "text_type_text")
        new_nodes = converter.split_nodes_link([node_with_link, node_without_link, node_with_link2, node_with_multiple_links])
        self.assertEqual(new_nodes, [TextNode('This is a ', 'text_type_text', None), TextNode('link', 'text_type_link', 'https://www.google.com/link'), TextNode(' node', 'text_type_text', None), TextNode('This is a regular text node', 'text_type_text', None), TextNode('This is a ', 'text_type_text', None), TextNode('link 2', 'text_type_link', 'https://www.google.com/link2'), TextNode(' node', 'text_type_text', None), TextNode('This is a ', 'text_type_text', None), TextNode('link 2', 'text_type_link', 'https://www.google.com/link2'), TextNode(' node ', 'text_type_text', None), TextNode('link 3', 'text_type_link', 'https://www.google.com/link3')])

    def test_text_to_textnodes(self):
        converter = MDConverter()
        text = "This is a **bold** text\nThis is an *italic* text\nThis is a `code` text\nThis is a [link](https://www.google.com/link) text\nThis is an ![image](https://www.google.com/image) text\nThis is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = converter.text_to_textnodes(text)
        self.assertEqual(nodes, [LeafNode(None, 'This is a ', None), LeafNode('b', 'bold', None), LeafNode(None, ' text', None), LeafNode(None, 'This is an ', None), LeafNode('i', 'italic', None), LeafNode(None, ' text', None), LeafNode(None, 'This is a ', None), LeafNode('code', 'code', None), LeafNode(None, ' text', None), LeafNode(None, 'This is a ', None), LeafNode('a', 'link', {'href': 'https://www.google.com/link'}), LeafNode(None, ' text', None), LeafNode(None, 'This is an ', None), LeafNode('img', '', {'src': 'https://www.google.com/image', 'alt': 'image'}), LeafNode(None, ' text', None), LeafNode(None, 'This is ', None), LeafNode('b', 'text', None), LeafNode(None, ' with an ', None), LeafNode('i', 'italic', None), LeafNode(None, ' word and a ', None), LeafNode('code', 'code block', None), LeafNode(None, ' and an ', None), LeafNode('img', '', {'src': 'https://i.imgur.com/fJRm4Vk.jpeg', 'alt': 'obi wan image'}), LeafNode(None, ' and a ', None), LeafNode('a', 'link', {'href': 'https://boot.dev'})])

    def test_md_to_blocks(self):
        converter = MDConverter()
        md = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        blocks = converter.markdown_to_blocks(md)
        self.assertEqual(blocks, ['# This is a heading', 'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', '* This is the first list item in a list block\n* This is a list item\n* This is another list item'])

    def test_block_to_block_type(self):
        converter = MDConverter()
        heading_block = "# This is a heading"
        list_block = "* This is a list item\n* This is another list item"
        paragraph_block = "This is a paragraph of text. It has some **bold** and *italic* words inside of it."
        code_block = "```python\nprint('Hello, World!')\n```"
        ordered_list_block = "1. This is an ordered list item\n2. This is another ordered list item"
        # quote_block = "> This is a quote"
        # self.assertEqual(converter.block_to_block_type(quote_block), "quote")
        self.assertEqual(converter.block_to_block_type(ordered_list_block), "ordered_list")
        self.assertEqual(converter.block_to_block_type(code_block), "code")
        self.assertEqual(converter.block_to_block_type(heading_block), "heading")
        self.assertEqual(converter.block_to_block_type(list_block), "list")
        self.assertEqual(converter.block_to_block_type(paragraph_block), "paragraph")

    def test_md_to_html_nodes(self):
        converter = MDConverter()
        md = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n## this is an h2\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item\n\n"
        md += "```python\nprint('Hello, World!')\n```\n\n"
        md += "1. This is an ordered list item\n2. This is another ordered list item\n\n"
        md += "> This is a quote\n> this is still the same quote\n\n"
        md += "This is a **bold** text\nThis is an *italic* text\nThis is a `code` text\nThis is a [link](https://www.google.com/link) text\nThis is an ![image](https://www.google.com/image) text\nThis is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        html_nodes = converter.markdown_to_html_node(md)
        converted_h1_leaf = html_nodes.children[0].children[0] # this is because we have headings as parent nodes, to allow for other markup inside of the heading.
        self.assertIsInstance(html_nodes, ParentNode)
        self.assertEqual(html_nodes.tag, "div")
        self.assertIsInstance(html_nodes.children[0], HTMLNode)
        self.assertEqual(html_nodes.children[0].tag, "h1")
        self.assertEqual(converted_h1_leaf.tag, None)
        self.assertEqual(converted_h1_leaf.value, "This is a heading")
        # self.assertEqual(len(html_nodes.children), 8)

    def test_extract_title(self):
        converter = MDConverter()
        md = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n## this is an h2\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item\n\n"
        heading = converter.extract_title(md)
        self.assertEqual(heading, "This is a heading")