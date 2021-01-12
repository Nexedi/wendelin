# Host:
# Database: test
# Table: 'data_stream'
#
CREATE TABLE `data_stream` (
  `uid` BIGINT UNSIGNED NOT NULL,
  `size` BIGINT UNSIGNED NOT NULL,
  `version` varchar(30) default '',
  PRIMARY KEY  (`uid`)
) ENGINE=InnoDB;