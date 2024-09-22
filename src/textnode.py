from src.leafnode import LeafNode

class TextNode():
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    def __repr__(self) -> str:
        return f"TextNode('{self.text}', '{self.text_type}', '{self.url}')"
    
    def to_html_node(self):
        match self.text_type:
            case "text_type_text":
                return LeafNode(value=self.text)
            case "text_type_link":
                return LeafNode(tag="a", value=self.text, props={"href": self.url})
            case "text_type_bold":
                return LeafNode(tag="b", value=self.text)
            case "text_type_italic":
                return LeafNode(tag="i", value=self.text)
            case "text_type_underline":
                return LeafNode(tag="u", value=self.text)
            case "text_type_code":
                return LeafNode(tag="code", value=self.text)
            case "text_type_image":
                return LeafNode(tag="img", value = "", props={"src": self.url, "alt": self.text})
            case _:
                raise ValueError(f"Unknown text type: {self.text_type}")