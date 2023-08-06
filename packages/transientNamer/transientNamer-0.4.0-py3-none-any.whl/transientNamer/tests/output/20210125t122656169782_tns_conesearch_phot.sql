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
            
INSERT IGNORE INTO `fs_tns_photometry` (`TNSId`,`exptime`,`filter`,`limitingMag`,`mag`,`magErr`,`magUnit`,`objectName`,`obsdate`,`reportAddedDate`,`reportingGroup`,`suggestedType`,`survey`,`telescope`, dateCreated) VALUES ("2016ayk" ,"60" ,"G-Gaia" ,"0" ,"18.59" ,"0.2" ,"ABMag" ,"Gaia18dmh" ,"2018-11-18 10:52:19" ,"2018-11-20 13:53:11" ,"GaiaAlerts" ,"Other" ,"GaiaAlerts" ,"Gaia_Gaia-photometric", NOW())  ON DUPLICATE KEY UPDATE  `TNSId`="2016ayk", `exptime`="60", `filter`="G-Gaia", `limitingMag`="0", `mag`="18.59", `magErr`="0.2", `magUnit`="ABMag", `objectName`="Gaia18dmh", `obsdate`="2018-11-18 10:52:19", `reportAddedDate`="2018-11-20 13:53:11", `reportingGroup`="GaiaAlerts", `suggestedType`="Other", `survey`="GaiaAlerts", `telescope`="Gaia_Gaia-photometric" ;
INSERT IGNORE INTO `fs_tns_photometry` (`TNSId`,`exptime`,`filter`,`limitingMag`,`mag`,`magErr`,`magUnit`,`objectName`,`obsdate`,`reportAddedDate`,`reportingGroup`,`suggestedType`,`survey`,`telescope`, dateCreated) VALUES ("2016ayk" ,null ,"G-Gaia" ,"1" ,"21.5" ,null ,"ABMag" ,"Gaia18dmh" ,"2018-11-17 22:50:52" ,"2018-11-20 13:53:11" ,"GaiaAlerts" ,"Other" ,"GaiaAlerts" ,"Gaia_Gaia-photometric", NOW())  ON DUPLICATE KEY UPDATE  `TNSId`="2016ayk", `exptime`=null, `filter`="G-Gaia", `limitingMag`="1", `mag`="21.5", `magErr`=null, `magUnit`="ABMag", `objectName`="Gaia18dmh", `obsdate`="2018-11-17 22:50:52", `reportAddedDate`="2018-11-20 13:53:11", `reportingGroup`="GaiaAlerts", `suggestedType`="Other", `survey`="GaiaAlerts", `telescope`="Gaia_Gaia-photometric" ;
INSERT IGNORE INTO `fs_tns_photometry` (`TNSId`,`exptime`,`filter`,`limitingMag`,`mag`,`magErr`,`magUnit`,`objectName`,`obsdate`,`reportAddedDate`,`reportingGroup`,`suggestedType`,`survey`,`telescope`, dateCreated) VALUES ("2016ayk" ,null ,"cyan-ATLAS" ,"0" ,"17.99" ,null ,"ABMag" ,"ATLAS16aex" ,"2016-03-03 08:09:36" ,"2016-03-11 17:16:41" ,"ATLAS" ,"PSN" ,"ATLAS" ,"ATLAS1_ACAM1", NOW())  ON DUPLICATE KEY UPDATE  `TNSId`="2016ayk", `exptime`=null, `filter`="cyan-ATLAS", `limitingMag`="0", `mag`="17.99", `magErr`=null, `magUnit`="ABMag", `objectName`="ATLAS16aex", `obsdate`="2016-03-03 08:09:36", `reportAddedDate`="2016-03-11 17:16:41", `reportingGroup`="ATLAS", `suggestedType`="PSN", `survey`="ATLAS", `telescope`="ATLAS1_ACAM1" ;