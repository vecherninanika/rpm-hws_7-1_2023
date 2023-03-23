#!/bin/bash

pip install -r requirements/requirements.txt

docker run -d --name names_hw1 -p 5432:5432 \
 -v $HOME/DATABASES/names_hw1:/var/lib/postresql/names_hw1 \
 -e POSTGRES_PASSWORD=change_me \
 -e POSTGRES_USER=sirius_2023 \
 -e POSTGRES_DB=names_hw1 \
 postgres

sleep 2

psql -h 127.0.0.1 -p 5432 -U sirius_2023 -d names_hw1 -f init_commands.ddl
