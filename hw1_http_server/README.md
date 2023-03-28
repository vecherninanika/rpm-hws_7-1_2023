# run:
- python3 main.py

# docker for postgresql and installation of some modules:

- chmod +x ./init_commands.sh
- ./init_commands.sh

# .env:

- run setup_env.py to create .env file

# examples of requests in Postman: 

- In Headers: key - "Authorization", value - "admin e71da913-37d1-4739-a48d-a6bd1e15b250" (without quotation marks)
- GET: 127.0.0.1:8001/examples
- POST: 127.0.0.1:8001/examples
-       In body, raw: {"name": "Lera"}
- PUT: 127.0.0.1:8001/examples?age=25
-       In body, raw: {"name": "Lera"}
-       (if you want to change name where age is 25)
- DELETE: 127.0.0.1:8001/examples?name=Lera
