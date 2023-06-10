#!/bin/bash

# set env variables
python3.10 tests/setup_env.py

# set up database
python3.10 tests/setup_db.py

# server start
echo "Starting the server"
cd hw1_http_server/
python3.10 main.py &

# real tests
sleep 2

OK=200
CREATED=201

token=a1b2c3d4-a1b2-c3d4-e5f6-a1b2c3a1b2c3
function check_code () {
    if [[ $1 -eq $2 ]]
    then
        echo "OK"
    else
        echo "FAILED, CODE: $1"
        exit 1
    fi
}

echo "simple_GET request:"

get_code=`curl -s -o /dev/null \
    -X GET \
    -w %{http_code} \
    http://127.0.0.1:8001/examples`

check_code $get_code $OK

echo "POST request:"

post_code=`curl -s -o /dev/null \
    -X POST \
    -d '{"name": "a1b2c3d4", "age": 1}' \
    -H "Authorization:admin $token"\
    -w %{http_code} \
    http://127.0.0.1:8001/examples`

check_code $post_code $CREATED

 
echo "query_GET request:"

get_code=`curl -s -o /dev/null \
    -X GET \
    -w %{http_code} \
    http://127.0.0.1:8001/examples?name=a1ba1b2c3d42c3d4`

check_code $get_code $OK

echo "DELETE request:"

post_code=`curl -s -o /dev/null \
    -X DELETE \
    -H "Authorization:admin $token"\
    -w %{http_code} \
    http://127.0.0.1:8001/examples?name=a1b2c3d4`

check_code $post_code $OK
