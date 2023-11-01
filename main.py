import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs


_routes = {}


def route(method, path):
    def decorator(func):
        _routes[f'{method}_{path}'] = func

        def inner(*args, **kwargs):
            return func(*args, **kwargs)

        return inner

    return decorator


class MyHandler(BaseHTTPRequestHandler):
    """ Класс, отвечает за обработку входящих запросов от клиентов """

    def do_GET(self):
        """ Метод для обработки входящих GET-запросов """

        url = urlparse(self.path)
        args = parse_qs(url.query)

        key = f'GET_{url.path}'

        if key not in _routes:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(http_response('404.html'))
            return

        method = _routes[key](self, args)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(method)

    @route('GET', '/')
    def index(self, *args, **kwargs) -> bytes:
        return http_response('index.html')

    @route('GET', '/categories')
    def categories(self, *args, **kwargs) -> bytes:
        return http_response('categories.html')

    @route('GET', '/orders')
    def orders(self, *args, **kwargs) -> bytes:
        return http_response('orders.html')

    @route('GET', '/contacts')
    def contacts(self, *args, **kwargs) -> bytes:
        return http_response('contacts.html')


def http_response(html_name: str) -> bytes:
    """ Функция для создания ответа """

    path_to_file = os.path.join(os.path.dirname(__file__), 'static', html_name)
    with open(path_to_file, 'r', encoding='utf-8') as html:
        return html.read().encode()


def run_server():
    """ Запустить сервер """

    host_name = "localhost"
    server_port = 8080
    web_server = HTTPServer((host_name, server_port), MyHandler)
    print(f'Server started http://{host_name}:{server_port}')

    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        web_server.server_close()
        print('Server stopped.')


if __name__ == '__main__':
    run_server()
