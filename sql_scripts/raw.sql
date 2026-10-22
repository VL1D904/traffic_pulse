set search_path = raw;

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

create type status as enum('inactive', 'active', 'pending', 'error', 'completed', 'canceled');

create table if not exists video_sources (
	id serial primary key,
	title varchar(100) not null unique,
	street_id int not null references streets(id) on delete restrict on update cascade,
	url text not null unique,
	status status not null default 'inactive'
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

create table if not exists logs (
	id bigserial,
	type_log text not null,
	created_at timestamp not null default now(),
	path text not null,
	primary key (id, created_at),
	unique (path, created_at)
) partition by range (created_at);

create table if not exists track_types (
	id serial primary key,
	track_type text not null unique
);

insert into track_types values
(0, 'Пешеход'),
(1, 'Велосипедист'),
(2, 'Автомобиль'),
(3, 'Мотоциклист'),
(5, 'Автобус'),
(7, 'Грузовик')
on conflict do nothing;

create table if not exists tracker_sessions (
	id uuid,
	video_source_id int not null references video_sources(id) on update cascade on delete restrict,
	started_at timestamp not null default now(),
	ended_at timestamp default null,
	model_version text,
	tracker_type text,
	status status default 'inactive',
	primary key (id, started_at),
	check (
		ended_at is null or
		ended_at >= started_at
		)
) partition by range(started_at);

create table if not exists tracked_objects (
	id bigserial,
	tracker_session_id uuid not null,
	track_id int not null,
	track_type_id int not null references track_types(id) on update cascade on delete restrict,
	first_seen_at timestamp not null default now(),
	last_seen_at timestamp default null,
	primary key (id, first_seen_at),
	unique (tracker_session_id, track_id, first_seen_at),
	check (
		last_seen_at is null or
		last_seen_at >= first_seen_at
	)
) partition by range(first_seen_at);

create table if not exists detections (
	id bigserial,
	detection_time timestamp default now(),
	track_id bigint not null,
	x_cord_px float not null,
	y_cord_px float not null,
	x_cord_m float not null,
	y_cord_m float not null,
	confidence float not null,
	frame_count int not null,
	primary key (id, detection_time)
) partition by range(detection_time);

select partman.create_parent(
	p_parent_table := 'raw.video_recording',
	p_control := 'recording_at',
	p_interval := '1 week',
	p_premake := 4,
	p_default_table := true,
	p_automatic_maintenance := 'on',
	p_jobmon := true
);

select partman.create_parent(
	p_parent_table := 'raw.logs',
	p_control := 'created_at',
	p_interval := '1 week',
	p_premake := 4,
	p_default_table := true,
	p_automatic_maintenance := 'on',
	p_jobmon := true
);

select partman.create_parent(
	p_parent_table := 'raw.tracker_sessions',
	p_control := 'started_at',
	p_interval := '1 week',
	p_premake := 4,
	p_default_table := true,
	p_automatic_maintenance := 'on',
	p_jobmon := true
);

select partman.create_parent(
	p_parent_table := 'raw.tracked_objects',
	p_control := 'first_seen_at',
	p_interval := '1 week',
	p_premake := 4,
	p_default_table := true,
	p_automatic_maintenance := 'on',
	p_jobmon := true
);

select partman.create_parent(
	p_parent_table := 'raw.detections',
	p_control := 'detection_time',
	p_interval := '1 week',
	p_premake := 4,
	p_default_table := true,
	p_automatic_maintenance := 'on',
	p_jobmon := true
);

