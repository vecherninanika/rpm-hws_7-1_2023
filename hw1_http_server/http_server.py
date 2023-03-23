from http.server import BaseHTTPRequestHandler
from config import *
from views import examples_html, predictage_html, mainpage_html, errorpage_html
from dbhandler import DbHandler
from predictage import predictage
import json

# просто класс с ошибкой:


class InvalidQuery(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        classname = self.__class__.__name__
        return f'\n {classname} Error: {self.msg}\n'


class CustomHandler(BaseHTTPRequestHandler):

    # Вывести страницы:

    def examples_or_predictage(self, query):
        if self.path.startswith(EXAMPLES):
            return examples_html(DbHandler.get_data(query))
        elif self.path.startswith(PREDICTAGE):
            return predictage_html(predictage(query))

    def get_page(self):
        if self.path.startswith((EXAMPLES, PREDICTAGE)):
            try:
                query = self.parse_query()
            except Exception as error:
                return BAD_REQUEST, errorpage_html(error)
            return OK, self.examples_or_predictage(query)
        # else: mainpage
        return OK, mainpage_html()

    def parse_query(self):
        if self.path.startswith(EXAMPLES):
            possible_attrs = EXAMPLES_ATTRS
        elif self.path.startswith(PREDICTAGE):
            possible_attrs = PREDICTAGE_ATTRS
        else:
            possible_attrs = None
        questionmark_place = self.path.find('?')
        if '?' in self.path and questionmark_place != len(self.path) - 1:
            query_data = self.path[questionmark_place + 1:].split('&')
            query_attr_value = [attr_value.split(
                '=') for attr_value in query_data]
            query_dict = {attr: int(value) if value.isdigit(
            ) else value for attr, value in query_attr_value}
            if possible_attrs:
                not_possible = list(
                    filter(lambda x: x not in possible_attrs, query_dict.keys()))
                if not_possible:
                    raise InvalidQuery(
                        f'{__name__} has unknown attributes: {not_possible}')
            return query_dict
        return None

    # GET POST PUT DELETE :

    def respond_to_client(self, http_code: int, msg: str):
        self.send_response(http_code)
        self.send_header(*CONTENT_TYPE)
        self.end_headers()
        self.wfile.write(msg.encode(CODING))

    def get(self):
        self.respond_to_client(*self.get_page())

    def get_request_json(self):
        content_length = int(self.headers.get(CONTENT_LENGTH, 0))
        if content_length:
            return json.loads(self.rfile.read(content_length).decode())
        return {}

    def post(self, request_data=None):
        if self.path.startswith(EXAMPLES):
            request_data = self.get_request_json()
            if not request_data:
                return BAD_REQUEST, f'No request data provided by {self.command}'
            for attr in request_data.keys():
                if attr not in EXAMPLES_ATTRS:
                    return NOT_IMPLEMENTED, f'Examples do not have attribute: {attr}'
            if all([req_attr in request_data for req_attr in EXAMPLES_REQ_ATTRS]):
                return CREATED, f'{self.command} OK' if DbHandler.insert(request_data) else BAD_REQUEST, f'{self.command} FAIL'
            return BAD_REQUEST, f'Required keys to add: {EXAMPLES_REQ_ATTRS}'
        return NO_CONTENT, f'Request data for {self.command} not found'

    def put(self):
        if self.path.startswith(EXAMPLES):
            request_data = self.get_request_json()
            if not request_data:
                return BAD_REQUEST, f'No request data provided by {self.command}'
            query = self.parse_query()
            if query:
                not_possible = list(
                    filter(lambda x: x not in EXAMPLES_ATTRS, query.keys()))
                if not_possible:
                    return NOT_IMPLEMENTED, f'students do not have attributes: {not_possible}'
            try:
                execute_command = DbHandler.update(where=query, data=request_data)
            except Exception as error:
                print(f'{self.command} error: {error}')
                return BAD_REQUEST, f'{self.command} error: {error}'
            if not execute_command:
                return self.post(request_data)
            return OK, f'{self.command} OK'

    def delete(self):
        if self.path.startswith(EXAMPLES):
            query = self.parse_query()
            if not query:
                return BAD_REQUEST, f'{self.command} error: no data provided by query'
            if DbHandler.delete(query):
                return OK, 'Content has been deleted'
        return NOT_FOUND, 'Content not found'

    def authorization(self):
        get_from_headers = self.headers.get(AUTH, '').split()
        if len(get_from_headers) == 2:
            return DbHandler.is_valid_token(get_from_headers[0], get_from_headers[1])
        return False

    def choose_method(self):
        methods = {'POST': self.post,
                   'PUT': self.put,
                   'DELETE': self.delete}
        if self.command == 'GET':
            self.get()
            return
        if self.command in methods.keys():
            func_to_use = methods[self.command]
        else:
            self.respond_to_client(NOT_IMPLEMENTED, 'Unknown method :(')
            return
        if self.authorization():
            self.respond_to_client(*func_to_use())
            return
        self.respond_to_client(FORBIDDEN, 'Authorization failed')

    def do_POST(self):
        self.choose_method()

    def do_PUT(self):
        self.choose_method()

    def do_DELETE(self):
        self.choose_method()

    def do_GET(self):
        self.choose_method()
