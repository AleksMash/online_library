import json
from http.server import HTTPServer, SimpleHTTPRequestHandler

from more_itertools import chunked
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server


def on_reload():
    with open("book_info.json", "r") as file:
        books_json = file.read()
    books = json.loads(books_json)
    books_chunked = chunked(books, 2)
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')
    rendered_page = template.render(books=books_chunked)
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def main():
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    # server = HTTPServer(('127.0.0.1', 8000), SimpleHTTPRequestHandler)
    # server.serve_forever()
    server.serve(root='.')


if __name__ == '__main__':
    main()