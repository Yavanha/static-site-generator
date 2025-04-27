from enum import Enum
import re


HEADING_PATTERN = r"^#{1,6}\s{1}"
HEADING_1_PATTERN = r"^#{1}\s{1}(.*)"
CODE_PATTERN = r"^`{3}.*`{3}$"
QUOTE_PATTERN = r"^>.*"
UNORDERED_LIST_PATTERN = r"^-.*"
ORDERED_LIST_PATTERN = r"^\d{1}\..*"


class BlockType(Enum):

    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    if re.search(HEADING_PATTERN, block):
        return BlockType.HEADING
    elif re.search(CODE_PATTERN, block, re.DOTALL):
        return BlockType.CODE
    elif re.search(QUOTE_PATTERN, block):
        return BlockType.QUOTE
    elif re.search(UNORDERED_LIST_PATTERN, block):
        return BlockType.UNORDERED_LIST
    elif re.search(ORDERED_LIST_PATTERN, block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def extract_title(markdown):
    blocks = markdown.strip("\n").split('\n\n')
    while (len(blocks)):
        match = re.findall(HEADING_1_PATTERN, blocks.pop(0))
        if not match:
            raise Exception('the document must have a header')
        return match[0]
