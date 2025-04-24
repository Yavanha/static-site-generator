from functools import reduce


class HTMLNode():
    def __init__(self, tag, value=None, children=None, props=None):
        if value != None and children != None:
            raise ValueError(
                'HTMLNode: has either a value or children can have both')
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props == None:
            return ""
        attributes = reduce(lambda acc, key_value: acc +
                            f"{key_value[0]}=\"{key_value[1]}\" ", self.props.items(), "")
        return attributes

    def __repr__(self):
        return f"HtmlNode : tag : {self.tag} value : {self.value} props : {self.props} children : {self.children}"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("All Parent nodes must have a tag")
        if not self.children:
            raise ValueError("All Parent nodes must have children")
        children_string = reduce(
            lambda acc, node: acc + node.to_html(), self.children, "")
        return f"<{self.tag}>{children_string}</{self.tag}>"
