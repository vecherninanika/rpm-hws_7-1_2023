from chat_server import decode, encode
from dotenv import load_dotenv
from os import getenv


load_dotenv()
DISCONNECT = getenv('DISCONNECT')
AUTH_OK = getenv('AUTH_OK')
ADDRESS = getenv('ADDRESS')
PORT = getenv('PORT')


def auth(name, client) -> bool:
    client.connect((ADDRESS, int(PORT)))
    client.send(encode(name))
    answer = decode(client.recv(1024))
    if answer == AUTH_OK:
        return False
    else:
        client.close()
    return answer


def main(message, client) -> None:
    client.send(encode(message))
    if message == DISCONNECT:
        client.close()
