from flask import Flask, render_template, request, redirect, url_for, session
import chat_client
from config import *
from dotenv import load_dotenv
from os import getenv
from psycopg2 import connect
from time import sleep
from threading import Thread
from socket import socket


load_dotenv()
DISCONNECT = getenv('DISCONNECT')
PG_USER = getenv('PG_USER')
PG_PASSWORD = getenv('PG_PASSWORD')
PG_HOST = getenv('PG_HOST')
PG_PORT = getenv('PG_PORT')
PG_DBNAME = getenv('PG_DBNAME')
MESSAGES_FROM_DB = getenv('MESSAGES_FROM_DB')
FLASK_PORT = getenv('FLASK_PORT')
FLASK_ADDRESS = getenv('FLASK_ADDRESS')
app = Flask(__name__)
app.secret_key = SECRET_KEY
clients = {}


@app.route("/", methods=['GET', 'POST'])
def mainpage():
    if request.method == 'POST':
        if request.form['username']:
            session['username'] = request.form['username']
            session_user = session['username']
            clients[session_user] = socket()
            answer = chat_client.auth(
                session['username'], clients[session_user]
            )
            if not answer:
                return redirect(url_for('chat'))
        else:
            answer = 'Username cannot be empty'
            return render_template(MAINPAGE_HTML, message=answer)
    return render_template(MAINPAGE_HTML)


@app.route('/logout')
def logout():
    global clients
    session.pop('username', None)
    clients.pop(session['username'])
    return redirect(url_for('index'))


@app.route("/chat", methods=['GET', 'POST'])
def chat():
    client = session.get('username')
    if client:
        print(client)
        if request.method == 'POST':
            message = request.form['message']
            if message == DISCONNECT:
                return redirect(url_for('logout'))
            if message:
                client_socket = clients.get(client)
                if client_socket:
                    Thread(target=chat_client.main, args=(message, client_socket)).start()
                else:
                    print('No client socket')
                    return redirect(url_for('mainpage'))
        connection = connect(
            dbname=PG_DBNAME, host=PG_HOST, port=PG_PORT, user=PG_USER, password=PG_PASSWORD
        )
        cursor = connection.cursor()
        sleep(1)
        cursor.execute(MESSAGES_FROM_DB)
        all_messages = []
        for user, message in cursor.fetchall():
            all_messages.append((user, message))
        return render_template(CHAT_HTML, messages=all_messages)
    return redirect(url_for('register'))


if __name__ == '__main__':
    app.run(host=FLASK_ADDRESS, port=FLASK_PORT)
