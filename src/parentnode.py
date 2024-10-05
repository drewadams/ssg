from src.htmlnode import HTMLNode
from typing import List

class ParentNode(HTMLNode):
    def __init__(self, tag = None, value = None, children: List[HTMLNode] = None, props: dict = None) -> None:
        super().__init__(tag, value, children, props)

    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self) -> str:
        # Ensure that the ParentNode has a tag and children
        if (self.tag is None):
            raise ValueError("ParentNode must have a tag")
        if (self.children is None):
            # print(self.tag, self.value, self.props)
            raise ValueError("ParentNode must have children")
        # Loop through children and call to_html on each one
        try:
            return f"<{self.tag}{self.props_to_html()}>{''.join([child.to_html() for child in self.children])}</{self.tag}>"
        except Exception as e:
            # print(e)
            # print(self.tag, self.value, self.props)
            # print(self.children)
            for child in self.children:
                if isinstance(child, List):
                    print(child)
            raise e