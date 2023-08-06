CREATE TABLE IF NOT EXISTS `fs_tns_spectra` (
  `primaryId` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'An internal counter',
  `TNSId` varchar(45) NOT NULL,
  `TNSuser` varchar(45) DEFAULT NULL,
  `dateCreated` datetime DEFAULT CURRENT_TIMESTAMP,
  `exptime` double DEFAULT NULL,
  `obsdate` datetime DEFAULT NULL,
  `reportAddedDate` datetime DEFAULT NULL,
  `specType` varchar(100) DEFAULT NULL,
  `survey` varchar(100) DEFAULT NULL,
  `telescope` varchar(100) DEFAULT NULL,
  `transRedshift` double DEFAULT NULL,
  `updated` tinyint(4) DEFAULT '0',
  `dateLastModified` datetime DEFAULT NULL,
  `remarks` VARCHAR(800) NULL DEFAULT NULL,
  `sourceComment` VARCHAR(800) NULL DEFAULT NULL,
  PRIMARY KEY (`primaryId`),
  UNIQUE KEY `u_tnsid_survey_obsdate` (`TNSId`,`survey`,`obsdate`),
  UNIQUE KEY `u_id_user_obsdate` (`TNSId`,`TNSuser`,`obsdate`)
) ENGINE=MyISAM AUTO_INCREMENT=0 DEFAULT CHARSET=latin1;
            
INSERT IGNORE INTO `fs_tns_spectra` (`TNSId`,`TNSuser`,`exptime`,`obsdate`,`reportAddedDate`,`specType`,`survey`,`telescope`,`transRedshift`, dateCreated) VALUES ("2016fbz" ,"rferr" ,null ,"2016-08-26 08:56:52" ,"2016-09-02 08:06:07" ,"SN Ia" ,"iPTF" ,"P60_SEDM" ,"0.045", NOW())  ON DUPLICATE KEY UPDATE  `TNSId`="2016fbz", `TNSuser`="rferr", `exptime`=null, `obsdate`="2016-08-26 08:56:52", `reportAddedDate`="2016-09-02 08:06:07", `specType`="SN Ia", `survey`="iPTF", `telescope`="P60_SEDM", `transRedshift`="0.045" ;
INSERT IGNORE INTO `fs_tns_spectra` (`TNSId`,`TNSuser`,`exptime`,`obsdate`,`reportAddedDate`,`specType`,`survey`,`telescope`,`transRedshift`, dateCreated) VALUES ("2016fbz" ,"rferr" ,"3000" ,"2016-08-27 14:24:00" ,"2016-09-02 08:06:07" ,"SN Ia" ,null ,"BAO-2.16m_Phot-spec" ,"0.045", NOW())  ON DUPLICATE KEY UPDATE  `TNSId`="2016fbz", `TNSuser`="rferr", `exptime`="3000", `obsdate`="2016-08-27 14:24:00", `reportAddedDate`="2016-09-02 08:06:07", `specType`="SN Ia", `survey`=null, `telescope`="BAO-2.16m_Phot-spec", `transRedshift`="0.045" ;