CREATE TABLE IF NOT EXISTS `fs_tns_photometry` (
  `primaryId` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'An internal counter',
  `TNSId` varchar(20) NOT NULL,
  `dateCreated` datetime DEFAULT CURRENT_TIMESTAMP,
  `exptime` double DEFAULT NULL,
  `filter` varchar(100) DEFAULT NULL,
  `limitingMag` tinyint(4) DEFAULT NULL,
  `mag` double DEFAULT NULL,
  `magErr` double DEFAULT NULL,
  `magUnit` varchar(100) DEFAULT NULL,
  `objectName` varchar(100) DEFAULT NULL,
  `obsdate` datetime DEFAULT NULL,
  `reportAddedDate` datetime DEFAULT NULL,
  `suggestedType` varchar(100) DEFAULT NULL,
  `survey` varchar(100) DEFAULT NULL,
  `telescope` varchar(100) DEFAULT NULL,
  `updated` tinyint(4) DEFAULT '0',
  `dateLastModified` datetime DEFAULT NULL,
  `remarks` VARCHAR(800) NULL DEFAULT NULL,
  `sourceComment` VARCHAR(800) NULL DEFAULT NULL,
  PRIMARY KEY (`primaryId`),
  UNIQUE KEY `tnsid_survey_obsdate` (`TNSId`,`survey`,`obsdate`),
  UNIQUE INDEX `u_tnsid_survey_obsdate` (`TNSId` ASC, `survey` ASC, `obsdate` ASC),
  UNIQUE INDEX `u_tnsid_obsdate_objname` (`TNSId` ASC, `obsdate` ASC, `objectName` ASC)
) ENGINE=MyISAM AUTO_INCREMENT=0 DEFAULT CHARSET=latin1;
            
INSERT IGNORE INTO `fs_tns_photometry` (`TNSId`,`exptime`,`filter`,`limitingMag`,`mag`,`magErr`,`magUnit`,`objectName`,`obsdate`,`reportAddedDate`,`reportingGroup`,`suggestedType`,`survey`,`telescope`, dateCreated) VALUES ("2016fbz" ,"45" ,"w-PS1" ,"0" ,"17.8" ,"0.02" ,"ABMag" ,"PS16ebg" ,"2016-08-30 13:19:12" ,"2016-09-02 15:54:03" ,"Pan-STARRS1" ,"PSN" ,"Pan-STARRS1" ,"PS1_GPC1", NOW())  ON DUPLICATE KEY UPDATE  `TNSId`="2016fbz", `exptime`="45", `filter`="w-PS1", `limitingMag`="0", `mag`="17.8", `magErr`="0.02", `magUnit`="ABMag", `objectName`="PS16ebg", `obsdate`="2016-08-30 13:19:12", `reportAddedDate`="2016-09-02 15:54:03", `reportingGroup`="Pan-STARRS1", `suggestedType`="PSN", `survey`="Pan-STARRS1", `telescope`="PS1_GPC1" ;
INSERT IGNORE INTO `fs_tns_photometry` (`TNSId`,`exptime`,`filter`,`limitingMag`,`mag`,`magErr`,`magUnit`,`objectName`,`obsdate`,`reportAddedDate`,`reportingGroup`,`suggestedType`,`survey`,`telescope`, dateCreated) VALUES ("2016fbz" ,"60" ,"g-PTF" ,"0" ,"17.2823" ,null ,"ABMag" ,"iPTF16fbz" ,"2016-08-25 12:00:00" ,"2016-08-25 12:34:00" ,"iPTF" ,"PSN" ,"iPTF" ,"P48_CFH12k", NOW())  ON DUPLICATE KEY UPDATE  `TNSId`="2016fbz", `exptime`="60", `filter`="g-PTF", `limitingMag`="0", `mag`="17.2823", `magErr`=null, `magUnit`="ABMag", `objectName`="iPTF16fbz", `obsdate`="2016-08-25 12:00:00", `reportAddedDate`="2016-08-25 12:34:00", `reportingGroup`="iPTF", `suggestedType`="PSN", `survey`="iPTF", `telescope`="P48_CFH12k" ;
INSERT IGNORE INTO `fs_tns_photometry` (`TNSId`,`exptime`,`filter`,`limitingMag`,`mag`,`magErr`,`magUnit`,`objectName`,`obsdate`,`reportAddedDate`,`reportingGroup`,`suggestedType`,`survey`,`telescope`, dateCreated) VALUES ("2016fbz" ,"60" ,"R-PTF" ,"1" ,"21.5" ,null ,"ABMag" ,"iPTF16fbz" ,"2009-01-01 00:00:00" ,"2016-08-25 12:34:00" ,"iPTF" ,"PSN" ,"iPTF" ,"P48_CFH12k", NOW())  ON DUPLICATE KEY UPDATE  `TNSId`="2016fbz", `exptime`="60", `filter`="R-PTF", `limitingMag`="1", `mag`="21.5", `magErr`=null, `magUnit`="ABMag", `objectName`="iPTF16fbz", `obsdate`="2009-01-01 00:00:00", `reportAddedDate`="2016-08-25 12:34:00", `reportingGroup`="iPTF", `suggestedType`="PSN", `survey`="iPTF", `telescope`="P48_CFH12k" ;
INSERT IGNORE INTO `fs_tns_photometry` (`TNSId`,`exptime`,`filter`,`limitingMag`,`mag`,`magErr`,`magUnit`,`objectName`,`obsdate`,`reportAddedDate`,`reportingGroup`,`suggestedType`,`survey`,`telescope`, dateCreated) VALUES ("2016fbz" ,"60" ,"G-Gaia" ,"0" ,"17.4" ,"0.2" ,"ABMag" ,"Gaia16bbi" ,"2016-08-16 19:59:31" ,"2016-08-19 09:13:29" ,"GaiaAlerts" ,"PSN" ,"GaiaAlerts" ,"Gaia_Gaia-photometric", NOW())  ON DUPLICATE KEY UPDATE  `TNSId`="2016fbz", `exptime`="60", `filter`="G-Gaia", `limitingMag`="0", `mag`="17.4", `magErr`="0.2", `magUnit`="ABMag", `objectName`="Gaia16bbi", `obsdate`="2016-08-16 19:59:31", `reportAddedDate`="2016-08-19 09:13:29", `reportingGroup`="GaiaAlerts", `suggestedType`="PSN", `survey`="GaiaAlerts", `telescope`="Gaia_Gaia-photometric" ;
INSERT IGNORE INTO `fs_tns_photometry` (`TNSId`,`exptime`,`filter`,`limitingMag`,`mag`,`magErr`,`magUnit`,`objectName`,`obsdate`,`reportAddedDate`,`reportingGroup`,`suggestedType`,`survey`,`telescope`, dateCreated) VALUES ("2016fbz" ,null ,"G-Gaia" ,"1" ,"21.5" ,null ,"ABMag" ,"Gaia16bbi" ,"2016-07-05 02:38:24" ,"2016-08-19 09:13:29" ,"GaiaAlerts" ,"PSN" ,"GaiaAlerts" ,"Gaia_Gaia-photometric", NOW())  ON DUPLICATE KEY UPDATE  `TNSId`="2016fbz", `exptime`=null, `filter`="G-Gaia", `limitingMag`="1", `mag`="21.5", `magErr`=null, `magUnit`="ABMag", `objectName`="Gaia16bbi", `obsdate`="2016-07-05 02:38:24", `reportAddedDate`="2016-08-19 09:13:29", `reportingGroup`="GaiaAlerts", `suggestedType`="PSN", `survey`="GaiaAlerts", `telescope`="Gaia_Gaia-photometric" ;