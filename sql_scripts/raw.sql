set search_path = raw;

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

create table if not exists detections (
	detection_id bigserial,
	video_id int not null,
	session_id uuid not null,
	track_id bigint not null,
	track_type_id int not null,
	
	detection_time timestamp not null default now(),

	bbox_x1_px int not null,
	bbox_y1_px int not null,
	bbox_x2_px int not null,
	bbox_y2_px int not null,

	frame_count int not null,
	confidence float not null,
	frame_width float not null,
	frame_height float not null,
	check (confidence between 0 and 1),
	primary key (detection_id, detection_time)
) partition by range(detection_time);



create index idx_detection_video_time on detections(video_id, detection_time);
create index idx_detections_track ON raw.detections (session_id, track_id);
create index idx_detections_class ON raw.detections (video_id, track_type_id, detection_time);

select partman.create_parent(
	p_parent_table := 'raw.detections',
	p_control := 'detection_time',
	p_interval := '1 week',
	p_premake := 4,
	p_default_table := true,
	p_automatic_maintenance := 'on',
	p_jobmon := true
);

