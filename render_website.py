import argparse
import json
import os
import math
from pathlib import Path
from urllib.request import pathname2url

from more_itertools import chunked
from pathvalidate import sanitize_filepath
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server

BOOK_CARDS_PER_PAGE = 10


def on_reload(json_file_path=None):
    if not json_file_path:
        json_file_path = 'book_info.json'
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    with open(json_file_path, "r") as file:
        book_descriptions = json.load(file)
    for book_description in book_descriptions:
        book_description['book_url'] = pathname2url(book_description['book_path'])
    chunked_book_descriptions = chunked(book_descriptions, BOOK_CARDS_PER_PAGE)
    page_count = math.ceil(len(book_descriptions)/BOOK_CARDS_PER_PAGE)
    template = env.get_template('template.html')
    for page_num, book_cards in enumerate(chunked_book_descriptions, start=1):
        rendered_page = template.render(
            books=book_cards,
            page_count=page_count,
            active_page=page_num
        )
        with open(Path('pages', f'index{"" if page_num == 1 else page_num}.html'), 'w', encoding='utf8') as file:
            file.write(rendered_page)


def main():
    parser = argparse.ArgumentParser(
        description='Render on-line library site'
    )
    parser.add_argument('-jf', '--json_file', type=str,
                        help='Путь к *.json файлу с данными книг', default='book_info.json')
    json_file_path = sanitize_filepath(parser.parse_args().json_file)
    os.makedirs('pages', exist_ok=True)
    on_reload(json_file_path)
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.', default_filename='pages/index.html')


if __name__ == '__main__':
    main()