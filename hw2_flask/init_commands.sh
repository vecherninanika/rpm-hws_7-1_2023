#!/bin/bash

python3.10 -m venv ./venv
sleep 1
. ./venv/bin/activate

pip install -r requirements.txt

docker run -d --name chat_multiclient \
-p 5656:5432 \
-e POSTGRES_USER=app \
-e POSTGRES_PASSWORD=change_me \
-e POSTGRES_DB=chat \
postgres

sleep 2

export PGPASSWORD=change_me
psql -h 127.0.0.1 -p 5656 -U app chat -f setup_db.ddl
