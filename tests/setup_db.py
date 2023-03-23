"""Set up the database."""
from psycopg2 import connect
from dotenv import load_dotenv
from os import getenv


def main():
    load_dotenv()
    creds = {
        "host": getenv("PG_HOST"),
        "port": getenv("PG_PORT"),
        "dbname": getenv("PG_DBNAME"),
        "user": getenv("PG_USER"),
        "password": getenv("PG_PASSWORD"),
    }

    connection = connect(**creds)
    cursor = connection.cursor()
    with open("tests/db_init.ddl", 'r') as file:
        cursor.execute(file.read())

    connection.commit()
    cursor.close()
    connection.close()


if __name__ == '__main__':
    main()
