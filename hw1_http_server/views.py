"""Read and fill html-documents."""
from config import *


def list_to_view(iterable: list) -> str:
    return ''.join([f'<ul>{item}</ul>' for item in iterable]) if iterable else '<p>No data given.</p>'


def predictage_html(predictage_data) -> str:
    with open(PREDICTAGE_TEMPLATE, 'r') as file:
        return file.read().format(**predictage_data)


def examples_html(examples_data) -> str:
    with open(EXAMPLES_TEMPLATE, 'r') as file:
        return file.read().format(**examples_data)


def mainpage_html() -> str:
    with open(MAIN_PAGE, 'r') as file:
        return file.read()


def errorpage_html(error: str) -> str:
    with open(ERROR_PAGE, 'r') as file:
        return file.read().format(error=error)
