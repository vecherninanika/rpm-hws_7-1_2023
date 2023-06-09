env_consts = {
    'ADDRESS': '127.0.0.1',
    'PORT': 8001,
    'DISCONNECT': '/disconnect',
    'ENCODING': 'utf-8',
    'AUTH_OK': 'Auth OK!',
    'SHUTDOWN': '/shutdown',
    'HELP': '/help',
    'LIST': '/list',
    'WHISPER': '/whisper',
    'PG_USER': 'app',
    'PG_PASSWORD': 'change_me',
    'PG_HOST': '127.0.0.1',
    'PG_PORT': 5656,
    'PG_DBNAME': 'chat',
    'SELECTOR_NAMES': "SELECT * FROM banned WHERE name='{0}'",
    'MESSAGES_FROM_DB': 'SELECT username, message FROM messages',
    'ADD_MESSAGES': "INSERT INTO messages (username, message) values ('{0}', '{1}')"
}


def setup_env():
    lines = [f'{const}={value}\n' for const, value in env_consts.items()]
    with open('.env', 'w') as env_file:
        env_file.writelines(lines)


if __name__ == '__main__':
    setup_env()
