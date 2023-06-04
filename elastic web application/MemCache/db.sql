-- -----------------------------------------------------
-- Schema serverdb
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `serverdb` ;

-- -----------------------------------------------------
-- Schema serverdb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `serverdb` DEFAULT CHARACTER SET utf8 ;
USE `serverdb` ;

-- -----------------------------------------------------
-- Table serverdb.configure
-- -----------------------------------------------------
DROP TABLE IF EXISTS `serverdb`.`configure` ;

CREATE TABLE IF NOT EXISTS `serverdb`.`configure`(
    `id` INT NOT NULL, -- Should only exist one configure
    `replacement_policy` VARCHAR(50) NOT NULL,
    `capacity` FLOAT NOT NULL, -- Size will be in MB
    `max_miss_rate_th` FLOAT NOT NULL, -- Within 0 to 1
    `min_miss_rate_th` FLOAT NOT NULL, -- Within 0 to 1
    `expand_ratio` FLOAT NOT NULL, -- Should be greater than 1
    `shrink_ratio` FLOAT NOT NULL, -- Should be greater than 0, less than 1
    PRIMARY KEY (`id`)
)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table serverdb.stats
-- Should be stored based on every 5 second 
-- -----------------------------------------------------
DROP TABLE IF EXISTS `serverdb`.`stats` ;

CREATE TABLE IF NOT EXISTS `serverdb`.`stats`(
    `time` DATETIME(6) NOT NULL, 
    `items_in_cache` INT NOT NULL,
    `total_size` FLOAT NOT NULL,
    `n_requests_served` INT NOT NULL,
    `n_requests_missed` INT NOT NULL,
    PRIMARY KEY (`time`)
)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table serverdb.item
-- -----------------------------------------------------
DROP TABLE IF EXISTS `serverdb`.`item` ;

CREATE TABLE IF NOT EXISTS `serverdb`.`item` (
    `key` VARCHAR (50) NOT NULL , 
    `name` VARCHAR (200) NOT NULL,
    `LAT` DATETIME(6),
    PRIMARY KEY (`key`),
    UNIQUE (`key`)
)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Initialization
-- -----------------------------------------------------
START TRANSACTION;
USE `serverdb`;
INSERT INTO `serverdb`.`configure` (`id`, `replacement_policy`, `capacity`, `max_miss_rate_th`, `min_miss_rate_th`, `expand_ratio`, `shrink_ratio`) VALUES (0, 'LRU', 1, 0.8, 0.2, 2, 0.5);

COMMIT;