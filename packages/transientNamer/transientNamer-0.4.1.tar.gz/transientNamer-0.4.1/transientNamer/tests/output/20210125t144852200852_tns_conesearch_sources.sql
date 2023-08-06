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
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=latin1;
            
INSERT IGNORE INTO `fs_tns_sources` (`TNSId`,`TNSName`,`decDeg`,`decSex`,`discDate`,`discMag`,`discMagFilter`,`discSurvey`,`discoveryName`,`hostName`,`hostRedshift`,`objectUrl`,`raDeg`,`raSex`,`reportingSurvey`,`separationArcsec`,`separationEastArcsec`,`separationNorthArcsec`,`specType`,`transRedshift`, dateCreated) VALUES ("2016ayk" ,"AT2016ayk" ,"35.741569" ,"+35:44:29.65" ,"2016-03-03 08:09:36.000" ,"17.99" ,"cyan-ATLAS" ,"ATLAS, GaiaAlerts" ,"ATLAS16aex" ,null ,null ,"https://www.wis-tns.org/object/2016ayk" ,"101.26391666666666" ,"06:45:03.340" ,"ATLAS, GaiaAlerts" ,"0.3" ,"-0.2" ,"-0.1" ,null ,null, NOW())  ON DUPLICATE KEY UPDATE  `TNSId`="2016ayk", `TNSName`="AT2016ayk", `decDeg`="35.741569", `decSex`="+35:44:29.65", `discDate`="2016-03-03 08:09:36.000", `discMag`="17.99", `discMagFilter`="cyan-ATLAS", `discSurvey`="ATLAS, GaiaAlerts", `discoveryName`="ATLAS16aex", `hostName`=null, `hostRedshift`=null, `objectUrl`="https://www.wis-tns.org/object/2016ayk", `raDeg`="101.26391666666666", `raSex`="06:45:03.340", `reportingSurvey`="ATLAS, GaiaAlerts", `separationArcsec`="0.3", `separationEastArcsec`="-0.2", `separationNorthArcsec`="-0.1", `specType`=null, `transRedshift`=null ;