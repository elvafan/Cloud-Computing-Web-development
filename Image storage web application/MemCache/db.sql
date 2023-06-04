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
INSERT INTO `serverdb`.`configure` (`id`, `replacement_policy`, `capacity`) VALUES (0, 'LRU', 1);

COMMIT;