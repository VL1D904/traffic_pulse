set search_path = reference;


create table if not exists cities (
	id serial primary key,
	name varchar(100) unique not null
);

create table if not exists streets (
	id serial primary key,
	city_id int not null references cities(id) on update cascade on delete cascade,
	name varchar(100) not null,
	unique (city_id, name)
);

create type video_status as enum('inactive', 'active', 'pending', 'error', 'completed', 'canceled');

create table if not exists video_sources (
	id serial primary key,
	street_id int not null references streets(id) on delete restrict on update cascade,
	url text not null unique,
	status video_status not null default 'inactive'
);

create table if not exists video_recording (
	id serial,
	video_source_id int not null references video_sources(id) on update cascade on delete restrict,
	recording_at timestamp not null default now(),
	recording_end timestamp default null,
	primary key (id, recording_at),
	check (
		recording_end is null or
		recording_end >= recording_at
	)
) partition by range (recording_at);

create table if not exists tracker_sessions (
	id uuid,
	video_source_id int not null references video_sources(id) on update cascade on delete restrict,
	started_at timestamp not null default now(),
	ended_at timestamp default null,
	primary key (id, started_at),
	check (
		ended_at is null or
		ended_at >= started_at
		)
) partition by range(started_at);

select partman.create_parent(
	p_parent_table := 'reference.video_recording',
	p_control := 'recording_at',
	p_interval := '1 week',
	p_premake := 4,
	p_default_table := true,
	p_automatic_maintenance := 'on',
	p_jobmon := true
);

select partman.create_parent(
	p_parent_table := 'reference.tracker_sessions',
	p_control := 'started_at',
	p_interval := '1 week',
	p_premake := 4,
	p_default_table := true,
	p_automatic_maintenance := 'on',
	p_jobmon := true
);