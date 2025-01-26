CREATE TABLE main_table (
	id INTEGER NOT NULL, 
	name VARCHAR, 
	sentences VARCHAR NOT NULL, 
	is_uesd BOOLEAN NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);insert into `main_table` (`id`, `is_uesd`, `name`, `sentences`) values (1, 0, '1', '1-1');
insert into `main_table` (`id`, `is_uesd`, `name`, `sentences`) values (2, 1, '2', '2-2');
insert into `main_table` (`id`, `is_uesd`, `name`, `sentences`) values (3, 0, '3', '3-3');
insert into `main_table` (`id`, `is_uesd`, `name`, `sentences`) values (4, 0, '4', '4-4');
insert into `main_table` (`id`, `is_uesd`, `name`, `sentences`) values (5, 0, '5', '5-5');
insert into `main_table` (`id`, `is_uesd`, `name`, `sentences`) values (6, 1, '6', '6-6');
