DROP TABLE IF EXISTS sqlite_master;
DROP TABLE IF EXISTS sqlite_sequence;
DROP TABLE IF EXISTS twitter;

CREATE TABLE sqlite_master
(
    type text,
    name text,
    tbl_name text,
    rootpage integer,
    sql text
);
CREATE TABLE sqlite_sequence
(
    name ,
    seq
);
CREATE TABLE twitter
(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    token_access STRING NOT NULL,
    token_access_secret STRING NOT NULL
);
CREATE UNIQUE INDEX twitter_token_access_uindex ON twitter (token_access);
CREATE UNIQUE INDEX twitter_token_access_secret_uindex ON twitter (token_access_secret);
CREATE TABLE users
(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    pseudo STRING NOT NULL,
    password STRING NOT NULL
);
CREATE UNIQUE INDEX users_pseudo_uindex ON users (pseudo);
CREATE UNIQUE INDEX users_password_uindex ON users (password)