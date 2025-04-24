from textnode import TextNode, TextType
import re
WHITE_SPACE = ' '


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            texts = node.text.split(delimiter)
            if len(texts) % 2 == 0:
                raise ValueError(
                    "invalid markdown, formatted section not closed")
            for i in range(len(texts)):
                if texts[i] == '':
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(texts[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(texts[i], text_type))
    return new_nodes


def split_nodes_image(old_nodes):
    return split_nodes_with_url(old_nodes, True)


def split_nodes_link(old_nodes):
    return split_nodes_with_url(old_nodes)


def split_nodes_with_url(old_nodes, image=False):
    new_nodes = []
    prefix = ""
    text_type = TextType.LINK
    if image:
        text_type = TextType.IMAGE
        prefix += "!"

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            matches = extract_markdown_images(
                node.text) if image else extract_markdown_links(node.text)
            if len(matches) == 0:
                new_nodes.append(node)
            else:
                node_text = node.text
                for alt, url in matches:

                    delimiter = prefix + f"[{alt}]({url})"
                    texts = node_text.split(delimiter, 1)
                    if texts[0]:
                        new_nodes.append(TextNode(texts[0], TextType.TEXT))
                    new_nodes.append(TextNode(alt, text_type, url))
                    node_text = texts[-1]
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((https:\/\/.*?)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((https:\/\/.*?)\)", text)
    return matches
