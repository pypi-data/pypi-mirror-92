CREATE TABLE IF NOT EXISTS `TNS_files` (
  `primaryId` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'An internal counter',
  `TNSId` varchar(100) NOT NULL,
  `dateCreated` datetime DEFAULT CURRENT_TIMESTAMP,
  `dateObs` datetime DEFAULT NULL,
  `filename` varchar(200) DEFAULT NULL,
  `spec1phot2` tinyint(4) DEFAULT NULL,
  `url` varchar(800) DEFAULT NULL,
  `updated` tinyint(4) DEFAULT '0',
  `dateLastModified` datetime DEFAULT NULL,
  `comment` VARCHAR(800) NULL DEFAULT NULL,
  PRIMARY KEY (`primaryId`),
  UNIQUE KEY `tnsid_url` (`TNSId`,`url`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=latin1;
            
INSERT IGNORE INTO `TNS_files` (`TNSId`,`dateObs`,`filename`,`spec1phot2`,`url`, dateCreated) VALUES ("2016asf" ,"2016-03-08 07:46:14" ,"tns_2016asf_classrep_145_DAO_OTS.ps" ,"1" ,"https://www.wis-tns.org/system/files/uploaded/DAO_OTS/tns_2016asf_classrep_145_DAO_OTS.ps", NOW())  ON DUPLICATE KEY UPDATE  `TNSId`="2016asf", `dateObs`="2016-03-08 07:46:14", `filename`="tns_2016asf_classrep_145_DAO_OTS.ps", `spec1phot2`="1", `url`="https://www.wis-tns.org/system/files/uploaded/DAO_OTS/tns_2016asf_classrep_145_DAO_OTS.ps" ;
INSERT IGNORE INTO `TNS_files` (`TNSId`,`dateObs`,`filename`,`spec1phot2`,`url`, dateCreated) VALUES ("2016asf" ,"2016-03-08 07:46:14" ,"tns_2016asf_2016-03-08_07-46-14_Plaskett_Telescope_Plaskett_DAO_OTS.txt" ,"1" ,"https://www.wis-tns.org/system/files/uploaded/DAO_OTS/tns_2016asf_2016-03-08_07-46-14_Plaskett_Telescope_Plaskett_DAO_OTS.txt", NOW())  ON DUPLICATE KEY UPDATE  `TNSId`="2016asf", `dateObs`="2016-03-08 07:46:14", `filename`="tns_2016asf_2016-03-08_07-46-14_Plaskett_Telescope_Plaskett_DAO_OTS.txt", `spec1phot2`="1", `url`="https://www.wis-tns.org/system/files/uploaded/DAO_OTS/tns_2016asf_2016-03-08_07-46-14_Plaskett_Telescope_Plaskett_DAO_OTS.txt" ;
INSERT IGNORE INTO `TNS_files` (`TNSId`,`dateObs`,`filename`,`spec1phot2`,`url`, dateCreated) VALUES ("2016asf" ,"2016-03-08 07:46:14" ,"tns_2016asf_2016-03-08_07-46-14_Plaskett_Telescope_Plaskett_DAO_OTS.fits" ,"1" ,"https://www.wis-tns.org/system/files/uploaded/DAO_OTS/tns_2016asf_2016-03-08_07-46-14_Plaskett_Telescope_Plaskett_DAO_OTS.fits", NOW())  ON DUPLICATE KEY UPDATE  `TNSId`="2016asf", `dateObs`="2016-03-08 07:46:14", `filename`="tns_2016asf_2016-03-08_07-46-14_Plaskett_Telescope_Plaskett_DAO_OTS.fits", `spec1phot2`="1", `url`="https://www.wis-tns.org/system/files/uploaded/DAO_OTS/tns_2016asf_2016-03-08_07-46-14_Plaskett_Telescope_Plaskett_DAO_OTS.fits" ;