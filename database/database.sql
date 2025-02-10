CREATE DATABASE IF NOT EXISTS urls_database;

USE urls_database;

CREATE TABLE users(
id int auto_increment primary key,
username varchar(255),
password varchar(255),
is_active boolean,
created_at datetime
);

create table urls(
id int auto_increment primary key,
user_id int,
link varchar(255),
shortened_link varchar(255),
foreign key (user_id) references users(id)
);