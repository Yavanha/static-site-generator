from blocktype import BlockType, block_to_block_type, extract_title
from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
import re
from functools import reduce
import os
import shutil
from pathlib import Path

PUBLIC_FOLDER = "public"
STATIC_FOLDER_PATH = "src/static"


def generate_pages_recursive(base_path, dir_path_content, template_path, dest_dir_path):
    files = os.listdir(dir_path_content)
    print(files)
    for file in files:
        file_path = os.path.join(dir_path_content, file)
        if os.path.isdir(file_path):
            next_dest_dir_path = os.path.join(dest_dir_path, file)
            os.mkdir(os.path.join(base_path, next_dest_dir_path))
            generate_pages_recursive(base_path,
                                     file_path, template_path, next_dest_dir_path)
        if Path(file_path).suffix.lower() in {".md", ".markdown"}:
            next_dest_file_path = os.path.join(dest_dir_path, "index.html")
            generate_page(base_path, file_path,
                          template_path, next_dest_file_path)


def generate_page(base_path, from_path, template_path, dest_path):
    print(
        f"Generating page from {from_path} to dest_path using {template_path}")
    from_content = read_file(os.path.join(base_path, from_path))
    template_content = read_file(os.path.join(base_path, template_path))
    html_content = markdown_to_html_node(from_content).to_html()
    title = extract_title(from_content)
    final_content = template_content.replace(
        "{{ Title }}", title).replace("{{ Content }}", html_content)

    write_file(os.path.join(base_path, dest_path),
               os.path.join(base_path, final_content))


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    return content


def write_file(path, content):
    with open(path, "w") as file:
        file.write(content)


def copy_files(source, destination, files):
    if len(files) == 0:
        return
    file_source_path = os.path.join(source, files[0])
    print(f"{file_source_path} to {os.path.join(destination, files[0])}")
    if os.path.isfile(file_source_path):
        shutil.copy(file_source_path, destination)
    if os.path.isdir(file_source_path):
        destination_path = os.path.join(destination, files[0])
        os.mkdir(destination_path)
        copy_files(file_source_path, destination_path,
                   os.listdir(file_source_path))

    copy_files(source, destination, files[1:])


def copy_from_static_to_public(source, dest):

    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)
    listdir = os.listdir(source)
    copy_files(source, dest, listdir)

    # this is an exercice i just wanted to learn python
    # this code need hudge refactoring


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    child_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                stripped_block = block.replace("\n", " ").lstrip("# ")
                text_nodes = text_to_textnodes(stripped_block)
                html_nodes = list(map(text_node_to_html_node, text_nodes))
                child_nodes.append(ParentNode("h1", html_nodes))
            case BlockType.CODE:

                html_node = text_node_to_html_node(
                    TextNode(block.strip("` ").lstrip('\n'), TextType.CODE))
                child_nodes.append(ParentNode("pre", [html_node]))
            case BlockType.QUOTE:
                stripped_block = block.replace("\n>", " ").lstrip("> ")
                text_nodes = text_to_textnodes(stripped_block)
                html_nodes = list(map(text_node_to_html_node, text_nodes))
                child_nodes.append(ParentNode(
                    "blockquote", html_nodes))
            case BlockType.UNORDERED_LIST:
                items = block.split("\n")
                list_item = []
                for item in items:
                    text_nodes = text_to_textnodes(item.lstrip('- '))
                    html_nodes = list(map(text_node_to_html_node, text_nodes))
                    list_item.append(ParentNode("li", html_nodes))
                child_nodes.append(ParentNode("ul", list_item))
            case BlockType.ORDERED_LIST:
                items = block.split("\n")
                list_item = []
                for item in items:
                    text_nodes = text_to_textnodes(item[3:])
                    print()
                    print(text_nodes)
                    print()
                    html_nodes = list(map(text_node_to_html_node, text_nodes))
                    list_item.append(ParentNode("li", html_nodes))
                child_nodes.append(ParentNode("ol", list_item))
            case BlockType.PARAGRAPH:
                text_nodes = text_to_textnodes(block.replace("\n", " "))
                html_nodes = list(map(text_node_to_html_node, text_nodes))
                child_nodes.append(ParentNode("p", html_nodes))
            case _:
                raise Exception(
                    f"Unsupported markdown block type '{block_type}' encountered in block: {block[:30]}...")
    parent_node = ParentNode("div", child_nodes)
    return parent_node


def markdown_to_blocks(markdown):
    blocks = []
    for block in markdown.split("\n\n"):
        if not block:
            continue
        blocks.append(block.strip(" \n"))
    return blocks


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes_1 = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes_2 = split_nodes_delimiter(nodes_1, "**", TextType.BOLD)
    nodes_3 = split_nodes_delimiter(nodes_2, "`", TextType.CODE)
    nodes_4 = split_nodes_image(nodes_3)
    nodes_5 = split_nodes_link(nodes_4)
    return nodes_5


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
            matches = extract_markdown_links(node.text)
            if image:
                matches = extract_markdown_images(
                    node.text)
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
                if node_text:
                    new_nodes.append(TextNode(node_text, TextType.TEXT))
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches
