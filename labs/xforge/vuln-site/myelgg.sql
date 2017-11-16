-- MySQL dump 10.13  Distrib 5.6.38, for Linux (x86_64)
--
-- Host: localhost    Database: myelgg
-- ------------------------------------------------------
-- Server version	5.6.38

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `elgg_access_collection_membership`
--

DROP TABLE IF EXISTS `elgg_access_collection_membership`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `elgg_access_collection_membership` (
  `user_guid` int(11) NOT NULL,
  `access_collection_id` int(11) NOT NULL,
  PRIMARY KEY (`user_guid`,`access_collection_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `elgg_access_collection_membership`
--

LOCK TABLES `elgg_access_collection_membership` WRITE;
/*!40000 ALTER TABLE `elgg_access_collection_membership` DISABLE KEYS */;
/*!40000 ALTER TABLE `elgg_access_collection_membership` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `elgg_access_collections`
--

DROP TABLE IF EXISTS `elgg_access_collections`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `elgg_access_collections` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` text NOT NULL,
  `owner_guid` bigint(20) unsigned NOT NULL,
  `site_guid` bigint(20) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `owner_guid` (`owner_guid`),
  KEY `site_guid` (`site_guid`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `elgg_access_collections`
--

LOCK TABLES `elgg_access_collections` WRITE;
/*!40000 ALTER TABLE `elgg_access_collections` DISABLE KEYS */;
/*!40000 ALTER TABLE `elgg_access_collections` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `elgg_annotations`
--

DROP TABLE IF EXISTS `elgg_annotations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `elgg_annotations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `entity_guid` bigint(20) unsigned NOT NULL,
  `name_id` int(11) NOT NULL,
  `value_id` int(11) NOT NULL,
  `value_type` enum('integer','text') NOT NULL,
  `owner_guid` bigint(20) unsigned NOT NULL,
  `access_id` int(11) NOT NULL,
  `time_created` int(11) NOT NULL,
  `enabled` enum('yes','no') NOT NULL DEFAULT 'yes',
  PRIMARY KEY (`id`),
  KEY `entity_guid` (`entity_guid`),
  KEY `name_id` (`name_id`),
  KEY `value_id` (`value_id`),
  KEY `owner_guid` (`owner_guid`),
  KEY `access_id` (`access_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `elgg_annotations`
--

LOCK TABLES `elgg_annotations` WRITE;
/*!40000 ALTER TABLE `elgg_annotations` DISABLE KEYS */;
/*!40000 ALTER TABLE `elgg_annotations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `elgg_api_users`
--

DROP TABLE IF EXISTS `elgg_api_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `elgg_api_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `site_guid` bigint(20) unsigned DEFAULT NULL,
  `api_key` varchar(40) DEFAULT NULL,
  `secret` varchar(40) NOT NULL,
  `active` int(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `api_key` (`api_key`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `elgg_api_users`
--

LOCK TABLES `elgg_api_users` WRITE;
/*!40000 ALTER TABLE `elgg_api_users` DISABLE KEYS */;
/*!40000 ALTER TABLE `elgg_api_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `elgg_config`
--

DROP TABLE IF EXISTS `elgg_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `elgg_config` (
  `name` varchar(255) NOT NULL,
  `value` text NOT NULL,
  `site_guid` int(11) NOT NULL,
  PRIMARY KEY (`name`,`site_guid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `elgg_config`
--

LOCK TABLES `elgg_config` WRITE;
/*!40000 ALTER TABLE `elgg_config` DISABLE KEYS */;
INSERT INTO `elgg_config` VALUES ('view','s:7:\"default\";',1),('language','s:2:\"en\";',1),('default_access','s:1:\"2\";',1),('allow_registration','b:1;',1),('walled_garden','b:0;',1),('allow_user_default_access','s:0:\"\";',1);
/*!40000 ALTER TABLE `elgg_config` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `elgg_datalists`
--

DROP TABLE IF EXISTS `elgg_datalists`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `elgg_datalists` (
  `name` varchar(255) NOT NULL,
  `value` text NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `elgg_datalists`
--

LOCK TABLES `elgg_datalists` WRITE;
/*!40000 ALTER TABLE `elgg_datalists` DISABLE KEYS */;
INSERT INTO `elgg_datalists` VALUES ('filestore_run_once','1510271617'),('plugin_run_once','1510271617'),('elgg_widget_run_once','1510271617'),('installed','1510271899'),('path','/var/www/csrflabelgg.com/elgg/'),('dataroot','/var/run/elgg_data/'),('default_site','1'),('version','2014012000'),('simplecache_enabled','1'),('system_cache_enabled','1'),('processed_upgrades','a:45:{i:0;s:14:\"2008100701.php\";i:1;s:14:\"2008101303.php\";i:2;s:14:\"2009022701.php\";i:3;s:14:\"2009041701.php\";i:4;s:14:\"2009070101.php\";i:5;s:14:\"2009102801.php\";i:6;s:14:\"2010010501.php\";i:7;s:14:\"2010033101.php\";i:8;s:14:\"2010040201.php\";i:9;s:14:\"2010052601.php\";i:10;s:14:\"2010060101.php\";i:11;s:14:\"2010060401.php\";i:12;s:14:\"2010061501.php\";i:13;s:14:\"2010062301.php\";i:14;s:14:\"2010062302.php\";i:15;s:14:\"2010070301.php\";i:16;s:14:\"2010071001.php\";i:17;s:14:\"2010071002.php\";i:18;s:14:\"2010111501.php\";i:19;s:14:\"2010121601.php\";i:20;s:14:\"2010121602.php\";i:21;s:14:\"2010121701.php\";i:22;s:14:\"2010123101.php\";i:23;s:14:\"2011010101.php\";i:24;s:61:\"2011021800-1.8_svn-goodbye_walled_garden-083121a656d06894.php\";i:25;s:61:\"2011022000-1.8_svn-custom_profile_fields-390ac967b0bb5665.php\";i:26;s:60:\"2011030700-1.8_svn-blog_status_metadata-4645225d7b440876.php\";i:27;s:51:\"2011031300-1.8_svn-twitter_api-12b832a5a7a3e1bd.php\";i:28;s:57:\"2011031600-1.8_svn-datalist_grows_up-0b8aec5a55cc1e1c.php\";i:29;s:61:\"2011032000-1.8_svn-widgets_arent_plugins-61836261fa280a5c.php\";i:30;s:59:\"2011032200-1.8_svn-admins_like_widgets-7f19d2783c1680d3.php\";i:31;s:14:\"2011052801.php\";i:32;s:60:\"2011061200-1.8b1-sites_need_a_site_guid-6d9dcbf46c0826cc.php\";i:33;s:62:\"2011092500-1.8.0.1-forum_reply_river_view-5758ce8d86ac56ce.php\";i:34;s:54:\"2011123100-1.8.2-fix_friend_river-b17e7ff8345c2269.php\";i:35;s:53:\"2011123101-1.8.2-fix_blog_status-b14c2a0e7b9e7d55.php\";i:36;s:50:\"2012012000-1.8.3-ip_in_syslog-87fe0f068cf62428.php\";i:37;s:50:\"2012012100-1.8.3-system_cache-93100e7d55a24a11.php\";i:38;s:59:\"2012041800-1.8.3-dont_filter_passwords-c0ca4a18b38ae2bc.php\";i:39;s:58:\"2012041801-1.8.3-multiple_user_tokens-852225f7fd89f6c5.php\";i:40;s:59:\"2013030600-1.8.13-update_user_location-8999eb8bf1bdd9a3.php\";i:41;s:62:\"2013051700-1.8.15-add_missing_group_index-52a63a3a3ffaced2.php\";i:42;s:53:\"2013052900-1.8.15-ipv6_in_syslog-f5c2cc0196e9e731.php\";i:43;s:50:\"2013060900-1.8.15-site_secret-404fc165cf9e0ac9.php\";i:44;s:50:\"2014012000-1.8.18-remember_me-9a8a433685cf7be9.php\";}'),('admin_registered','1'),('simplecache_lastupdate_default','1510272992'),('simplecache_lastcached_default','1510272992'),('__site_secret__','zYJc_b-KOEi0aOIvpfSb89tEtMdrEYZc'),('simplecache_lastupdate_failsafe','0'),('simplecache_lastcached_failsafe','0'),('simplecache_lastupdate_foaf','0'),('simplecache_lastcached_foaf','0'),('simplecache_lastupdate_ical','0'),('simplecache_lastcached_ical','0'),('simplecache_lastupdate_installation','0'),('simplecache_lastcached_installation','0'),('simplecache_lastupdate_json','0'),('simplecache_lastcached_json','0'),('simplecache_lastupdate_opendd','0'),('simplecache_lastcached_opendd','0'),('simplecache_lastupdate_php','0'),('simplecache_lastcached_php','0'),('simplecache_lastupdate_rss','0'),('simplecache_lastcached_rss','0'),('simplecache_lastupdate_xml','0'),('simplecache_lastcached_xml','0');
/*!40000 ALTER TABLE `elgg_datalists` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `elgg_entities`
--

DROP TABLE IF EXISTS `elgg_entities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `elgg_entities` (
  `guid` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `type` enum('object','user','group','site') NOT NULL,
  `subtype` int(11) DEFAULT NULL,
  `owner_guid` bigint(20) unsigned NOT NULL,
  `site_guid` bigint(20) unsigned NOT NULL,
  `container_guid` bigint(20) unsigned NOT NULL,
  `access_id` int(11) NOT NULL,
  `time_created` int(11) NOT NULL,
  `time_updated` int(11) NOT NULL,
  `last_action` int(11) NOT NULL DEFAULT '0',
  `enabled` enum('yes','no') NOT NULL DEFAULT 'yes',
  PRIMARY KEY (`guid`),
  KEY `type` (`type`),
  KEY `subtype` (`subtype`),
  KEY `owner_guid` (`owner_guid`),
  KEY `site_guid` (`site_guid`),
  KEY `container_guid` (`container_guid`),
  KEY `access_id` (`access_id`),
  KEY `time_created` (`time_created`),
  KEY `time_updated` (`time_updated`)
) ENGINE=MyISAM AUTO_INCREMENT=43 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `elgg_entities`
--

LOCK TABLES `elgg_entities` WRITE;
/*!40000 ALTER TABLE `elgg_entities` DISABLE KEYS */;
INSERT INTO `elgg_entities` VALUES (1,'site',0,0,1,0,2,1510271899,1510271899,1510271899,'yes'),(2,'object',2,1,1,1,2,1510271899,1510271899,1510271899,'yes'),(3,'object',2,1,1,1,2,1510271899,1510271899,1510271899,'yes'),(4,'object',2,1,1,1,2,1510271899,1510271899,1510271899,'yes'),(5,'object',2,1,1,1,2,1510271899,1510271899,1510271899,'yes'),(6,'object',2,1,1,1,2,1510271899,1510271899,1510271899,'yes'),(7,'object',2,1,1,1,2,1510271899,1510271899,1510271899,'yes'),(8,'object',2,1,1,1,2,1510271899,1510271899,1510271899,'yes'),(9,'object',2,1,1,1,2,1510271899,1510271899,1510271899,'yes'),(10,'object',2,1,1,1,2,1510271899,1510271899,1510271899,'yes'),(11,'object',2,1,1,1,2,1510271899,1510271899,1510271899,'yes'),(12,'object',2,1,1,1,2,1510271899,1510271899,1510271899,'yes'),(13,'object',2,1,1,1,2,1510271899,1510271899,1510271899,'yes'),(14,'object',2,1,1,1,2,1510271899,1510271899,1510271899,'yes'),(15,'object',2,1,1,1,2,1510271899,1510271899,1510271899,'yes'),(16,'object',2,1,1,1,2,1510271899,1510271899,1510271899,'yes'),(17,'object',2,1,1,1,2,1510271899,1510271899,1510271899,'yes'),(18,'object',2,1,1,1,2,1510271899,1510271899,1510271899,'yes'),(19,'object',2,1,1,1,2,1510271899,1510271899,1510271899,'yes'),(20,'object',2,1,1,1,2,1510271899,1510271899,1510271899,'yes'),(21,'object',2,1,1,1,2,1510271899,1510271899,1510271899,'yes'),(22,'object',2,1,1,1,2,1510271899,1510271899,1510271899,'yes'),(23,'object',2,1,1,1,2,1510271899,1510271899,1510271899,'yes'),(24,'object',2,1,1,1,2,1510271899,1510271899,1510271899,'yes'),(25,'object',2,1,1,1,2,1510271899,1510271899,1510271899,'yes'),(26,'object',2,1,1,1,2,1510271899,1510271899,1510271899,'yes'),(27,'object',2,1,1,1,2,1510271899,1510271899,1510271899,'yes'),(28,'object',2,1,1,1,2,1510271899,1510271899,1510271899,'yes'),(29,'object',2,1,1,1,2,1510271899,1510271899,1510271899,'yes'),(30,'object',2,1,1,1,2,1510271899,1510271899,1510271899,'yes'),(31,'object',2,1,1,1,2,1510271899,1510271899,1510271899,'yes'),(32,'object',2,1,1,1,2,1510271899,1510271899,1510271899,'yes'),(33,'user',0,0,1,0,2,1510271931,1510272591,1510271931,'yes'),(34,'object',3,33,1,33,0,1510271931,1510271931,1510271931,'yes'),(35,'object',3,33,1,33,0,1510271931,1510271931,1510271931,'yes'),(36,'object',3,33,1,33,0,1510271931,1510271931,1510271931,'yes'),(37,'object',3,33,1,33,0,1510271931,1510271931,1510271931,'yes'),(38,'object',3,33,1,33,0,1510271931,1510271931,1510271931,'yes'),(39,'user',0,0,1,0,2,1510272666,1510272666,1510272666,'yes'),(40,'user',0,0,1,0,2,1510272705,1510272705,1510272705,'yes'),(41,'user',0,0,1,0,2,1510272744,1510272744,1510272744,'yes'),(42,'user',0,0,1,0,2,1510272762,1510272762,1510272762,'yes');
/*!40000 ALTER TABLE `elgg_entities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `elgg_entity_relationships`
--

DROP TABLE IF EXISTS `elgg_entity_relationships`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `elgg_entity_relationships` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `guid_one` bigint(20) unsigned NOT NULL,
  `relationship` varchar(50) NOT NULL,
  `guid_two` bigint(20) unsigned NOT NULL,
  `time_created` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `guid_one` (`guid_one`,`relationship`,`guid_two`),
  KEY `relationship` (`relationship`),
  KEY `guid_two` (`guid_two`)
) ENGINE=MyISAM AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `elgg_entity_relationships`
--

LOCK TABLES `elgg_entity_relationships` WRITE;
/*!40000 ALTER TABLE `elgg_entity_relationships` DISABLE KEYS */;
INSERT INTO `elgg_entity_relationships` VALUES (1,2,'active_plugin',1,1510271899),(2,3,'active_plugin',1,1510271899),(3,11,'active_plugin',1,1510271899),(4,12,'active_plugin',1,1510271899),(5,13,'active_plugin',1,1510271899),(7,15,'active_plugin',1,1510271899),(8,16,'active_plugin',1,1510271899),(9,17,'active_plugin',1,1510271899),(10,18,'active_plugin',1,1510271899),(11,19,'active_plugin',1,1510271899),(12,20,'active_plugin',1,1510271899),(13,21,'active_plugin',1,1510271899),(14,22,'active_plugin',1,1510271899),(15,23,'active_plugin',1,1510271899),(16,24,'active_plugin',1,1510271899),(17,25,'active_plugin',1,1510271899),(18,26,'active_plugin',1,1510271899),(19,28,'active_plugin',1,1510271899),(20,29,'active_plugin',1,1510271899),(21,31,'active_plugin',1,1510271899),(22,32,'active_plugin',1,1510271899),(23,33,'member_of_site',1,1510271931),(24,39,'member_of_site',1,1510272666),(25,40,'member_of_site',1,1510272705),(26,41,'member_of_site',1,1510272744),(27,42,'member_of_site',1,1510272762);
/*!40000 ALTER TABLE `elgg_entity_relationships` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `elgg_entity_subtypes`
--

DROP TABLE IF EXISTS `elgg_entity_subtypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `elgg_entity_subtypes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` enum('object','user','group','site') NOT NULL,
  `subtype` varchar(50) NOT NULL,
  `class` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `type` (`type`,`subtype`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `elgg_entity_subtypes`
--

LOCK TABLES `elgg_entity_subtypes` WRITE;
/*!40000 ALTER TABLE `elgg_entity_subtypes` DISABLE KEYS */;
INSERT INTO `elgg_entity_subtypes` VALUES (1,'object','file','ElggFile'),(2,'object','plugin','ElggPlugin'),(3,'object','widget','ElggWidget'),(4,'object','blog','ElggBlog'),(5,'object','thewire','ElggWire');
/*!40000 ALTER TABLE `elgg_entity_subtypes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `elgg_geocode_cache`
--

DROP TABLE IF EXISTS `elgg_geocode_cache`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `elgg_geocode_cache` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `location` varchar(128) DEFAULT NULL,
  `lat` varchar(20) DEFAULT NULL,
  `long` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `location` (`location`)
) ENGINE=MEMORY DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `elgg_geocode_cache`
--

LOCK TABLES `elgg_geocode_cache` WRITE;
/*!40000 ALTER TABLE `elgg_geocode_cache` DISABLE KEYS */;
/*!40000 ALTER TABLE `elgg_geocode_cache` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `elgg_groups_entity`
--

DROP TABLE IF EXISTS `elgg_groups_entity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `elgg_groups_entity` (
  `guid` bigint(20) unsigned NOT NULL,
  `name` text NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY (`guid`),
  KEY `name` (`name`(50)),
  KEY `description` (`description`(50)),
  FULLTEXT KEY `name_2` (`name`,`description`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `elgg_groups_entity`
--

LOCK TABLES `elgg_groups_entity` WRITE;
/*!40000 ALTER TABLE `elgg_groups_entity` DISABLE KEYS */;
/*!40000 ALTER TABLE `elgg_groups_entity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `elgg_hmac_cache`
--

DROP TABLE IF EXISTS `elgg_hmac_cache`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `elgg_hmac_cache` (
  `hmac` varchar(255) NOT NULL,
  `ts` int(11) NOT NULL,
  PRIMARY KEY (`hmac`),
  KEY `ts` (`ts`)
) ENGINE=MEMORY DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `elgg_hmac_cache`
--

LOCK TABLES `elgg_hmac_cache` WRITE;
/*!40000 ALTER TABLE `elgg_hmac_cache` DISABLE KEYS */;
/*!40000 ALTER TABLE `elgg_hmac_cache` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `elgg_metadata`
--

DROP TABLE IF EXISTS `elgg_metadata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `elgg_metadata` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `entity_guid` bigint(20) unsigned NOT NULL,
  `name_id` int(11) NOT NULL,
  `value_id` int(11) NOT NULL,
  `value_type` enum('integer','text') NOT NULL,
  `owner_guid` bigint(20) unsigned NOT NULL,
  `access_id` int(11) NOT NULL,
  `time_created` int(11) NOT NULL,
  `enabled` enum('yes','no') NOT NULL DEFAULT 'yes',
  PRIMARY KEY (`id`),
  KEY `entity_guid` (`entity_guid`),
  KEY `name_id` (`name_id`),
  KEY `value_id` (`value_id`),
  KEY `owner_guid` (`owner_guid`),
  KEY `access_id` (`access_id`)
) ENGINE=MyISAM AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `elgg_metadata`
--

LOCK TABLES `elgg_metadata` WRITE;
/*!40000 ALTER TABLE `elgg_metadata` DISABLE KEYS */;
INSERT INTO `elgg_metadata` VALUES (1,1,1,2,'text',0,2,1510271899,'yes'),(2,33,3,4,'text',33,2,1510271931,'yes'),(3,33,5,4,'text',0,2,1510271931,'yes'),(4,33,6,7,'text',0,2,1510271931,'yes'),(5,39,3,4,'text',39,2,1510272666,'yes'),(6,39,8,4,'text',39,2,1510272666,'yes'),(7,39,9,10,'integer',39,2,1510272666,'yes'),(8,40,3,4,'text',40,2,1510272705,'yes'),(9,40,8,4,'text',40,2,1510272705,'yes'),(10,40,9,10,'integer',40,2,1510272705,'yes'),(11,41,3,4,'text',41,2,1510272744,'yes'),(12,41,8,4,'text',41,2,1510272744,'yes'),(13,41,9,10,'integer',41,2,1510272744,'yes'),(14,42,3,4,'text',42,2,1510272762,'yes'),(15,42,8,4,'text',42,2,1510272762,'yes'),(16,42,9,10,'integer',42,2,1510272762,'yes');
/*!40000 ALTER TABLE `elgg_metadata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `elgg_metastrings`
--

DROP TABLE IF EXISTS `elgg_metastrings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `elgg_metastrings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `string` text NOT NULL,
  PRIMARY KEY (`id`),
  KEY `string` (`string`(50))
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `elgg_metastrings`
--

LOCK TABLES `elgg_metastrings` WRITE;
/*!40000 ALTER TABLE `elgg_metastrings` DISABLE KEYS */;
INSERT INTO `elgg_metastrings` VALUES (1,'email'),(2,'me@you.com'),(3,'notification:method:email'),(4,'1'),(5,'validated'),(6,'validated_method'),(7,'admin_user'),(8,'admin_created'),(9,'created_by_guid'),(10,'33');
/*!40000 ALTER TABLE `elgg_metastrings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `elgg_objects_entity`
--

DROP TABLE IF EXISTS `elgg_objects_entity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `elgg_objects_entity` (
  `guid` bigint(20) unsigned NOT NULL,
  `title` text NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY (`guid`),
  FULLTEXT KEY `title` (`title`,`description`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `elgg_objects_entity`
--

LOCK TABLES `elgg_objects_entity` WRITE;
/*!40000 ALTER TABLE `elgg_objects_entity` DISABLE KEYS */;
INSERT INTO `elgg_objects_entity` VALUES (2,'blog',''),(3,'bookmarks',''),(4,'categories',''),(5,'custom_index',''),(6,'dashboard',''),(7,'developers',''),(8,'diagnostics',''),(9,'embed',''),(10,'externalpages',''),(11,'file',''),(12,'garbagecollector',''),(13,'groups',''),(14,'htmlawed',''),(15,'invitefriends',''),(16,'likes',''),(17,'logbrowser',''),(18,'logrotate',''),(19,'members',''),(20,'messageboard',''),(21,'messages',''),(22,'notifications',''),(23,'pages',''),(24,'profile',''),(25,'reportedcontent',''),(26,'search',''),(27,'tagcloud',''),(28,'thewire',''),(29,'tinymce',''),(30,'twitter_api',''),(31,'uservalidationbyemail',''),(32,'zaudio',''),(34,'',''),(35,'',''),(36,'',''),(37,'',''),(38,'','');
/*!40000 ALTER TABLE `elgg_objects_entity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `elgg_private_settings`
--

DROP TABLE IF EXISTS `elgg_private_settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `elgg_private_settings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `entity_guid` int(11) NOT NULL,
  `name` varchar(128) NOT NULL,
  `value` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `entity_guid` (`entity_guid`,`name`),
  KEY `name` (`name`),
  KEY `value` (`value`(50))
) ENGINE=MyISAM AUTO_INCREMENT=55 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `elgg_private_settings`
--

LOCK TABLES `elgg_private_settings` WRITE;
/*!40000 ALTER TABLE `elgg_private_settings` DISABLE KEYS */;
INSERT INTO `elgg_private_settings` VALUES (1,2,'elgg:internal:priority','1'),(2,3,'elgg:internal:priority','2'),(3,4,'elgg:internal:priority','3'),(4,5,'elgg:internal:priority','4'),(5,6,'elgg:internal:priority','5'),(6,7,'elgg:internal:priority','6'),(7,8,'elgg:internal:priority','7'),(8,9,'elgg:internal:priority','8'),(9,10,'elgg:internal:priority','9'),(10,11,'elgg:internal:priority','10'),(11,12,'elgg:internal:priority','11'),(12,13,'elgg:internal:priority','12'),(13,14,'elgg:internal:priority','13'),(14,15,'elgg:internal:priority','14'),(15,16,'elgg:internal:priority','15'),(16,17,'elgg:internal:priority','16'),(17,18,'elgg:internal:priority','17'),(18,19,'elgg:internal:priority','18'),(19,20,'elgg:internal:priority','19'),(20,21,'elgg:internal:priority','20'),(21,22,'elgg:internal:priority','21'),(22,23,'elgg:internal:priority','22'),(23,24,'elgg:internal:priority','23'),(24,25,'elgg:internal:priority','24'),(25,26,'elgg:internal:priority','25'),(26,27,'elgg:internal:priority','26'),(27,28,'elgg:internal:priority','27'),(28,29,'elgg:internal:priority','28'),(29,30,'elgg:internal:priority','29'),(30,31,'elgg:internal:priority','30'),(31,32,'elgg:internal:priority','31'),(32,34,'handler','control_panel'),(33,34,'context','admin'),(34,34,'column','1'),(35,34,'order','0'),(36,35,'handler','admin_welcome'),(37,35,'context','admin'),(38,35,'order','10'),(39,35,'column','1'),(40,36,'handler','online_users'),(41,36,'context','admin'),(42,36,'column','2'),(43,36,'order','0'),(44,37,'handler','new_users'),(45,37,'context','admin'),(46,37,'order','10'),(47,37,'column','2'),(48,38,'handler','content_stats'),(49,38,'context','admin'),(50,38,'order','20'),(51,38,'column','2'),(52,36,'num_display','8'),(53,37,'num_display','5'),(54,38,'num_display','8');
/*!40000 ALTER TABLE `elgg_private_settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `elgg_river`
--

DROP TABLE IF EXISTS `elgg_river`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `elgg_river` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(8) NOT NULL,
  `subtype` varchar(32) NOT NULL,
  `action_type` varchar(32) NOT NULL,
  `access_id` int(11) NOT NULL,
  `view` text NOT NULL,
  `subject_guid` int(11) NOT NULL,
  `object_guid` int(11) NOT NULL,
  `annotation_id` int(11) NOT NULL,
  `posted` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `type` (`type`),
  KEY `action_type` (`action_type`),
  KEY `access_id` (`access_id`),
  KEY `subject_guid` (`subject_guid`),
  KEY `object_guid` (`object_guid`),
  KEY `annotation_id` (`annotation_id`),
  KEY `posted` (`posted`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `elgg_river`
--

LOCK TABLES `elgg_river` WRITE;
/*!40000 ALTER TABLE `elgg_river` DISABLE KEYS */;
/*!40000 ALTER TABLE `elgg_river` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `elgg_sites_entity`
--

DROP TABLE IF EXISTS `elgg_sites_entity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `elgg_sites_entity` (
  `guid` bigint(20) unsigned NOT NULL,
  `name` text NOT NULL,
  `description` text NOT NULL,
  `url` varchar(255) NOT NULL,
  PRIMARY KEY (`guid`),
  UNIQUE KEY `url` (`url`),
  FULLTEXT KEY `name` (`name`,`description`,`url`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `elgg_sites_entity`
--

LOCK TABLES `elgg_sites_entity` WRITE;
/*!40000 ALTER TABLE `elgg_sites_entity` DISABLE KEYS */;
INSERT INTO `elgg_sites_entity` VALUES (1,'One Bad Place','','http://csrflabelgg.com/');
/*!40000 ALTER TABLE `elgg_sites_entity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `elgg_system_log`
--

DROP TABLE IF EXISTS `elgg_system_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `elgg_system_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `object_id` int(11) NOT NULL,
  `object_class` varchar(50) NOT NULL,
  `object_type` varchar(50) NOT NULL,
  `object_subtype` varchar(50) NOT NULL,
  `event` varchar(50) NOT NULL,
  `performed_by_guid` int(11) NOT NULL,
  `owner_guid` int(11) NOT NULL,
  `access_id` int(11) NOT NULL,
  `enabled` enum('yes','no') NOT NULL DEFAULT 'yes',
  `time_created` int(11) NOT NULL,
  `ip_address` varchar(46) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `object_id` (`object_id`),
  KEY `object_class` (`object_class`),
  KEY `object_type` (`object_type`),
  KEY `object_subtype` (`object_subtype`),
  KEY `event` (`event`),
  KEY `performed_by_guid` (`performed_by_guid`),
  KEY `access_id` (`access_id`),
  KEY `time_created` (`time_created`),
  KEY `river_key` (`object_type`,`object_subtype`,`event`)
) ENGINE=MyISAM AUTO_INCREMENT=72 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `elgg_system_log`
--

LOCK TABLES `elgg_system_log` WRITE;
/*!40000 ALTER TABLE `elgg_system_log` DISABLE KEYS */;
INSERT INTO `elgg_system_log` VALUES (1,2,'ElggPlugin','object','plugin','create',0,1,2,'yes',1510271899,'172.25.0.3'),(2,3,'ElggPlugin','object','plugin','create',0,1,2,'yes',1510271899,'172.25.0.3'),(3,4,'ElggPlugin','object','plugin','create',0,1,2,'yes',1510271899,'172.25.0.3'),(4,5,'ElggPlugin','object','plugin','create',0,1,2,'yes',1510271899,'172.25.0.3'),(5,6,'ElggPlugin','object','plugin','create',0,1,2,'yes',1510271899,'172.25.0.3'),(6,7,'ElggPlugin','object','plugin','create',0,1,2,'yes',1510271899,'172.25.0.3'),(7,8,'ElggPlugin','object','plugin','create',0,1,2,'yes',1510271899,'172.25.0.3'),(8,9,'ElggPlugin','object','plugin','create',0,1,2,'yes',1510271899,'172.25.0.3'),(9,10,'ElggPlugin','object','plugin','create',0,1,2,'yes',1510271899,'172.25.0.3'),(10,11,'ElggPlugin','object','plugin','create',0,1,2,'yes',1510271899,'172.25.0.3'),(11,12,'ElggPlugin','object','plugin','create',0,1,2,'yes',1510271899,'172.25.0.3'),(12,13,'ElggPlugin','object','plugin','create',0,1,2,'yes',1510271899,'172.25.0.3'),(13,14,'ElggPlugin','object','plugin','create',0,1,2,'yes',1510271899,'172.25.0.3'),(14,15,'ElggPlugin','object','plugin','create',0,1,2,'yes',1510271899,'172.25.0.3'),(15,16,'ElggPlugin','object','plugin','create',0,1,2,'yes',1510271899,'172.25.0.3'),(16,17,'ElggPlugin','object','plugin','create',0,1,2,'yes',1510271899,'172.25.0.3'),(17,18,'ElggPlugin','object','plugin','create',0,1,2,'yes',1510271899,'172.25.0.3'),(18,19,'ElggPlugin','object','plugin','create',0,1,2,'yes',1510271899,'172.25.0.3'),(19,20,'ElggPlugin','object','plugin','create',0,1,2,'yes',1510271899,'172.25.0.3'),(20,21,'ElggPlugin','object','plugin','create',0,1,2,'yes',1510271899,'172.25.0.3'),(21,22,'ElggPlugin','object','plugin','create',0,1,2,'yes',1510271899,'172.25.0.3'),(22,23,'ElggPlugin','object','plugin','create',0,1,2,'yes',1510271899,'172.25.0.3'),(23,24,'ElggPlugin','object','plugin','create',0,1,2,'yes',1510271899,'172.25.0.3'),(24,25,'ElggPlugin','object','plugin','create',0,1,2,'yes',1510271899,'172.25.0.3'),(25,26,'ElggPlugin','object','plugin','create',0,1,2,'yes',1510271899,'172.25.0.3'),(26,27,'ElggPlugin','object','plugin','create',0,1,2,'yes',1510271899,'172.25.0.3'),(27,28,'ElggPlugin','object','plugin','create',0,1,2,'yes',1510271899,'172.25.0.3'),(28,29,'ElggPlugin','object','plugin','create',0,1,2,'yes',1510271899,'172.25.0.3'),(29,30,'ElggPlugin','object','plugin','create',0,1,2,'yes',1510271899,'172.25.0.3'),(30,31,'ElggPlugin','object','plugin','create',0,1,2,'yes',1510271899,'172.25.0.3'),(31,32,'ElggPlugin','object','plugin','create',0,1,2,'yes',1510271899,'172.25.0.3'),(32,1,'ElggRelationship','relationship','active_plugin','create',0,0,2,'yes',1510271899,'172.25.0.3'),(33,23,'ElggRelationship','relationship','member_of_site','create',0,0,2,'yes',1510271931,'172.25.0.3'),(34,33,'ElggUser','user','','create',0,0,2,'yes',1510271931,'172.25.0.3'),(35,2,'ElggMetadata','metadata','notification:method:email','create',0,33,2,'yes',1510271931,'172.25.0.3'),(36,34,'ElggWidget','object','widget','create',0,33,0,'yes',1510271931,'172.25.0.3'),(37,35,'ElggWidget','object','widget','create',0,33,0,'yes',1510271931,'172.25.0.3'),(38,36,'ElggWidget','object','widget','create',0,33,0,'yes',1510271931,'172.25.0.3'),(39,37,'ElggWidget','object','widget','create',0,33,0,'yes',1510271931,'172.25.0.3'),(40,38,'ElggWidget','object','widget','create',0,33,0,'yes',1510271931,'172.25.0.3'),(41,33,'ElggUser','user','','make_admin',0,0,2,'yes',1510271931,'172.25.0.3'),(42,3,'ElggMetadata','metadata','validated','create',0,0,2,'yes',1510271931,'172.25.0.3'),(43,4,'ElggMetadata','metadata','validated_method','create',0,0,2,'yes',1510271931,'172.25.0.3'),(44,33,'ElggUser','user','','update',33,0,2,'yes',1510271931,'172.25.0.3'),(45,33,'ElggUser','user','','login',33,0,2,'yes',1510271931,'172.25.0.3'),(46,33,'ElggUser','user','','update',33,0,2,'yes',1510272591,'172.25.0.3'),(47,24,'ElggRelationship','relationship','member_of_site','create',33,0,2,'yes',1510272666,'172.25.0.3'),(48,39,'ElggUser','user','','create',33,0,2,'yes',1510272666,'172.25.0.3'),(49,5,'ElggMetadata','metadata','notification:method:email','create',33,39,2,'yes',1510272666,'172.25.0.3'),(50,39,'ElggUser','user','','update',33,0,2,'yes',1510272666,'172.25.0.3'),(51,6,'ElggMetadata','metadata','admin_created','create',33,39,2,'yes',1510272666,'172.25.0.3'),(52,7,'ElggMetadata','metadata','created_by_guid','create',33,39,2,'yes',1510272666,'172.25.0.3'),(53,25,'ElggRelationship','relationship','member_of_site','create',33,0,2,'yes',1510272705,'172.25.0.3'),(54,40,'ElggUser','user','','create',33,0,2,'yes',1510272705,'172.25.0.3'),(55,8,'ElggMetadata','metadata','notification:method:email','create',33,40,2,'yes',1510272705,'172.25.0.3'),(56,40,'ElggUser','user','','update',33,0,2,'yes',1510272705,'172.25.0.3'),(57,9,'ElggMetadata','metadata','admin_created','create',33,40,2,'yes',1510272705,'172.25.0.3'),(58,10,'ElggMetadata','metadata','created_by_guid','create',33,40,2,'yes',1510272705,'172.25.0.3'),(59,26,'ElggRelationship','relationship','member_of_site','create',33,0,2,'yes',1510272744,'172.25.0.3'),(60,41,'ElggUser','user','','create',33,0,2,'yes',1510272744,'172.25.0.3'),(61,11,'ElggMetadata','metadata','notification:method:email','create',33,41,2,'yes',1510272744,'172.25.0.3'),(62,41,'ElggUser','user','','update',33,0,2,'yes',1510272744,'172.25.0.3'),(63,12,'ElggMetadata','metadata','admin_created','create',33,41,2,'yes',1510272744,'172.25.0.3'),(64,13,'ElggMetadata','metadata','created_by_guid','create',33,41,2,'yes',1510272744,'172.25.0.3'),(65,27,'ElggRelationship','relationship','member_of_site','create',33,0,2,'yes',1510272762,'172.25.0.3'),(66,42,'ElggUser','user','','create',33,0,2,'yes',1510272762,'172.25.0.3'),(67,14,'ElggMetadata','metadata','notification:method:email','create',33,42,2,'yes',1510272762,'172.25.0.3'),(68,42,'ElggUser','user','','update',33,0,2,'yes',1510272762,'172.25.0.3'),(69,15,'ElggMetadata','metadata','admin_created','create',33,42,2,'yes',1510272762,'172.25.0.3'),(70,16,'ElggMetadata','metadata','created_by_guid','create',33,42,2,'yes',1510272762,'172.25.0.3'),(71,6,'ElggRelationship','relationship','active_plugin','delete',33,0,2,'yes',1510272992,'172.25.0.3');
/*!40000 ALTER TABLE `elgg_system_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `elgg_users_apisessions`
--

DROP TABLE IF EXISTS `elgg_users_apisessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `elgg_users_apisessions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_guid` bigint(20) unsigned NOT NULL,
  `site_guid` bigint(20) unsigned NOT NULL,
  `token` varchar(40) DEFAULT NULL,
  `expires` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_guid` (`user_guid`,`site_guid`),
  KEY `token` (`token`)
) ENGINE=MEMORY DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `elgg_users_apisessions`
--

LOCK TABLES `elgg_users_apisessions` WRITE;
/*!40000 ALTER TABLE `elgg_users_apisessions` DISABLE KEYS */;
/*!40000 ALTER TABLE `elgg_users_apisessions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `elgg_users_entity`
--

DROP TABLE IF EXISTS `elgg_users_entity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `elgg_users_entity` (
  `guid` bigint(20) unsigned NOT NULL,
  `name` text NOT NULL,
  `username` varchar(128) NOT NULL DEFAULT '',
  `password` varchar(32) NOT NULL DEFAULT '',
  `salt` varchar(8) NOT NULL DEFAULT '',
  `email` text NOT NULL,
  `language` varchar(6) NOT NULL DEFAULT '',
  `code` varchar(32) NOT NULL DEFAULT '',
  `banned` enum('yes','no') NOT NULL DEFAULT 'no',
  `admin` enum('yes','no') NOT NULL DEFAULT 'no',
  `last_action` int(11) NOT NULL DEFAULT '0',
  `prev_last_action` int(11) NOT NULL DEFAULT '0',
  `last_login` int(11) NOT NULL DEFAULT '0',
  `prev_last_login` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`guid`),
  UNIQUE KEY `username` (`username`),
  KEY `password` (`password`),
  KEY `email` (`email`(50)),
  KEY `code` (`code`),
  KEY `last_action` (`last_action`),
  KEY `last_login` (`last_login`),
  KEY `admin` (`admin`),
  FULLTEXT KEY `name` (`name`),
  FULLTEXT KEY `name_2` (`name`,`username`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `elgg_users_entity`
--

LOCK TABLES `elgg_users_entity` WRITE;
/*!40000 ALTER TABLE `elgg_users_entity` DISABLE KEYS */;
INSERT INTO `elgg_users_entity` VALUES (33,'admin','admin','db4c8540eccd3f55fe0bf4dad0233052','syg7q84p','admin@here.com','en','','no','yes',1510273098,1510272993,1510271931,0),(39,'Alice','alice','028570fdf46d1e003090bdaa992b427c','Iedyj_S4','here@there.com','en','','no','no',0,0,0,0),(40,'Boby','boby','072e47d0d896eca1a6d23bbf41c80f93','jbHSKzlH','boby@seed.here','en','','no','no',0,0,0,0),(41,'Charlie','charlie','fd63939acf7b768044f1b4cb2bffab0e','I7SUvzWB','here@there.com','en','','no','no',0,0,0,0),(42,'Samy','samy','04500a568d3009d15aae00debb337efd','swwfxCpQ','sam@sam.com','en','','no','no',0,0,0,0);
/*!40000 ALTER TABLE `elgg_users_entity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `elgg_users_sessions`
--

DROP TABLE IF EXISTS `elgg_users_sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `elgg_users_sessions` (
  `session` varchar(255) NOT NULL,
  `ts` int(11) unsigned NOT NULL DEFAULT '0',
  `data` mediumblob,
  PRIMARY KEY (`session`),
  KEY `ts` (`ts`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `elgg_users_sessions`
--

LOCK TABLES `elgg_users_sessions` WRITE;
/*!40000 ALTER TABLE `elgg_users_sessions` DISABLE KEYS */;
INSERT INTO `elgg_users_sessions` VALUES ('voc1glcpnncnofpfkidn494oq4',1510273098,'__elgg_session|s:32:\"e339c72c0c1e16779f5f57a909be83de\";user|O:8:\"ElggUser\":8:{s:15:\"\0*\0url_override\";N;s:16:\"\0*\0icon_override\";N;s:16:\"\0*\0temp_metadata\";a:0:{}s:19:\"\0*\0temp_annotations\";a:0:{}s:24:\"\0*\0temp_private_settings\";a:0:{}s:11:\"\0*\0volatile\";a:0:{}s:13:\"\0*\0attributes\";a:25:{s:4:\"guid\";i:33;s:4:\"type\";s:4:\"user\";s:7:\"subtype\";s:1:\"0\";s:10:\"owner_guid\";s:1:\"0\";s:9:\"site_guid\";s:1:\"1\";s:14:\"container_guid\";s:1:\"0\";s:9:\"access_id\";s:1:\"2\";s:12:\"time_created\";s:10:\"1510271931\";s:12:\"time_updated\";s:10:\"1510272591\";s:11:\"last_action\";s:10:\"1510272993\";s:7:\"enabled\";s:3:\"yes\";s:12:\"tables_split\";i:2;s:13:\"tables_loaded\";i:2;s:4:\"name\";s:5:\"admin\";s:8:\"username\";s:5:\"admin\";s:8:\"password\";s:32:\"db4c8540eccd3f55fe0bf4dad0233052\";s:4:\"salt\";s:8:\"syg7q84p\";s:5:\"email\";s:14:\"admin@here.com\";s:8:\"language\";s:2:\"en\";s:4:\"code\";s:0:\"\";s:6:\"banned\";s:2:\"no\";s:5:\"admin\";s:3:\"yes\";s:16:\"prev_last_action\";s:10:\"1510272992\";s:10:\"last_login\";s:10:\"1510271931\";s:15:\"prev_last_login\";s:1:\"0\";}s:8:\"\0*\0valid\";b:0;}guid|i:33;id|i:33;username|s:5:\"admin\";name|s:5:\"admin\";msg|a:0:{}sticky_forms|a:0:{}');
/*!40000 ALTER TABLE `elgg_users_sessions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-11-10  0:18:43
