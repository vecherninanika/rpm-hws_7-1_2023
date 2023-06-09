create extension "uuid-ossp";

create table banned (id uuid primary key default uuid_generate_v4(),
                     name text not null);

insert into banned (name) values ('Maxeem'), ('Nika');

create table messages (username text not null,
                       message text not null);
