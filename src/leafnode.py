from src.htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag = None, value = None, props: dict = None) -> None:
        super().__init__(tag, value, [], props)

    def __repr__(self) -> str:
        return f"LeafNode('{self.tag}', '{self.value}', {self.props})"
    def to_html(self) -> str:
        if (self.value is None):
            raise ValueError("LeafNode must have a value")
        if (self.tag is None):
            return f"{self.value}"
        if (self.tag == "img"):
            return f"<{self.tag}{self.props_to_html() if self.props else ''}>"
        return f"<{self.tag}{self.props_to_html() if self.props else ''}>{self.value}</{self.tag}>"