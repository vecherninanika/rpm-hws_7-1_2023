CREATE EXTENSION "uuid-ossp";

CREATE TABLE IF NOT EXISTS token (username text primary key, token uuid);

CREATE TABLE examples (id uuid primary key default uuid_generate_v4(),
                       name text not null,
                       age int);

INSERT INTO token VALUES ('admin', 'a1b2c3d4-a1b2-c3d4-e5f6-a1b2c3a1b2c3');
