from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import pathlib
import json
import mimetypes
import urllib.parse
from threading import Thread
import socket
import logging


MAIN_DIR = pathlib.Path("front-init")
DIR_WITH_DATA = MAIN_DIR / "storage"
FILE_WITH_DATA = "data.json"
HOST_IP = "127.0.0.1"
UDP_PORT = 5000
BUFFER = 10240


class CustomHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        body = self.rfile.read(int(self.headers["Content-Length"]))
        self._send_to_server(body)
        self.send_response(302)
        self.send_header("Location", "/index.html")
        self.end_headers()

    def do_GET(self):
        route = urllib.parse.urlparse(self.path)
        match route.path:
            case "/":
                self.send_html("index.html")
            case "/message":
                self.send_html("message.html")
            case _:
                file = MAIN_DIR / route.path[1:]
                print(file)
                if file.exists():
                    self.send_static(file)
                else:
                    self.send_html("error.html", 404)

    def send_html(self, filename, status_code=200):
        self.send_response(status_code)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        print(filename)
        with open(MAIN_DIR / filename, "rb") as main_file:
            self.wfile.write(main_file.read())

    def send_static(self, filename):
        self.send_response(200)
        mime_type, *rest = mimetypes.guess_type(filename)
        if mime_type:
            self.send_header("Content-Type", mime_type)
        else:
            self.send_header("Content-Type", "text/plain")
        self.end_headers()
        with open(filename, "rb") as main_file:
            self.wfile.write(main_file.read())

    @staticmethod
    def _send_to_server(data):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.sendto(data, (HOST_IP, UDP_PORT))
        client_socket.close()


def run_http_server(server=HTTPServer, handler=CustomHTTPRequestHandler):
    address = ("0.0.0.0", 3000)
    http = server(address, handler)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


def run_socket_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = HOST_IP, UDP_PORT
    server_socket.bind(server)
    try:
        while True:
            data, _ = server_socket.recvfrom(BUFFER)
            save_jo_json(DIR_WITH_DATA, data)
            if not data:
                break
    except KeyboardInterrupt:
        logging.debug(f"Socket server stopped!")
    finally:
        server_socket.close()


def save_jo_json(path, msg):
    data = urllib.parse.unquote_plus(msg.decode())
    list_with_values = [el.split("=") for el in data.split("&")]
    data = {key: value for key, value in list_with_values}
    data_json = {}
    try:
        with open(path / FILE_WITH_DATA, "r") as fh:
            data_json = json.load(fh)
    except ValueError:
        logging.debug(f"Failed parse data")
    except FileNotFoundError:
        logging.debug(f"Read file not found")

    now = datetime.now()
    date_string = now.strftime("%d-%m-%Y %H:%M:%S")
    data_json[date_string] = data
    print(date_string)
    if not path.exists():
        path.mkdir()
    with open(path / FILE_WITH_DATA, "w", encoding="utf-8") as fd:
        json.dump(data_json, fd, ensure_ascii=False)


def main():
    thread_for_http_server = Thread(target=run_http_server)
    thread_for_http_server.start()

    thread_for_socket_server = Thread(target=run_socket_server)
    thread_for_socket_server.start()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(message)s")
    STORAGE_DIR = pathlib.Path().joinpath("data")
    FILE_STORAGE = STORAGE_DIR / "data.json"
    if not FILE_STORAGE.exists():
        with open(FILE_STORAGE, "w", encoding="utf-8") as fd:
            json.dump({}, fd, ensure_ascii=False)

    main()
