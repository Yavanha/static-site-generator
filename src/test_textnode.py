import unittest
from blocktype import BlockType, block_to_block_type, extract_title
from textnode import TextNode, TextType, text_node_to_html_node
from helper import markdown_to_blocks, markdown_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes


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

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual([
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE,
                     "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ], nodes)

    def test_text_to_textnodes_only_text(self):
        text = "This is a text"
        nodes = text_to_textnodes(text)
        self.assertListEqual([TextNode(text, TextType.TEXT)], nodes)

    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_heading(self):
        text = "# heading"
        block_type = block_to_block_type(text)
        self.assertEqual(BlockType.HEADING, block_type)

    def test_block_to_block_type_code(self):
        text = "``` heading ```"
        block_type = block_to_block_type(text)
        self.assertEqual(BlockType.CODE, block_type)

    def test_block_to_block_type_quote(self):
        text = ">this is a quote"
        block_type = block_to_block_type(text)
        self.assertEqual(BlockType.QUOTE, block_type)

    def test_block_to_block_type_unordered_list(self):
        text = "- this is an unordered list"
        block_type = block_to_block_type(text)
        self.assertEqual(BlockType.UNORDERED_LIST, block_type)

    def test_block_to_block_type_ordered_list(self):
        text = ". this is an ordered list"
        block_type = block_to_block_type(text)
        self.assertEqual(BlockType.ORDERED_LIST, block_type)

    def test_block_to_block_type_paragraph(self):
        text = "this is a paragraph"
        block_type = block_to_block_type(text)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_extract_title_raise_exception(self):
        with self.assertRaises(Exception):
            extract_title("Hello")

    def test_extract_title(self):
        title = extract_title("""
# Hello World
Hello 
""")
        self.assertEqual(title, "Hello World")


if __name__ == "__main__":
    unittest.main()
