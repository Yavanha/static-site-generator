import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html(self):
        node = HTMLNode(
            "div",
            children=[HTMLNode("p", value="this a text")],
            props={"dir": "ltr", "style": "display: block;"},
        )
        self.assertEqual(node.props_to_html(),
                         'dir="ltr" style="display: block;" ')

    def test_print(self):
        node = HTMLNode(
            "div",
            children=[HTMLNode("p", value="this a text")],
            props={"dir": "ltr", "style": "display: block;"},
        )
        node_str = "HtmlNode : tag : div value : None props : {'dir': 'ltr', 'style': 'display: block;'} children : [HtmlNode : tag : p value : this a text props : None children : None]"
        self.assertEqual(node_str, node.__repr__())

    def test_raise_value_error(self):
        with self.assertRaises(ValueError):
            HTMLNode(
                "div",
                value="this is a value",
                children=[HTMLNode("p", value="this a text")],
                props={"dir": "ltr", "style": "display: block;"},
            )

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(tag=None, value="Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),
                         "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":

    unittest.main()
