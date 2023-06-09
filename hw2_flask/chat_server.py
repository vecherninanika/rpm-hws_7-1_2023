from socket import socket
from dotenv import load_dotenv
from os import getenv
from threading import Thread, Lock
from types import SimpleNamespace
from psycopg2 import connect

consts = SimpleNamespace()
load_dotenv()

consts.ADDRESS = getenv('ADDRESS')
consts.DISCONNECT = getenv('DISCONNECT')
consts.ENCODING = getenv('ENCODING')
consts.AUTH_OK = getenv('AUTH_OK')
consts.SHUTDOWN: str = getenv('SHUTDOWN', default='/shutdown')
PG_USER = getenv('PG_USER')
PG_PASSWORD = getenv('PG_PASSWORD')
PG_HOST = getenv('PG_HOST')
PG_PORT = getenv('PG_PORT')
PG_DBNAME = getenv('PG_DBNAME')
SELECTOR_NAMES = getenv('SELECTOR_NAMES')
ADD_MESSAGES = getenv('ADD_MESSAGES')
try:
    consts.PORT = int(getenv('PORT'))
except Exception as error:
    print(f'Error occured while loading PORT: {error}, defaults to 8001')
    consts.PORT = 8001


def encode(text: str, coding=consts.ENCODING) -> bytes:
    return text.encode(coding)


def decode(msg: bytes, coding=consts.ENCODING) -> str:
    return msg.decode(coding)


def send_all(message: str):
    with users_lock:
        for user in users.values():
            user.send(encode(message))
            user.close()


def normal_msg(msg: str, name: str):
    global users, users_lock, db_cursor, connection
    with users_lock:
        if name not in users.keys():
            return True
        db_cursor.execute(ADD_MESSAGES.format(name, msg))
        connection.commit()


def parse_msg(msg: str, name: str, client: socket) -> bool:
    global users, users_lock
    match msg:
        case str(consts.DISCONNECT):
            client.send(encode(consts.DISCONNECT))
            client.close()
            print('client.close()')
            with users_lock:
                if name in users.keys():
                    del users[name]
            return False
        case _:
            normal_msg(msg, name, client)
    return True


def receiver(client: socket, name: str):
    while True:
        msg = decode(client.recv(1024))
        if not parse_msg(msg, name, client):
            break


def is_banned(name):
    global db_cursor
    request = SELECTOR_NAMES.format(name)
    db_cursor.execute(request)
    return bool(db_cursor.fetchall())


def new_client(client: socket, cl_address: tuple) -> str:
    global users, users_lock
    while True:
        name = decode(client.recv(1024))
        if name:
            if not parse_msg(name, str(cl_address), client):
                return
            with users_lock:
                if name in users.keys():
                    client.send(encode('Username is taken'))
                elif is_banned(name):
                    client.send(encode('You were permanently banned for a while'))
                    client.close()
                    return
                else:
                    client.send(encode(consts.AUTH_OK))
                    print(f'Client {cl_address} authenticated by name {name}')
                    users[name] = client
                    Thread(target=receiver, args=(client, name)).start()
                    return


def accept_client(server: socket):
    while True:
        client, cl_address = server.accept()
        print(f'Client connected from {cl_address}')
        Thread(target=new_client, args=(client, cl_address), daemon=True).start()


def main(server: socket) -> None:
    server.bind((consts.ADDRESS, consts.PORT))
    server.listen()
    Thread(target=accept_client, args=(server,), daemon=True).start()
    while True:
        match input():
            case str(consts.SHUTDOWN):
                print('Shutdown!')
                send_all(consts.DISCONNECT)
                break


if __name__ == '__main__':
    users: dict = {}
    users_lock = Lock()
    server = socket()
    connection = connect(
        dbname=PG_DBNAME, host=PG_HOST, port=PG_PORT, user=PG_USER, password=PG_PASSWORD
    )
    db_cursor = connection.cursor()
    try:
        main(server)
    except KeyboardInterrupt:
        print('Goodbye!')
    except BrokenPipeError as error:
        print(f'Server shut down due to {error.strerror}')
    finally:
        server.close()
        db_cursor.close()
        connection.close()
