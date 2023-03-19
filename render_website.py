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


def on_reload(json_file_path):
    if not json_file_path:
        json_file_path = 'book_info.json'
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    with open(json_file_path, "r") as file:
        books_json = file.read()
    books = json.loads(books_json)
    for book in books:
        book['book_url'] = pathname2url(book['book_path'])
    book_pages = chunked(books, 10)
    print(type(books))
    page_count = math.ceil(len(books)/10)
    print(page_count)
    for page_num, book_page in enumerate(book_pages):
        book_rows = chunked(book_page, 2)
        template = env.get_template('template.html')
        rendered_page = template.render(
            book_rows=book_rows,
            page_count=page_count,
            active_page=page_num+1
        )
        with open(Path('pages', f'index{"" if not page_num else page_num+1}.html'), 'w', encoding="utf8") as file:
            file.write(rendered_page)


def main():
    parser = argparse.ArgumentParser(
        description="Render on-line library site"
    )
    parser.add_argument("-jf", "--json_file", type=str,
                        help="Путь к *.json файлу с данными книг")
    json_file_path = parser.parse_args().json_file
    if json_file_path:
        json_file_path = sanitize_filepath(json_file_path)
    os.makedirs('pages', exist_ok=True)
    on_reload(json_file_path)
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.', default_filename='pages/index.html')


if __name__ == '__main__':
    main()