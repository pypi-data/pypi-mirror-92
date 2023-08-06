CREATE TABLE IF NOT EXISTS `fs_tns_files` (
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
) ENGINE=MyISAM AUTO_INCREMENT=0 DEFAULT CHARSET=latin1;
            
INSERT IGNORE INTO `fs_tns_files` (`TNSId`,`dateObs`,`filename`,`spec1phot2`,`url`, dateCreated) VALUES ("2016fbz" ,"2016-08-26 08:56:52" ,"tns_2016fbz_2016-08-26_08-56-52_P60_SED-Machine_iPTF.ascii" ,"1" ,"https://www.wis-tns.org/system/files/uploaded/iPTF/tns_2016fbz_2016-08-26_08-56-52_P60_SED-Machine_iPTF.ascii", NOW())  ON DUPLICATE KEY UPDATE  `TNSId`="2016fbz", `dateObs`="2016-08-26 08:56:52", `filename`="tns_2016fbz_2016-08-26_08-56-52_P60_SED-Machine_iPTF.ascii", `spec1phot2`="1", `url`="https://www.wis-tns.org/system/files/uploaded/iPTF/tns_2016fbz_2016-08-26_08-56-52_P60_SED-Machine_iPTF.ascii" ;
INSERT IGNORE INTO `fs_tns_files` (`TNSId`,`dateObs`,`filename`,`spec1phot2`,`url`, dateCreated) VALUES ("2016fbz" ,"2016-08-27 14:24:00" ,"tns_2016fbz_2016-08-27.60_BAO-2.16m_Phot-spec.txt" ,"1" ,"https://www.wis-tns.org/system/files/uploaded/general/tns_2016fbz_2016-08-27.60_BAO-2.16m_Phot-spec.txt", NOW())  ON DUPLICATE KEY UPDATE  `TNSId`="2016fbz", `dateObs`="2016-08-27 14:24:00", `filename`="tns_2016fbz_2016-08-27.60_BAO-2.16m_Phot-spec.txt", `spec1phot2`="1", `url`="https://www.wis-tns.org/system/files/uploaded/general/tns_2016fbz_2016-08-27.60_BAO-2.16m_Phot-spec.txt" ;