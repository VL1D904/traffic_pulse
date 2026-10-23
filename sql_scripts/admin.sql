set search_path = admin;

create table if not exists admins (
	id serial primary key,
	login text not null unique,
	pwd text not null
);