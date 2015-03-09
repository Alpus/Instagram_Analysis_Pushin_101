-- -----------------------------------------------------
-- Schema InstagamBase
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `InstagamBase` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `InstagamBase` ;

-- -----------------------------------------------------
-- Table `InstagamBase`.`Users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `InstagamBase`.`Users` (
  `id_profile` INT UNSIGNED NOT NULL,
  `first_name` VARCHAR(100) NULL,
  `second_name` VARCHAR(100) NULL,
  `registration_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_visit` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `rating` INT NOT NULL  DEFAULT 0,
  PRIMARY KEY (`id_profile`)
  FOREIGN KEY (`id_profile`) REFERENCES `InstagamBase`.`InstProfiles` (`id_profile`),
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `InstagamBase`.`InstProfiles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `InstagamBase`.`InstProfiles` (
  `id_profile` INT UNSIGNED NOT NULL,
  `login` VARCHAR(100) NOT NULL,
  `post_count` INT UNSIGNED NOT NULL,
  `followers_count` INT UNSIGNED NOT NULL,
  `folowing_count` INT UNSIGNED NOT NULL,
  `given_like` INT UNSIGNED  NULL,
  `get_like` INT UNSIGNED NULL,
  `given_comment` INT UNSIGNED NULL,
  `get_comment` INT UNSIGNED NULL,
  `mark_count` INT UNSIGNED NULL,
  `last_check` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_profile`),
  UNIQUE KEY (`login`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `InstagamBase`.`Follows`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `InstagamBase`.`Follows` (
  `id_follow` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_follower` INT UNSIGNED NOT NULL,
  `id_following` INT UNSIGNED NOT NULL,
  `given_like` INT UNSIGNED NULL,
  `given_comment` INT UNSIGNED NULL,
  `last_check` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_follow`),
  UNIQUE KEY (`id_follower`, `id_following`),
  FOREIGN KEY (`id_follower`) REFERENCES `InstagamBase`.`InstProfiles` (`id_profile`),
  FOREIGN KEY (`id_following`) REFERENCES `InstagamBase`.`InstProfiles` (`id_profile`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `InstagamBase`.`ProfileGeos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `InstagamBase`.`ProfileGeos` (
  `id_profilegeo` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_profile` INT UNSIGNED NOT NULL,
  `id_geo` INT UNSIGNED NOT NULL,
  `using_count` INT UNSIGNED NULL,
  `get_like` INT UNSIGNED NULL,
  `get_comment` INT UNSIGNED NULL,
  PRIMARY KEY (`id_profilegeo`),
  UNIQUE KEY ('id_profile', 'id_geo'),
  FOREIGN KEY (`id_profile`) REFERENCES `InstagamBase`.`InstProfiles` (`id_profile`),
  FOREIGN KEY (`id_geo`) REFERENCES `InstagamBase`.`Geos` (`id_geo`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `InstagamBase`.`Geos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `InstagamBase`.`Geos` (
  `id_geo` INT UNSIGNED NOT NULL,
  `geo_name` VARCHAR(300) NOT NULL,
  `using_count` INT UNSIGNED NULL,
  `get_like` INT UNSIGNED NULL,
  `get_comment` INT UNSIGNED NULL,
  PRIMARY KEY (`id_geo`),
  UNIQUE  KEY (`geo_name`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `InstagamBase`.`ProfileWords`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `InstagamBase`.`ProfileWords` (
  `id_profileword` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_profile` INT UNSIGNED NOT NULL,
  `id_word` INT UNSIGNED NOT NULL,
  `using_count` INT UNSIGNED NULL,
  `is_tag` TINYINT(1) NOT NULL,
  PRIMARY KEY (`id_profileword`),
  UNIQUE KEY (`id_profile`, `id_geo`, `is_tag`),
  FOREIGN KEY (`id_profile`) REFERENCES `InstagamBase`.`InstProfiles` (`id_profile`),
  FOREIGN KEY (`id_word`) REFERENCES `InstagamBase`.`Words` (`id_word`))
ENGINE = InnoDB;



-- -----------------------------------------------------
-- Table `InstagamBase`.`Words`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `InstagamBase`.`Words` (
  `id_word` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `word_name` VARCHAR(100) NOT NULL,
  `using_count` INT UNSIGNED NULL,
  `get_like` INT UNSIGNED NULL,
  `get_comment` INT UNSIGNED NULL,
  PRIMARY KEY (`id_word`),
  UNIQUE KEY (`word_name`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `InstagamBase`.`WordMeanings`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `InstagamBase`.`WordMeanings` (
  `id_wordmean` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_word` VARCHAR(100) NOT NULL,
  `id_mean` VARCHAR(100) NOT NULL,
  `importance` INT NOT NULL DEFAULT 1,
  PRIMARY KEY (`id_wordmean`),
  UNIQUE KEY (`id_word`, `id_mean`),
  FOREIGN KEY (`id_word`) REFERENCES `InstagamBase`.`Words` (`id_word`),
  FOREIGN KEY (`id_mean`) REFERENCES `InstagamBase`.`Meanings` (`id_mean`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `InstagamBase`.`Meanings`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `InstagamBase`.`Meanings` (
  `id_mean` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `meaning_name` VARCHAR(100) NOT NULL,
  `using_count` INT UNSIGNED NULL,
  `get_like` INT UNSIGNED NULL,
  `get_comment` INT UNSIGNED NULL,
  PRIMARY KEY (`id_mean`),
  UNIQUE KEY (`meaning_name`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `InstagamBase`.`Posts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `InstagamBase`.`Posts` (
  `id_post`  INT UNSIGNED NOT NULL,
  `id_profile` INT UNSIGNED NOT NULL,
  `get_like` INT UNSIGNED NOT NULL,
  `get_comments` INT UNSIGNED NOT NULL,
  `filter` VARCHAR(100) NOT NULL,
  `last_check` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_post`),
  FOREIGN KEY (`id_profile`) REFERENCES `InstagramBase`.`InstProfiles` (`id_profile`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `InstagamBase`.`ProfileFilters`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `InstagamBase`.`ProfileFilters` (
  `id_profilefilter` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_profile` INT UNSIGNED NOT NULL, 
  `id_filter` INT UNSIGNED NOT NULL,
  `using_count` INT UNSIGNED NULL,
  `get_like` INT UNSIGNED NULL,
  `get_comments` INT UNSIGNED NULL,
  PRIMARY KEY (`id_profilefilter`),
  UNIQUE KEY (`id_profile`, `id_filter`),
  FOREIGN KEY (`id_profile`) REFERENCES `InstagamBase`.`InstProfiles` (`id_profile`),
  FOREIGN KEY (`id_filter`) REFERENCES `InstagamBase`.`Filters` (`id_filter`)))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `InstagamBase`.`Filters`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `InstagamBase`.`Filters` (
  `id_filter`  INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `filter_name` VARCHAR(100) NOT NULL,
  `using_count` INT UNSIGNED NULL,
  `get_like` INT UNSIGNED NULL,
  `get_comments` INT UNSIGNED NULL,
  PRIMARY KEY (`id_filter`),
  UNIQUE KEY (`filter_name`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `InstagamBase`.`ProfileUsermarks`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `InstagamBase`.`ProfileUsermarks` (
  `id_usermarks`  INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_profile` INT UNSIGNED NOT NULL, 
  `id_mark` INT UNSIGNED NOT NULL,
  `using_count` INT UNSIGNED NULL,
  `get_like` INT UNSIGNED NULL,
  `get_comments` INT UNSIGNED NULL,
  PRIMARY KEY (`id_usermarks`),
  UNIQUE KEY (`id_profile`, `id_mark`),
  FOREIGN KEY (`id_profile`) REFERENCES `InstagamBase`.`InstProfiles` (`id_profile`),
  FOREIGN KEY (`id_mark`) REFERENCES `InstagamBase`.`InstProfiles` (`id_profile`)))
ENGINE = InnoDB;