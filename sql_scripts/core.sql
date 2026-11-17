set search_path = core;


create table if not exists tracks (
	id bigserial,
	track_id bigint not null,
	class_id int not null,
	video_id int not null,
	session_id uuid not null,

	first_seen timestamp not null default now(),
	last_seen timestamp not null,
	duration_seconds float not null,
	detection_count int not null,

	entry_x_norm float not null,
	entry_y_norm float not null,
	exit_x_norm float not null,
	exit_y_norm float not null,
	trajectory_length_norm float not null default 0,
	direction_rad float,
	
	avg_speed_norm float not null default 0,
	max_speed_norm float not null default 0,
	min_speed_norm float not null default 0,
	speed_variance float,

	avg_confidence float not null,
	primary key(id, first_seen),
	check (
		last_seen >= first_seen
	),
	check (
		duration_seconds >= 0 and
		detection_count > 0
	),
	check (
		entry_x_norm between 0 and 1 and
		entry_y_norm between 0 and 1 and
		exit_x_norm between 0 and 1 and
		exit_y_norm between 0 and 1 and
		trajectory_length_norm >= 0
	),
	check (
		avg_speed_norm >= 0 and
		max_speed_norm >= 0 and
		min_speed_norm >= 0 and
		(speed_variance is null or speed_variance >= 0) and
		avg_confidence between 0 and 1
	)
) partition by range(first_seen);

create index idx_video_time on tracks(video_id, first_seen desc);
create index idx_tracks_session_track on tracks(session_id, track_id);
create index idx_video_class_time on tracks(video_id, class_id, first_seen desc);

select partman.create_parent(
	p_parent_table := 'core.tracks',
	p_control := 'first_seen',
	p_interval := '1 week',
	p_premake := 4,
	p_default_table := true,
	p_automatic_maintenance := 'on',
	p_jobmon := true
);

create table if not exists tracks_trajectory_history (
	track_id bigint not null,
	session_id uuid not null,

	video_id int not null,
	first_seen timestamp not null,
	
	trajectory_points jsonb,
	point_count int not null,

	primary key (session_id, track_id, first_seen),
	check (point_count > 0),
    check (jsonb_typeof(trajectory_points) = 'array')
) partition by range(first_seen);

create index idx_history_video_time on core.tracks_trajectory_history (video_id, first_seen desc);
create index idx_history_session_track on core.tracks_trajectory_history (session_id, track_id);

select partman.create_parent(
	p_parent_table := 'core.tracks_trajectory_history',
	p_control := 'first_seen',
	p_interval := '1 week',
	p_premake := 4,
	p_default_table := true,
	p_automatic_maintenance := 'on',
	p_jobmon := true
);

create table if not exists speed_event