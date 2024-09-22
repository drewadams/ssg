from src.textnode import TextNode
class MDConverter:
    def __init__(self, md = None):
        self.md = md

    def split_nodes_delimiter(self, old_nodes, delimiter, text_type):
        new_nodes = []
        for node in old_nodes:
            if delimiter in node.text:
                parts = node.text.split(delimiter)
                for i, part in enumerate(parts):
                    if i % 2 == 0 or i == 0:
                        new_nodes.append(TextNode(part, node.text_type))
                    else:
                        new_nodes.append(TextNode(part, text_type))

            else:
                new_nodes.append(node)
        return new_nodes