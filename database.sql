drop schema if exists biosecurity;
create schema biosecurity;
use biosecurity;

drop table if exists role;
create table role (
                      role_id int not null auto_increment primary key,
                      role_name varchar(50) not null
);
INSERT INTO role (role_name) VALUES
('Administrator'),
('Staff'),
('Pest Controller');

drop table if exists user;
create table user (
    user_id int not null auto_increment primary key,
    user_name varchar(50) not null,
    password_hash varchar(200) not null ,
    role_id int not null
);

INSERT INTO user (user_name, password_hash, role_id) VALUES
('admin', 'e8779a100293a9c3bd09845d9269d09db4d2973042dd3904298de98a65f31cbc', 1);
commit;

INSERT INTO user (user_name, password_hash, role_id) VALUES
('staff1', 'e8779a100293a9c3bd09845d9269d09db4d2973042dd3904298de98a65f31cbc', 2);
commit;

INSERT INTO user (user_name, password_hash, role_id) VALUES
('staff2', 'e8779a100293a9c3bd09845d9269d09db4d2973042dd3904298de98a65f31cbc', 2);
commit;

INSERT INTO user (user_name, password_hash, role_id) VALUES
('staff3', 'e8779a100293a9c3bd09845d9269d09db4d2973042dd3904298de98a65f31cbc', 2);
commit;

INSERT INTO user (user_name, password_hash, role_id) VALUES
('Pest Controllers users1', 'e8779a100293a9c3bd09845d9269d09db4d2973042dd3904298de98a65f31cbc', 3);
commit;

INSERT INTO user (user_name, password_hash, role_id) VALUES
('Pest Controllers users2', 'e8779a100293a9c3bd09845d9269d09db4d2973042dd3904298de98a65f31cbc', 3);
commit;

INSERT INTO user (user_name, password_hash, role_id) VALUES
('Pest Controllers users3', 'e8779a100293a9c3bd09845d9269d09db4d2973042dd3904298de98a65f31cbc', 3);
commit;

INSERT INTO user (user_name, password_hash, role_id) VALUES
('Pest Controllers users4', 'e8779a100293a9c3bd09845d9269d09db4d2973042dd3904298de98a65f31cbc', 3);
commit;

INSERT INTO user (user_name, password_hash, role_id) VALUES
('Pest Controllers users5', 'e8779a100293a9c3bd09845d9269d09db4d2973042dd3904298de98a65f31cbc', 3);
commit;

drop table if exists admin_profile;
CREATE table admin_profile (
	admin_id INT not null auto_increment primary key,
    user_id int not null,
    first_name varchar(50) not null,
    last_name varchar(50) not null,
    address varchar(255),
    email varchar(100) not null,
    phone varchar(11) not null,
	date_joined date,
    status varchar(25),
    foreign key (user_id) references user(user_id) on delete cascade
);

drop table if exists staff_profile;
CREATE table staff_profile (
	staff_id INT not null auto_increment primary key,
    user_id int not null,
    staff_number varchar(6),
    first_name varchar(50) not null,
    last_name varchar(50) not null,
    email varchar(100) not null,
    phone varchar(11) not null,
	hire_date date,
    position varchar(100),
    department varchar(100),
    status varchar(25),
    foreign key (user_id) references user(user_id) on delete cascade
);

drop table if exists controller_profile;
CREATE table controller_profile (
	controller_id INT not null auto_increment primary key,
    user_id int not null,
    first_name varchar(50) not null,
    last_name varchar(50) not null,
    address varchar(255),
    email varchar(100) not null,
    phone varchar(11) not null,
	date_joined date,
    status varchar(25),
    foreign key (user_id) references user(user_id) on delete cascade
);

drop table if exists animal_guide;
CREATE table animal_guide (
	animal_id INT not null auto_increment primary key,
    description varchar(255) not null,
    distribution varchar(255),
    size varchar(255),
    droppings varchar(255),
    footprints text,
	impacts text,
    control_methods text,
    primary_image varchar(255),
    secondary_image varchar(255)
);
