import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from helper import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link


class TestTextNode(unittest.TestCase):

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_print(self):
        node = TextNode("This is a text node", TextType.BOLD)
        str = "TextNode(This is a text node, bold, None)"
        self.assertEqual(str, node.__repr__())

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is some anchor text",
                         TextType.LINK, "https://www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_split_bold(self):
        node = TextNode(
            "This is text with a **bolded phrase** in the middle", TextType.TEXT)
        splited_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(splited_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT),
        ])

    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        splited_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(splited_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

    def test_split_italic(self):
        node = TextNode(
            "This is text with a _italic words_ word", TextType.TEXT)
        splited_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(splited_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic words", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ])

    def test_split_no_split(self):
        node = TextNode(
            "italic words", TextType.ITALIC)
        splited_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(splited_nodes, [
            TextNode("italic words", TextType.ITALIC),
        ])

    def test_split_raise_error(self):
        with self.assertRaises(ValueError):
            node = TextNode(
                "This is text with a _italic words_ word _second italic", TextType.TEXT)
            split_nodes_delimiter([node], '_', TextType.ITALIC)

    def test_split_no_space(self):
        node = TextNode(
            "This is text with a**bolded phrase**in the middle", TextType.TEXT)
        splited_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(splited_nodes, [
            TextNode("This is text with a", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode("in the middle", TextType.TEXT),
        ])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"

        matches = extract_markdown_links(text)
        self.assertListEqual(
            [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_markdown_no_images(self):
        matches = extract_markdown_images(
            "This is text with an"
        )
        self.assertListEqual(
            [], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_no_matches_images(self):
        node = TextNode(
            "This is text with a link",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link", TextType.TEXT),

            ],
            new_nodes,
        )

    def test_split_no_matches_links(self):
        node = TextNode(
            "This is text with a link",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link", TextType.TEXT),

            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
