from typing import List

class HTMLNode():
    def __init__(self, tag = None, value = None, children: List["HTMLNode"] = None, props: dict = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
    def to_html(self) -> str:
        raise NotImplementedError
    def props_to_html(self) -> str:
        # return "".join(list(map(lambda items: f' {items[0]}="{items[1]}"', self.props.items())))
        return "".join([f' {key}="{value}"' for key, value in self.props.items()])
    