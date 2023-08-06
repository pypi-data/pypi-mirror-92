CREATE TABLE IF NOT EXISTS `TNS_photometry` (
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
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=latin1;
            
INSERT IGNORE INTO `TNS_photometry` (`TNSId`,`exptime`,`filter`,`limitingMag`,`mag`,`magErr`,`magUnit`,`objectName`,`obsdate`,`reportAddedDate`,`reportingGroup`,`suggestedType`,`survey`,`telescope`, dateCreated) VALUES ("2016asf" ,"270" ,"V-Johnson" ,"0" ,"17.1" ,"0.12" ,"VegaMag" ,"ASASSN-16cs" ,"2016-03-06 08:09:36" ,"2016-03-07 04:08:20" ,"ASAS-SN" ,"PSN" ,"ASAS-SN" ,"ASASSN-1_Brutus", NOW())  ON DUPLICATE KEY UPDATE  `TNSId`="2016asf", `exptime`="270", `filter`="V-Johnson", `limitingMag`="0", `mag`="17.1", `magErr`="0.12", `magUnit`="VegaMag", `objectName`="ASASSN-16cs", `obsdate`="2016-03-06 08:09:36", `reportAddedDate`="2016-03-07 04:08:20", `reportingGroup`="ASAS-SN", `suggestedType`="PSN", `survey`="ASAS-SN", `telescope`="ASASSN-1_Brutus" ;
INSERT IGNORE INTO `TNS_photometry` (`TNSId`,`exptime`,`filter`,`limitingMag`,`mag`,`magErr`,`magUnit`,`objectName`,`obsdate`,`reportAddedDate`,`reportingGroup`,`suggestedType`,`survey`,`telescope`, dateCreated) VALUES ("2016asf" ,"270" ,"V-Johnson" ,"1" ,"17.8" ,null ,"VegaMag" ,"ASASSN-16cs" ,"2016-03-02 07:26:24" ,"2016-03-07 04:08:20" ,"ASAS-SN" ,"PSN" ,"ASAS-SN" ,"ASASSN-1_Brutus", NOW())  ON DUPLICATE KEY UPDATE  `TNSId`="2016asf", `exptime`="270", `filter`="V-Johnson", `limitingMag`="1", `mag`="17.8", `magErr`=null, `magUnit`="VegaMag", `objectName`="ASASSN-16cs", `obsdate`="2016-03-02 07:26:24", `reportAddedDate`="2016-03-07 04:08:20", `reportingGroup`="ASAS-SN", `suggestedType`="PSN", `survey`="ASAS-SN", `telescope`="ASASSN-1_Brutus" ;