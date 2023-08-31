CREATE TABLE `Vehicles` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`LP_num` VARCHAR(255) NOT NULL,
	`make` VARCHAR(255) NOT NULL,
	`model` VARCHAR(255) NOT NULL,
	`colour` VARCHAR(255) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Cameras` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`lat` FLOAT NOT NULL,
	`long` FLOAT NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Journeys` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`vehicle_id` INT NOT NULL,
	`camera_id` INT NOT NULL,
	`time` TIME NOT NULL,
	`date` DATE NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `usual_route` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`vehicle_id` INT NOT NULL,
	`start_journey_id` INT NOT NULL,
	`end_journey_id` INT NOT NULL,
	`start_time_window` TIME NOT NULL,
	`end_time_window` TIME NOT NULL,
	`dayOfTheWeek` DATE NOT NULL,
	`dayOfTheMonth` DATE NOT NULL,
	`avg_appearances` INT NOT NULL,
	PRIMARY KEY (`id`)
);

ALTER TABLE `Journeys` ADD CONSTRAINT `Journeys_fk0` FOREIGN KEY (`vehicle_id`) REFERENCES `Vehicles`(`id`);

ALTER TABLE `Journeys` ADD CONSTRAINT `Journeys_fk1` FOREIGN KEY (`camera_id`) REFERENCES `Cameras`(`id`);

ALTER TABLE `usual_route` ADD CONSTRAINT `usual_route_fk0` FOREIGN KEY (`vehicle_id`) REFERENCES `Vehicles`(`id`);

ALTER TABLE `usual_route` ADD CONSTRAINT `usual_route_fk1` FOREIGN KEY (`start_journey_id`) REFERENCES `Journeys`(`id`);

ALTER TABLE `usual_route` ADD CONSTRAINT `usual_route_fk2` FOREIGN KEY (`end_journey_id`) REFERENCES `Journeys`(`id`);





