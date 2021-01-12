# Host:
# Database: test
# Table: 'data_stream'
#
CREATE TABLE `data_stream` (
  `uid` BIGINT UNSIGNED NOT NULL,
  `size` BIGINT SIGNED,
  `version` varchar(32) default '',
  PRIMARY KEY  (`uid`)
) ENGINE=InnoDB;