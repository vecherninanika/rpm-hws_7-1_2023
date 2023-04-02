# run:
- python3 main.py

# docker for postgresql and installation of some modules:

- chmod +x ./init_commands.sh
- ./init_commands.sh

# .env:

- run setup_env.py to create .env file

# examples of requests in Postman: 

In Headers: key - "Authorization", value - "admin a1b2c3d4-a1b2-c3d4-e5f6-a1b2c3a1b2c3" (without quotation marks)

**GET:**
- 127.0.0.1:8001/examples

**POST:**
- 127.0.0.1:8001/examples
- In body, raw: {"name": "Lera"}

**PUT:**
- 127.0.0.1:8001/examples?age=25
- In body, raw: {"name": "Lera"}
- *(if you want to change name where age is 25)*

**DELETE:**
- 127.0.0.1:8001/examples?name=Lera
