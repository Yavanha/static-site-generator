

from blocktype import extract_title
from helper import copy_files, copy_from_static_to_public, generate_page
PUBLIC_FOLDER = "public"
STATIC_FOLDER_PATH = "src/static"


def main():
    copy_from_static_to_public()
    generate_page("src/content/index.md",
                  "template.html", "public/index.html")


main()
