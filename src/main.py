

from blocktype import extract_title
from helper import copy_files, copy_from_static_to_public, generate_page, generate_pages_recursive
PUBLIC_FOLDER = "public"
STATIC_FOLDER_PATH = "src/static"


def main():
    copy_from_static_to_public()
    generate_pages_recursive("content",
                             "template.html", "public")


main()
