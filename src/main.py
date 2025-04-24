from textnode import TextNode, TextType
from helper import extract_markdown_links, split_nodes_image, split_nodes_link


def main():

    node = TextNode(
        "This is text with a link",
        TextType.TEXT,
    )

    new_nodes = split_nodes_link([node])

    print(new_nodes)


main()
