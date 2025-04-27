

from sys import argv
from blocktype import extract_title
from helper import copy_files, copy_from_static_to_public, generate_page, generate_pages_recursive
PUBLIC_FOLDER = "docs"
STATIC_FOLDER_PATH = "src/static"


def main():
    base_path = ""
    if len(argv) > 1:
        base_path = argv[1]
    copy_from_static_to_public(
        base_path + STATIC_FOLDER_PATH, base_path + PUBLIC_FOLDER)
    generate_pages_recursive(base_path, "content",
                             "template.html", "docs")


main()
