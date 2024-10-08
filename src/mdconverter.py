from typing import List, NamedTuple, Optional
from src.leafnode import LeafNode
from src.parentnode import ParentNode
from src.textnode import TextNode
import re
class ImageData(NamedTuple):
    alt: str
    src: str

class LinkData(NamedTuple):
    text: str
    href: str
class MDConverter:
    def __init__(self, md = None):
        self.md = md
        self.regex = r"\[(.*?)\]\((.*?)\)"
        self.link_regex = re.compile(rf"(?<![!]){self.regex}")
        self.image_regex = re.compile(rf"!{self.regex}")
        self.block_types = [("heading", "#"), ("list", "* "), ("list", "-"), ("quote", ">"), ("ordered_list", "1. "), ("code", "```")]

    def extract_md_image(self, text: str) -> Optional[ImageData]:
        matches = self.image_regex.findall(text)
        if not matches:
            return None
        return matches[0]
    
    def extract_md_link(self, text: str) -> Optional[LinkData]:
        matches = self.link_regex.findall(text)
        if not matches:
            return None

        return matches[0]
    
    def split_nodes_delimiter(self, old_nodes, delimiter, text_type):
        new_nodes = []
        for node in old_nodes:
            if delimiter in node.text:
                parts = node.text.split(delimiter)
                for i, part in enumerate(parts):
                    if i % 2 == 0 or i == 0 and part.endswith(delimiter):
                        new_nodes.append(TextNode(part, node.text_type))
                    else:
                        new_nodes.append(TextNode(part, text_type))
            else:
                new_nodes.append(node)
        return new_nodes
    
    def split_nodes_type(self, old_nodes, regex_matcher, regex_splitter, extractor_func, text_type):
        """
        Splits nodes based on a specific type (e.g., image, link) using regex matching and extraction.

        Args:
            old_nodes (List[TextNode]): The list of existing text nodes.
            regex_matcher (Pattern): The compiled regex pattern to match the specific type.
            regex_splitter (str): The regex pattern to split the text.
            extractor_func (Callable): The function to extract data from the matched text.
            text_type (str): The type of text to assign to the new nodes.

        Returns:
            List[TextNode]: The list of new text nodes with the specific type applied.
        """
        new_nodes = []
        for node in old_nodes:
            # Check if the node text matches the regex pattern
            if regex_matcher.findall(node.text):
                # Split the text based on the regex splitter
                parts = re.split(regex_splitter, node.text)
                # Filter out empty parts
                filtered_parts = [part for part in parts if part]
                for part in filtered_parts:
                    # Extract data using the extractor function
                    extracted_data = extractor_func(part)
                    if extracted_data:
                        # Create a new TextNode with the extracted data and specified text type
                        new_nodes.append(TextNode(extracted_data[0], text_type, extracted_data[1]))
                    else:
                        # Create a new TextNode with the original text type
                        new_nodes.append(TextNode(part, node.text_type))
            else:
                # If no match, retain the original node
                new_nodes.append(node)
        return new_nodes

    def split_nodes_image(self, old_nodes):
        splitter = r"(!\[.*?\]\(.*?\))"
        return self.split_nodes_type(old_nodes, self.image_regex, splitter, self.extract_md_image, "text_type_image")

    def split_nodes_link(self, old_nodes):
        splitter = r"((?<![!])\[.*?\]\([^)]*\))"
        return self.split_nodes_type(old_nodes, self.link_regex, splitter, self.extract_md_link, "text_type_link")
    
    def text_to_textnodes(self, text):
        nodes = [TextNode(line, "text_type_text") for line in text.split("\n")]
        nodes = self.split_nodes_image(nodes)
        nodes = self.split_nodes_link(nodes)
        text_types = [("text_type_bold", "**"), ("text_type_italic","*"), ("text_type_code", "`"), ("text_type_italic", "_")]
        for text_type, delimiter in text_types:
            nodes = self.split_nodes_delimiter(nodes, delimiter, text_type)
        return [node.to_html_node() for node in nodes]

    def markdown_to_blocks(self, md):
        return [block.strip() for block in md.split("\n\n") if block]

    def block_to_block_type(self, block):
        # This would be theoretically faster if we used a dictionary
        # instead of a list of tuples. However, 
        # For some reason it's not working as expected.
        for block_type, prefix in self.block_types:
            if block.startswith(prefix):
                return block_type
        return "paragraph"
    
    def markup_list_block(self, block):
        html = ParentNode(tag = "ul")
        children = []
        for line in block.split("\n"):
            if not line.startswith("*") and not line.startswith("-"):
                raise Exception("Invalid list block")
            children.append(ParentNode(tag = "li", children = self.text_to_textnodes(line[1:].strip())))
        html.children = children
        return html
    
    def markup_ordered_list_block(self, block):
        html = ParentNode(tag = "ol")
        children = []
        for line in block.split("\n"):
            if not re.match(r"^\d+\.", line):
                raise Exception("Invalid ordered list block")
            children.append(ParentNode(tag = "li", children = self.text_to_textnodes(line[2:].strip())))
        html.children = children
        return html
    
    def markup_heading_block(self, block):
        level = 1
        while block[level] == "#":
            if level == 6:
                break
            level += 1
        return ParentNode(tag = f"h{level}", children = self.text_to_textnodes(block[level:].strip()))
    
    def markup_quote_block(self, block):
        html = ParentNode(tag = "blockquote")
        for line in block.split("\n"):
            if not html.children:
                html.children = self.text_to_textnodes(line[1:].strip())
                continue
            html.children.extend(self.text_to_textnodes(line[1:].strip()))

        return html
        
    def markup_code_block(self, block: str):
        return LeafNode(tag = "code", value = block.strip("```"))
    
    def markup_paragraph_block(self, block: str):
        return self.text_to_textnodes(block)

    def markdown_to_html_node(self, md):
        html = []
        blocks = self.markdown_to_blocks(md)
        for block in blocks:
            block_type = self.block_to_block_type(block)
            match block_type:
                case "heading":
                    html.append(self.markup_heading_block(block))
                case "list":
                    html.append(self.markup_list_block(block))
                case "quote":
                    html.append(self.markup_quote_block(block))
                case "ordered_list":
                    html.append(self.markup_ordered_list_block(block))
                case "code":
                    html.append(self.markup_code_block(block))
                case "paragraph":
                    html.extend(self.markup_paragraph_block(block))
                case _:
                    raise ValueError(f"Unknown block type: {block_type}")
        return ParentNode(tag = "div", children = html)

    def extract_title(self, md: str) -> str:
        if not md.startswith("# "):
            raise ValueError("Markdown must start with a header")
        return md.split("\n")[0].replace("# ", "")