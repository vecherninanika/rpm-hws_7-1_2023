"""Start the server."""
from http.server import HTTPServer
from http_server import CustomHandler
from config import HOST, PORT

# starting the server
if __name__ == '__main__':
    with HTTPServer((HOST, PORT), CustomHandler) as server:
        server.serve_forever()
