# server host and port
HOST = '127.0.0.1'
PORT = 8001

# pages
PREDICTAGE = '/predictage'
EXAMPLES = '/examples'

# templates paths
TEMPLATES = 'templates/'
MAIN_PAGE = f'{TEMPLATES}mainpage.html'
PREDICTAGE_TEMPLATE = f'{TEMPLATES}predictage.html'
EXAMPLES_TEMPLATE = f'{TEMPLATES}examples.html'
ERROR_PAGE = f'{TEMPLATES}error.html'

# HTTP headers
CONTENT_LENGTH = 'Content-Length'
CONTENT_TYPE = 'Content-Type', 'text/html'
AUTH = 'Authorization'

# HTTP server error codes
NOT_FOUND = 404
FORBIDDEN = 403
BAD_REQUEST = 400

# HTTP OK codes
OK = 200
CREATED = 201
NO_CONTENT = 204

# other HTTP codes
NOT_IMPLEMENTED = 501

# db requests
SELECTOR = 'SELECT * FROM examples'
GET_TOKEN = 'SELECT token FROM token WHERE username=\'{username}\''
INSERT = 'INSERT INTO examples ({keys}) VALUES ({values})'
UPDATE = 'UPDATE examples SET {request}'
DELETE = 'DELETE FROM examples '
EXAMPLES_ATTRS = ['name', 'age']
EXAMPLES_REQ_ATTRS = ['name']
PREDICTAGE_ATTRS = ['name']

# page str to byte coding
CODING = 'KOI8-R'

# URL of my API
AGIFY_API_URL = 'https://api.agify.io'
