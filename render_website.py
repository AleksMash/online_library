import json
import os
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler

from more_itertools import chunked
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server


def on_reload():

    with open("book_info.json", "r") as file:
        books_json = file.read()
    books = json.loads(books_json)
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    book_pages = chunked(books, 10)
    for page_num, book_page in enumerate(book_pages):
        book_rows = chunked(book_page, 2)
        template = env.get_template('template.html')
        rendered_page = template.render(book_rows=book_rows)
        with open(Path('pages', f'index{page_num+1}.html'), 'w', encoding="utf8") as file:
            file.write(rendered_page)


def main():
    os.makedirs('pages', exist_ok=True)
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    # server = HTTPServer(('127.0.0.1', 8000), SimpleHTTPRequestHandler)
    # server.serve_forever()
    server.serve(root='.', default_filename='pages/index1.html')


if __name__ == '__main__':
    main()