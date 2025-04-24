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
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            matches = extract_markdown_images(node.text)
            texts = node.text.split('!')
            i = 0
            for text in texts:
                alt, url = matches[i]
                image = f"[{alt}]({url})"
                if text and image not in text:
                    new_nodes.append(TextNode(text, TextType.TEXT))
                    continue
                if len(image) <= len(text):
                    new_nodes.append(TextNode(alt, TextType.IMAGE, url))
                    i += 1
                    split_text = text.split(")")[1]
                    if split_text:
                        new_nodes.append(TextNode(split_text, TextType.TEXT))
            print(new_nodes)


def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((https:\/\/.*?)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((https:\/\/.*?)\)", text)
    return matches
