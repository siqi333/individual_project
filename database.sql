drop schema if exists biosecurity;
create schema biosecurity;
use biosecurity;

drop table if exists admin_profile;
drop table if exists staff_profile;
drop table if exists controller_profile;
drop table if exists animal_guide;
drop table if exists role;
drop table if exists user;

create table role (
                      role_id int not null auto_increment primary key,
                      role_name varchar(50) not null
);
INSERT INTO role (role_name) VALUES
('Administrator'),
('Staff'),
('Pest Controller');


create table user (
    user_id int not null auto_increment primary key,
    user_name varchar(50) not null,
    password_hash varchar(200) not null,
    role_id int not null
);

INSERT INTO user (user_name, password_hash, role_id) VALUES
('admin', 'e8779a100293a9c3bd09845d9269d09db4d2973042dd3904298de98a65f31cbc', 1);
commit;

INSERT INTO user (user_name, password_hash, role_id) VALUES
('staff1', 'e8779a100293a9c3bd09845d9269d09db4d2973042dd3904298de98a65f31cbc', 2),
('staff2', 'e8779a100293a9c3bd09845d9269d09db4d2973042dd3904298de98a65f31cbc', 2),
('staff3', 'e8779a100293a9c3bd09845d9269d09db4d2973042dd3904298de98a65f31cbc', 2);
commit;

INSERT INTO user (user_name, password_hash, role_id) VALUES
('PC1', 'e8779a100293a9c3bd09845d9269d09db4d2973042dd3904298de98a65f31cbc', 3),
('PC2', 'e8779a100293a9c3bd09845d9269d09db4d2973042dd3904298de98a65f31cbc', 3),
('PC3', 'e8779a100293a9c3bd09845d9269d09db4d2973042dd3904298de98a65f31cbc', 3),
('PC4', 'e8779a100293a9c3bd09845d9269d09db4d2973042dd3904298de98a65f31cbc', 3),
('PC5', 'e8779a100293a9c3bd09845d9269d09db4d2973042dd3904298de98a65f31cbc', 3);
commit;

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

insert into admin_profile (user_id, first_name, last_name, address, email, phone, date_joined, status)
values (1,'ad','min','address','email@email.com','08001234',str_to_date('19700102','%Y%m%d'), 'active');
commit;


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


insert into staff_profile (user_id, staff_number, first_name, last_name, email, phone, hire_date, position, department, status)
values (2,'123456','st','aff','email@email.com','08001234',str_to_date('19700102','%Y%m%d'), 'position', 'dept', 'active');
commit;


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

insert into controller_profile (user_id, first_name, last_name, address, email, phone, date_joined, status)
values (5,'cont','roller','address','email@email.com','08001234',str_to_date('19700102','%Y%m%d'),'active');
commit;

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
insert into animal_guide
    (description,distribution,size,droppings,footprints,impacts,control_methods,primary_image,secondary_image)
values
    ('Adults can reach up to 50 cm in arm span.','Originally from the northern Pacific','20~50cm','starfish','None','It competes with native predators for food resources.','Mechanical removal','sea_star1.png','sea_star2.png'),
    ('The European Shore Crab is a small','Originally from European and North African coasts','Up to 7.5 cm (3 inches)','Not commonly highlighted','None','Alters the ecological balance of invaded habitats, impacting native species diversity.','Manual removal','shore_crab1.png','shore_crab2.png'),
    ('The Chinese Mitten Crab is a notable freshwater and estuarine crab, recognized by its furry, mitten-like claws.','Originally from East Asia','Up to 10 cm','Specific details about their droppings are not typically highlighted','None','It burrows into riverbanks and levees, causing erosion and structural damage.','Physical removal','mitten_crab1.png','mitten_crab2.png'),
    ('The interior of the shell is usually light purple to pink.','Originally from Asia','Up to 5 cm (2 inches)','Asian Clam droppings, or biodeposits, contribute to sediment enrichment ','None','Filters large volumes of water, removing significant amounts of plankton and potentially impacting food chains.','Water treatment','clam1.png','clam2.png'),
    ('Aquarium Caulerpa is a green marine algae','Caulerpa, especially Caulerpa taxifolia','Up to several feet ','As a plant-like organism, Caulerpa does not produce "droppings" in the way animals do','None','Can hinder commercial fishing activities and affect the aesthetic and ecological value of invaded marine ecosystems.','Biological control','aquarium_caulerpa1.png','aquarium_caulerpa2.png'),
    ('The Mediterranean Fanworm is a sessile marine polychaete worm characterized by its long','Originally from the Mediterranean Sea','Up to 40 cm','As filter feeders, their droppings contribute to the benthic organic matter.','None','Can form dense aggregations, outcompeting native species for space and resources.','Monitoring and rapid response','fanworm1.jpeg','fanworm2.jpeg'),
    ('The Droplet Tunicate is a colonial sea squirt that forms dense mats on marine substrates.','Originally thought to be native to Japan','small','As filter feeders, droplet tunicates process large volumes of water.','None','Competes with native marine organisms for space, light, and resources.','Physical removal','tunicate1.jpeg','tunicate2.jpeg'),
    ('The Clubbed Tunicate is a solitary marine invertebrate characterized by its tough','Originally from the Northwest Pacific','Up to 15-20 cm','As filter feeders, Clubbed Tunicates consume plankton','None','Competes with native species for space and resources, potentially displacing them.','Physical removal','clubbed_tunicate1.jpeg','clubbed_tunicate2.jpeg'),
    ('The Asian Date Mussel is a small','Originally from the Pacific coast of Asia','Up to about 5 cm (2 inches)','Like other filter-feeding bivalves','None','Dense populations can smother native bivalves and other benthic organisms, reducing biodiversity.','Biological control','mussel1.jpeg','mussel2.jpeg'),
    ('The Asian Paddle Crab is a medium-sized marine crab','Native to the western Pacific Ocean','Up to 12 cm (about 4.7 inches)','Asian Paddle Crabs','None','Competes with native species for food and habitat, potentially displacing them','Monitoring and surveillance','paddle_crab1.jpeg','paddle_crab2.jpeg'),
    ('Wakame is a type of edible seaweed','Originally from the cold temperate coastal areas of Japan, Korea, and China','2-3 meters','As an algae, Wakame does not produce droppings in the traditional sense.','None','Displaces native algae and seagrass species, reducing biodiversity.','Preventative measures','wakame1.jpeg','wakame2.jpeg'),
    ('Moths in the family to which Orthoclydon praefectata belongs typically have wings that are adorned with various patterns and colors, aiding in camouflage or warning predators of their unpalatability.','The distribution of Orthoclydon praefectata would be specific to its ecological requirements.','Wingspan of moth 35~38 mm','The droppings or frass of moth larvae (caterpillars) are typically small, pellet-like, and vary in color based on their diet.','None','The impact of Orthoclydon praefectata, particularly in its larval stage, would depend on its feeding habits.','Control methods for moths and their larvae typically include cultural, biological, and chemical strategies.','flax_looper_mouth2.jpg','flax_looper_mouth1.jpg'),
    ('Nests are formed in the ground or in cavities in houses','New Zealand and introduced','Small to medium–sized insects.','Ants are clean insects and usually designate specific areas in or around their nest for waste','They do leave chemical trails with their pheromones.','Ants play critical roles in ecosystems.','Boiling water, vinegar, or diatomaceous earth','ants2.jpg','ants1.jpg'),
    ('Tyria jacobaeae Linnaeus','From Europe, more common in lower North Island and upper South Island','20-25mm','The caterpillars produce small, dark droppings as they feed on ragwort leaves, indicating active feeding sites.','None','Positively, the larvae consume and help control ragwort.','Introduced as a biological control for ragwort','Cinnabar_moth2.jpg','Cinnabar_moth1.jpg'),
    ('Periplaneta americana (Linnaeus)','Originally from tropical America, found in warmer parts of New Zealand','Large insect, up to 40 mm long','0','None','dirty, wet places','Spray medications','Cockroach2.jpg','Cockroach1.jpg'),
    ('Beetles are characterized by their hard exoskeletons and forewings.','Beetles are found on every continent except Antarctica.','Very small (less than 1 mm)','Beetle droppings, or frass, vary in appearance.','None','Beetles play complex roles in ecosystems.','Control strategies for beetles vary widely depending on the species and context.','beetle2.jpg','beetle1.jpg'),
    ('Fanworms have a long, soft body encased in a hard, protective tube, which they construct from sediment, shell fragments, and other materials found in their environment.','Fanworms are found in oceans worldwide, from shallow waters to the deep sea.','The size of fanworms can vary widely among species.','Like other filter feeders, fanworms contribute to their ecosystems by processing organic particles.','None','Their filter feeding helps clarify water by removing suspended particles.','Generally, fanworms are not considered pests, and control measures are not typically necessary.','fanworm1.jpeg','fanworm2.png'),
    ('These moths often have camouflaged wings to blend into their surroundings.','Potentially spanning across various continents where flax is grown for its fibers or seeds.','Vary widely','In the larval stage, the moth would produce frass (caterpillar droppings).','Moths and their larvae do not leave traditional footprints.','Positive: Adult moths may contribute to pollination to a small extent.','Cultural controls','flax_looper_mouth2.jpg','flax_looper_mouth1.jpg'),
    ('Green Planthoppers are small, winged insects with a distinctive green color that helps them blend into their plant surroundings.','Green Planthoppers are found worldwide, with their distribution closely tied to their host plants.',' From 2 to 3 mm ','Green Planthoppers excrete honeydew, a sugary liquid waste product from the digestion of plant sap.','None','Agricultural damage','Cultural controls','green_planthopper2.jpg','green_planthopper1.jpg'),
    ('A moth referred to as a "Green Spangled Moth" would likely have wings that exhibit a vibrant green color, possibly with spangled or speckled markings that enhance its camouflage among foliage.','Moths with green and spangled appearances can be found worldwide, with their distribution depending on the specific species.','small moths','Moth larvae (caterpillars) produce droppings known as frass.','None','Positive: Adult moths can play roles in pollination, and their larvae (caterpillars) can be important food sources for other wildlife.','Biological controls','green_spangled_moth2.jpg','green_spangled_moth1.jpg');
commit;
