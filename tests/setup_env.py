env_consts = {
    'PG_HOST': '127.0.0.1',
    'PG_PORT': '5432',
    'PG_USER': 'test',
    'PG_PASSWORD': 'test',
    'PG_DBNAME': 'test'
}


def setup_env():
    lines = [f'{const}={value}\n' for const, value in env_consts.items()]
    with open('.env', 'w') as env_file:
        env_file.writelines(lines)


if __name__ == '__main__':
    setup_env()
