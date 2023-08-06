CREATE TABLE IF NOT EXISTS `fs_tns_sources` (
  `primaryId` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'An internal counter',
  `TNSId` varchar(20) NOT NULL,
  `TNSName` varchar(20) DEFAULT NULL,
  `dateCreated` datetime DEFAULT NULL,
  `decDeg` double DEFAULT NULL,
  `decSex` varchar(45) DEFAULT NULL,
  `discDate` datetime DEFAULT NULL,
  `discMag` double DEFAULT NULL,
  `discMagFilter` varchar(45) DEFAULT NULL,
  `discSurvey` varchar(100) DEFAULT NULL,
  `discoveryName` varchar(100) DEFAULT NULL,
  `objectUrl` varchar(200) DEFAULT NULL,
  `raDeg` double DEFAULT NULL,
  `raSex` varchar(45) DEFAULT NULL,
  `specType` varchar(100) DEFAULT NULL,
  `transRedshift` double DEFAULT NULL,
  `updated` tinyint(4) DEFAULT '0',
  `dateLastModified` datetime DEFAULT NULL,
  `hostName` VARCHAR(100) NULL DEFAULT NULL,
  `hostRedshift` DOUBLE NULL DEFAULT NULL, 
  `survey` VARCHAR(100) NULL DEFAULT NULL,
  PRIMARY KEY (`primaryId`),
  UNIQUE KEY `tnsid` (`TNSId`)
) ENGINE=MyISAM AUTO_INCREMENT=0 DEFAULT CHARSET=latin1;
            
INSERT IGNORE INTO `fs_tns_sources` (`TNSId`,`TNSName`,`decDeg`,`decSex`,`discDate`,`discMag`,`discMagFilter`,`discSurvey`,`discoveryName`,`hostName`,`hostRedshift`,`objectUrl`,`raDeg`,`raSex`,`reportingSurvey`,`specType`,`transRedshift`, dateCreated) VALUES ("2016fbz" ,"SN2016fbz" ,"22.05019" ,"+22:03:00.70" ,"2016-08-16 19:59:31.000" ,"17.4" ,"G-Gaia" ,"GaiaAlerts, iPTF, Pan-STARRS1" ,"Gaia16bbi" ,null ,null ,"https://www.wis-tns.org/object/2016fbz" ,"359.816667" ,"23:59:16.000" ,"GaiaAlerts, iPTF, Pan-STARRS1" ,"SN Ia" ,"0.045", NOW())  ON DUPLICATE KEY UPDATE  `TNSId`="2016fbz", `TNSName`="SN2016fbz", `decDeg`="22.05019", `decSex`="+22:03:00.70", `discDate`="2016-08-16 19:59:31.000", `discMag`="17.4", `discMagFilter`="G-Gaia", `discSurvey`="GaiaAlerts, iPTF, Pan-STARRS1", `discoveryName`="Gaia16bbi", `hostName`=null, `hostRedshift`=null, `objectUrl`="https://www.wis-tns.org/object/2016fbz", `raDeg`="359.816667", `raSex`="23:59:16.000", `reportingSurvey`="GaiaAlerts, iPTF, Pan-STARRS1", `specType`="SN Ia", `transRedshift`="0.045" ;