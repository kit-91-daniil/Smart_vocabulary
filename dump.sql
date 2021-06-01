-- MySQL dump 10.13  Distrib 5.7.30, for Win64 (x86_64)
--
-- Host: localhost    Database: my_project
-- ------------------------------------------------------
-- Server version	5.7.30-log
USE my_project;
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
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('e9c8b3ae9bd7');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interval_words`
--

DROP TABLE IF EXISTS `interval_words`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `interval_words` (
  `user_id` int(11) NOT NULL,
  `word_id` int(11) NOT NULL,
  `addition_time` datetime NOT NULL,
  `repeating_time` datetime DEFAULT NULL,
  `time_to_repeat` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`user_id`,`word_id`),
  KEY `word_id` (`word_id`),
  CONSTRAINT `interval_words_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `interval_words_ibfk_2` FOREIGN KEY (`word_id`) REFERENCES `vocabulary` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interval_words`
--

LOCK TABLES `interval_words` WRITE;
/*!40000 ALTER TABLE `interval_words` DISABLE KEYS */;
INSERT INTO `interval_words` VALUES (1,3,'2020-12-13 18:36:43','2021-05-29 14:34:20',3524762,7),(1,4,'2020-12-13 18:36:43','2021-06-05 07:16:58',4103320,7),(1,7,'2020-12-13 18:36:43','2021-05-16 15:18:25',2404207,7),(1,8,'2020-12-13 18:36:43','2021-05-29 21:18:40',3549022,7),(1,11,'2020-12-13 18:36:43','2021-05-29 21:14:38',3548780,7),(1,14,'2020-12-13 18:36:43','2021-05-29 21:15:14',3548816,7),(1,15,'2020-12-13 18:36:43','2021-05-29 21:16:18',3548880,7),(1,17,'2020-12-13 18:36:43','2021-05-16 18:18:56',2415038,7),(1,21,'2020-12-13 18:36:43','2021-05-17 14:45:27',2488629,7),(1,22,'2020-12-13 18:36:43','2021-06-05 07:16:53',4103315,7),(1,23,'2020-12-13 18:36:43','2021-05-29 21:14:43',3548785,7),(1,26,'2020-12-13 18:36:43','2021-06-05 07:13:01',4103083,7),(1,27,'2020-12-13 18:36:43','2021-05-29 14:35:59',3524861,7),(1,29,'2020-12-13 18:36:43','2021-05-29 14:39:34',3525076,7),(1,30,'2020-12-13 18:36:43','2021-06-05 07:13:23',4103105,7),(1,32,'2020-12-13 18:44:29','2021-06-05 07:15:46',4103248,7),(1,33,'2020-12-13 18:44:29','2021-05-17 15:07:37',2489959,7),(1,34,'2020-12-13 18:44:29','2021-06-04 14:22:20',4042442,7),(1,36,'2020-12-13 18:44:29','2021-05-16 15:18:36',2404218,7),(1,37,'2020-12-13 18:44:29','2021-06-05 07:16:27',4103289,7),(1,38,'2020-12-13 18:44:29','2021-05-29 21:16:55',3548917,7),(1,39,'2020-12-13 18:44:29','2021-05-16 18:20:39',2415141,7),(1,40,'2020-12-13 18:44:29','2021-05-29 21:15:52',3548854,7),(1,42,'2020-12-13 18:44:29','2021-05-29 14:34:33',3524775,7),(1,43,'2020-12-13 18:44:29','2021-05-29 14:37:39',3524961,7),(1,44,'2020-12-13 18:44:29','2021-05-16 18:15:42',2414844,7),(1,45,'2020-12-13 18:44:29','2021-05-29 21:18:06',3548988,7),(1,46,'2020-12-13 18:44:29','2021-06-04 07:41:44',4018406,7),(1,47,'2020-12-13 18:44:29','2021-05-29 21:16:22',3548884,7),(1,48,'2020-12-13 18:44:29','2021-06-04 14:22:36',4042458,7),(1,49,'2020-12-13 18:44:29','2021-06-05 07:14:12',4103154,7),(1,50,'2020-12-13 18:44:29','2021-05-16 15:18:00',2404182,7),(1,51,'2020-12-13 18:44:29','2021-05-29 21:18:15',3548997,7),(1,52,'2020-12-14 19:17:55','2021-05-29 21:18:10',3548992,7),(1,53,'2020-12-14 19:17:55','2021-05-29 14:35:32',3524834,7),(1,54,'2020-12-14 19:17:55','2021-06-05 07:12:20',4103042,7),(1,56,'2020-12-14 19:17:55','2021-06-04 07:46:05',4018667,7),(1,57,'2020-12-14 19:17:55','2021-05-16 15:18:42',2404224,7),(1,59,'2020-12-14 19:17:55','2021-05-29 14:34:55',3524797,7),(1,61,'2020-12-14 19:17:55','2021-05-17 14:49:19',2488861,7),(1,62,'2020-12-14 19:17:55','2021-05-17 15:05:51',2489853,7),(1,63,'2020-12-14 19:17:55','2021-05-29 21:18:21',3549003,7),(1,64,'2020-12-14 19:17:55','2021-05-29 21:19:07',3549049,7),(1,67,'2020-12-14 19:17:55','2021-05-16 18:04:59',2414201,7),(1,70,'2020-12-14 19:17:55','2021-06-04 14:24:03',4042545,7),(1,71,'2020-12-14 19:17:55','2021-05-29 14:38:40',3525022,7),(1,72,'2020-12-14 19:17:55','2021-05-29 21:17:08',3548930,7),(1,73,'2020-12-14 19:17:55','2021-05-29 21:16:12',3548874,7),(1,74,'2020-12-14 19:17:55','2021-05-29 21:19:15',3549057,7),(1,79,'2020-12-18 18:48:51','2021-06-04 07:41:35',4018397,7),(1,80,'2020-12-18 18:48:51','2021-05-16 18:17:40',2414962,7),(1,81,'2020-12-18 18:48:51','2021-06-05 07:14:40',4103182,7),(1,82,'2020-12-18 18:48:51','2021-05-17 14:50:56',2488958,7),(1,84,'2020-12-18 18:48:51','2021-05-29 14:39:01',3525043,7),(1,85,'2020-12-18 18:48:51','2021-05-29 21:16:34',3548896,7),(1,86,'2020-12-18 18:48:51','2021-05-16 15:17:53',2404175,7),(1,89,'2020-12-18 18:48:51','2021-05-29 21:16:30',3548892,7),(1,90,'2020-12-18 18:48:51','2021-06-05 07:13:08',4103090,7),(1,91,'2020-12-18 18:48:51','2021-05-29 21:15:07',3548809,7),(1,92,'2020-12-18 18:48:51','2021-06-05 07:14:20',4103162,7),(1,93,'2020-12-18 18:48:51','2021-05-29 21:16:43',3548905,7),(1,94,'2020-12-18 18:48:51','2021-05-29 21:16:08',3548870,7),(1,95,'2020-12-18 18:48:51','2021-06-04 14:21:59',4042421,7),(1,96,'2020-12-18 18:48:51','2021-05-17 14:49:52',2488894,7),(1,97,'2020-12-18 18:48:51','2021-05-29 21:16:39',3548901,7),(1,98,'2020-12-18 18:48:51','2021-05-29 14:35:07',3524809,7),(1,99,'2020-12-18 18:48:51','2021-06-05 07:13:56',4103138,7),(1,104,'2020-12-19 08:36:56','2021-05-29 14:34:46',3524788,7),(1,106,'2020-12-19 08:36:56','2021-05-17 14:58:23',2489405,7),(1,107,'2020-12-19 08:36:56','2021-05-29 14:37:31',3524953,7),(1,108,'2020-12-19 08:36:56','2021-05-29 21:18:51',3549033,7),(1,109,'2020-12-19 08:36:56','2021-06-05 07:14:52',4103194,7),(1,110,'2020-12-19 08:36:56','2021-05-16 15:25:39',2404641,7),(1,111,'2020-12-19 08:36:56','2021-05-29 21:17:59',3548981,7),(1,113,'2020-12-19 08:36:56','2021-05-17 15:08:39',2490021,7),(1,114,'2020-12-19 08:36:56','2021-05-29 21:19:33',3549075,7),(1,115,'2020-12-19 08:36:56','2021-06-05 07:12:54',4103076,7),(1,117,'2020-12-19 08:36:56','2021-06-04 07:44:52',4018594,7),(1,118,'2020-12-19 08:36:56','2021-05-29 21:18:45',3549027,7),(1,119,'2020-12-19 08:36:56','2021-06-04 14:22:56',4042478,7),(1,120,'2020-12-19 08:36:56','2021-06-04 07:41:10',4018372,7),(1,121,'2020-12-19 08:36:56','2021-06-04 07:37:30',4018152,7),(1,122,'2020-12-19 08:36:56','2021-05-29 21:15:33',3548835,7),(1,123,'2020-12-19 08:36:56','2021-05-17 15:09:06',2490048,7),(1,124,'2020-12-19 08:36:56','2021-06-05 07:15:55',4103257,7),(1,125,'2020-12-19 08:36:56','2021-05-29 21:19:22',3549064,7),(1,127,'2020-12-19 15:55:59','2021-06-05 07:16:06',4103268,7),(1,128,'2021-01-08 09:37:02','2021-05-29 14:38:09',3524991,7),(1,130,'2021-01-17 10:49:35','2021-06-04 07:42:11',4018433,7),(1,131,'2021-01-17 10:50:10','2021-05-29 14:38:52',3525034,7),(1,132,'2021-01-17 10:50:28','2021-05-29 21:14:48',3548790,7),(1,133,'2021-01-17 10:50:40','2021-06-04 07:44:26',4018568,7),(1,134,'2021-01-17 10:50:56','2021-05-29 21:17:44',3548966,7),(1,135,'2021-01-17 10:51:11','2021-05-29 21:17:21',3548943,7),(1,136,'2021-01-17 10:51:29','2021-05-29 14:36:13',3524875,7),(1,137,'2021-01-17 10:51:46','2021-05-29 21:16:51',3548913,7),(1,138,'2021-01-17 10:52:01','2021-05-29 21:19:01',3549043,7),(1,139,'2021-01-17 10:53:22','2021-05-29 14:37:20',3524942,7),(1,141,'2021-01-17 10:53:56','2021-05-29 14:38:26',3525008,7),(1,142,'2021-01-17 10:54:09','2021-06-05 07:14:31',4103173,7),(1,143,'2021-01-17 10:54:21','2021-05-29 14:35:23',3524825,7),(1,144,'2021-01-17 10:54:35','2021-06-04 07:46:16',4018678,7),(1,145,'2021-01-17 10:54:54','2021-05-29 21:19:39',3549081,7),(1,147,'2021-01-17 10:55:56','2021-05-29 21:18:34',3549016,7),(1,148,'2021-01-17 10:56:10','2021-06-05 07:19:09',4103451,7),(1,149,'2021-01-17 10:56:27','2021-06-05 07:12:38',4103060,7),(1,150,'2021-01-17 10:56:38','2021-06-05 07:15:39',4103241,7),(1,151,'2021-01-17 10:56:56','2021-05-29 14:37:50',3524972,7),(1,152,'2021-01-17 10:49:54','2021-06-04 07:42:23',4018445,7),(1,153,'2021-01-17 10:53:42','2021-06-04 07:41:59',4018421,7),(1,154,'2021-01-17 10:55:41','2021-06-05 07:16:15',4103277,7),(1,155,'2021-02-01 04:52:23','2021-06-17 19:07:57',5182779,7),(1,156,'2021-02-01 04:52:53','2021-06-17 19:08:29',5182811,7),(1,157,'2021-02-01 04:53:02','2021-06-17 19:02:26',5182448,7),(1,158,'2021-02-01 04:53:15','2021-06-17 19:07:26',5182748,7),(1,159,'2021-02-01 04:53:26','2021-06-17 19:05:52',5182654,7),(1,160,'2021-02-01 04:53:45','2021-06-17 19:07:33',5182755,7),(1,161,'2021-02-01 04:54:02','2021-06-17 19:06:32',5182694,7),(1,162,'2021-02-01 04:54:16','2021-06-17 19:03:18',5182500,7),(1,163,'2021-02-01 04:54:28','2021-06-17 19:01:49',5182411,7),(1,164,'2021-02-01 04:54:37','2021-06-17 19:03:54',5182536,7),(1,165,'2021-02-01 04:54:46','2021-06-17 19:05:58',5182660,7),(1,166,'2021-02-01 04:54:59','2021-06-17 19:06:39',5182701,7),(1,167,'2021-02-01 04:55:08','2021-06-17 19:05:26',5182628,7),(1,168,'2021-02-01 04:55:25','2021-06-17 19:03:25',5182507,7),(1,169,'2021-02-01 04:55:36','2021-06-17 19:07:40',5182762,7),(1,170,'2021-02-01 04:55:46','2021-06-17 19:02:20',5182442,7),(1,171,'2021-02-01 04:56:01','2021-06-17 19:01:56',5182418,7),(1,172,'2021-02-01 04:56:11','2021-06-17 19:08:08',5182790,7),(1,173,'2021-02-01 04:56:20','2021-06-17 19:04:23',5182565,7),(1,174,'2021-02-02 04:37:45','2021-06-17 19:02:09',5182431,7),(1,175,'2021-02-02 04:37:59','2021-06-17 19:06:47',5182709,7),(1,177,'2021-02-23 11:43:23','2021-05-05 07:47:05',1426727,6),(1,178,'2021-02-23 11:43:41','2021-05-05 14:21:08',1450370,6),(1,179,'2021-02-23 11:43:56','2021-05-06 07:17:59',1511381,6),(1,180,'2021-02-23 11:44:13','2021-05-05 14:20:54',1450356,6),(1,181,'2021-02-23 11:44:33','2021-05-06 07:17:28',1511350,6),(1,182,'2021-02-23 11:55:21','2021-05-06 07:17:15',1511337,6),(1,183,'2021-02-23 11:45:57','2021-05-05 14:21:47',1450409,6),(1,184,'2021-02-23 11:46:15','2021-05-05 14:23:54',1450536,6),(1,185,'2021-02-23 11:46:33','2021-05-06 07:14:07',1511149,6),(1,186,'2021-02-23 11:46:47','2021-05-05 07:44:34',1426576,6),(1,187,'2021-02-23 11:48:19','2021-05-06 07:17:35',1511357,6),(1,188,'2021-02-23 11:49:19','2021-05-06 07:19:20',1511462,6),(1,190,'2021-02-23 11:49:35','2021-05-05 14:24:09',1450551,6),(1,191,'2021-02-23 11:50:56','2021-05-05 07:44:42',1426584,6),(1,194,'2021-03-02 11:24:21','2021-05-06 07:17:22',1511344,6),(1,195,'2021-03-01 18:03:47','2021-05-05 07:40:53',1426355,6),(1,196,'2021-03-01 18:16:50','2021-05-06 07:12:47',1511069,6),(1,197,'2021-03-01 18:19:09','2021-05-05 07:45:56',1426658,6),(1,198,'2021-03-09 11:05:37','2021-05-18 19:02:46',2590468,6),(1,199,'2021-03-09 11:05:38','2021-05-18 19:07:00',2590722,6),(1,200,'2021-03-09 11:05:39','2021-05-18 19:03:05',2590487,6),(1,201,'2021-03-09 11:05:40','2021-05-18 19:08:03',2590785,6),(1,202,'2021-03-09 11:05:41','2021-05-18 19:02:14',2590436,6),(1,203,'2021-03-09 11:05:43','2021-05-18 19:03:59',2590541,6),(1,204,'2021-03-09 11:05:43','2021-05-18 19:04:15',2590557,6),(1,205,'2021-03-09 11:05:45','2021-05-18 19:01:30',2590392,6),(1,206,'2021-03-09 11:05:46','2021-05-18 19:01:43',2590405,6),(1,207,'2021-03-09 11:05:47','2021-05-18 19:04:36',2590578,6),(1,208,'2021-03-09 11:05:48','2021-05-18 19:08:15',2590797,6),(1,209,'2021-03-09 11:05:49','2021-05-18 19:07:18',2590740,6),(1,210,'2021-03-09 11:05:50','2021-05-18 19:02:03',2590425,6),(1,211,'2021-03-09 11:05:51','2021-05-18 19:03:33',2590515,6),(1,212,'2021-03-09 11:05:52','2021-05-18 19:04:31',2590573,6),(1,214,'2021-03-21 12:07:15','2021-04-21 07:13:48',215130,5),(1,215,'2021-03-21 12:07:00','2021-04-20 07:46:28',130690,5),(1,216,'2021-03-21 12:06:49','2021-04-21 07:19:28',215470,5),(1,217,'2021-04-18 16:28:18','2021-04-18 23:28:14',14396,1);
/*!40000 ALTER TABLE `interval_words` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `learned_words`
--

DROP TABLE IF EXISTS `learned_words`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `learned_words` (
  `user_id` int(11) NOT NULL,
  `word_id` int(11) NOT NULL,
  `addition_time` datetime NOT NULL,
  PRIMARY KEY (`user_id`,`word_id`),
  KEY `word_id` (`word_id`),
  CONSTRAINT `learned_words_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `learned_words_ibfk_2` FOREIGN KEY (`word_id`) REFERENCES `vocabulary` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `learned_words`
--

LOCK TABLES `learned_words` WRITE;
/*!40000 ALTER TABLE `learned_words` DISABLE KEYS */;
INSERT INTO `learned_words` VALUES (1,1,'2020-12-19 17:20:44'),(1,41,'2021-03-14 20:29:17'),(1,105,'2021-03-30 14:31:45'),(2,1,'2020-12-13 18:56:31');
/*!40000 ALTER TABLE `learned_words` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (4,'student','Just learn English and worry nothing, may change email'),(5,'editor','allowed to correct the words-translations'),(6,'administrator','full access');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles_users`
--

DROP TABLE IF EXISTS `roles_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `roles_users` (
  `user_id` int(11) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  KEY `user_id` (`user_id`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `roles_users_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `roles_users_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles_users`
--

LOCK TABLES `roles_users` WRITE;
/*!40000 ALTER TABLE `roles_users` DISABLE KEYS */;
INSERT INTO `roles_users` VALUES (1,4),(1,6),(3,4),(4,4);
/*!40000 ALTER TABLE `roles_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'dan2@mail.ru','$2b$12$JVSyUJlXV1cOgqFoWf8.n.6/OC/.Ot2p9PbvT3Xp/46V9LYWgRG9u',1),(2,'coder@mail.ru','$2b$12$fkojtr.FAwCJViOZQteZVe0Phh7InWumVgnm0In307kbKUxRe55Ba',1),(3,'new_user1@mail.ru','$2b$12$w6RRTGLRtLmir4C.Y2GRC.ge2iDzn8m6sIiiTPb71l38HSpQ/R1te',1),(4,'new_user2@mail.ru','$2b$12$2/DBru0rLLostO3pj8RpxesbiwZPdxv00uLYRPfCZUrIpzVg8i.D.',1);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vocabulary`
--

DROP TABLE IF EXISTS `vocabulary`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vocabulary` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `word` varchar(40) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `translation` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `word` (`word`)
) ENGINE=InnoDB AUTO_INCREMENT=222 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vocabulary`
--

LOCK TABLES `vocabulary` WRITE;
/*!40000 ALTER TABLE `vocabulary` DISABLE KEYS */;
INSERT INTO `vocabulary` VALUES (1,'custom','индивидуальный'),(3,'involve','содержит'),(4,'man','мужчина'),(7,'science','наука'),(8,'sugar','сахара'),(11,'nice','красивый'),(14,'to require','требовать'),(15,'a noon','полдень'),(17,'to examine','исследовать'),(21,'branch','ответвление'),(22,'to evolve','улучшаться'),(23,'separately','отдельно'),(24,'separate','отдельный'),(26,'conciling','примирение'),(27,'simultaneously','одновременно'),(29,'to refer','направить'),(30,'inherent','присущий'),(31,'facilities','станции'),(32,'facility','возможности'),(33,'occasionally','иногда'),(34,'discourage','отговаривать'),(36,'merge','слияние'),(37,'relying','полагаясь'),(38,'rather','скорее'),(39,'undoing','отмена'),(40,'coherent','Когерентный'),(41,'to permit','разрешить'),(42,'several','несколько'),(43,'contribution','вклад'),(44,'collaborate','совместно работать'),(45,'enormously','чрезвычайно'),(46,'among','между'),(47,'overall','общий'),(48,'behind','сзади'),(49,'scale','шкала'),(50,'introduction','вступление'),(51,'goal','цель'),(52,'reference','ссылка'),(53,'extensive','обширный'),(54,'peruse','читать'),(56,'mentioned','упомянутый'),(57,'wealth','богатство'),(59,'streamline','упростить'),(61,'explicitly','явно'),(62,'omission','замалчивание'),(63,'describe','описывать'),(64,'briefly','Кратко'),(67,'exhausetive','исчерпывающий'),(70,'occure','происходить'),(71,'prevent','предотвратить'),(72,'quote','ставку'),(73,'snapshot','снимок'),(74,'comprise','состоять из'),(75,'nest','вложить'),(76,'to precede','предшествовать'),(77,'release','предохранительный'),(78,'initial','начальный'),(79,'proceed','продолжать'),(80,'denote','сообщить'),(81,'respect','уважение'),(82,'tip','совет'),(84,'overlap','наложение'),(85,'apart','кроме'),(86,'regard','С уважением'),(89,'electrical','электрическое'),(90,'smoothly','замедленно'),(91,'approach','подход'),(92,'explicit','искренний'),(93,'effort','усилие'),(94,'complicated','сложный'),(95,'to maintain','поддерживать'),(96,'to implement','осуществлять'),(97,'polished','полированный'),(98,'drawback','недостаток'),(99,'credential','учетные данные'),(100,'realm','область'),(101,'influence','влияние'),(102,'sign','подпись'),(103,'provide','предоставлять'),(104,'configure','настраивать'),(105,'entirely','полностью'),(106,'to handle','обрабатывать'),(107,'granular','зернистый'),(108,'to achieve','достигать'),(109,'to retrieve','извлечь'),(110,'to supply','обеспечить'),(111,'to mitigate','смягчить'),(113,'accept','принимать'),(114,'to assign','присваивать'),(115,'to assume','предполагать'),(117,'to bear in mind','иметь ввиду'),(118,'a breach','нарушение'),(119,'certain','уверенный'),(120,'certainly','конечно'),(121,'circumstance','обстоятельство'),(122,'complexity','сложность'),(123,'completely','полностью'),(124,'to contribute','способствовать'),(125,'to appreciate','оценивать'),(127,'entity','сущность'),(128,'unambigous','однозначный'),(129,'expose','выставлять'),(130,'to fulfill','выполнить'),(131,'to further','продвигать'),(132,'prone','склонный'),(133,'obvious','очевидный'),(134,'to originate','создавать'),(135,'to appear','казаться'),(136,'to affect','влиять'),(137,'to appropriate','присвоить'),(138,'ultimately','в конечном итоге'),(139,'conclusion','заключение'),(140,'exhibit','выставлять'),(141,'to arise','возникать'),(142,'intact','неповрежденный'),(143,'conjuction','соединение'),(144,'to strive','прилагать усилия'),(145,'though','тем не менее'),(146,'unintentially','непреднамеренный'),(147,'within','внутри'),(148,'to leave up','обращаться'),(149,'along','вдоль'),(150,'therefore','следовательно'),(151,'redundant','избыточный'),(152,'to expose','выставлять'),(153,'to exhibit','выставлять'),(154,'unintentionally','непреднамеренно'),(155,'to expand','расширять'),(156,'advantage','преимущество'),(157,'demand','потребность'),(158,'to suggest','предложить'),(159,'to lounge','бездельничать'),(160,'to quench','утолять'),(161,'to lure','завлекать'),(162,'fabulous','сказочный'),(163,'gorgeous','роскошный'),(164,'tan','загар'),(165,'leisure','досуг'),(166,'layout','макет'),(167,'perhaps','может быть'),(168,'possibly','возможно'),(169,'probably','вероятно'),(170,'fortunately','к счастью'),(171,'unfortunately','к сожалению'),(172,'definitly','точно'),(173,'actually','на самом деле'),(174,'importance','важность'),(175,'to seek','стремиться'),(176,'conjugate','сопрягать'),(177,'approximately','приблизительно'),(178,'beforehand','заранее'),(179,'deliberately','умышленно'),(180,'frankly','откровенно'),(181,'gradually','постепенно'),(182,'incredibly','невероятно'),(183,'instantly','немедленно'),(184,'jointly','вместе'),(185,'nevertheless','тем не менее'),(186,'partly','частично'),(187,'precisely','определенно'),(188,'regardless','несмотря ни на что'),(189,'relatively','относительно'),(190,'slightly','немного'),(191,'utterly','крайне'),(194,'polite','вежливый'),(195,'adorable','милый'),(196,'embalished','украшен'),(197,'wardrobe','гардероб'),(198,'disease','болезнь'),(199,'symptom','симптом'),(200,'bleeding','кровотечение'),(201,'tiredness','усталость'),(202,'sneezing','чихание'),(203,'lightning','молния'),(204,'nerve','нерв'),(205,'elbow','локоть'),(206,'cramping pain','спазматическая боль'),(207,'cramp','спазм'),(208,'mild pain','слабая боль'),(209,'moderate pain','умеренная боль'),(210,'severe pain','сильная боль'),(211,'shooting pain','стреляющая боль'),(212,'tearing pain','раздирающая боль'),(214,'against','против'),(215,'relevant','соответствующий'),(216,'aware','осведомленный'),(217,'alternately','попеременно'),(218,'to get along','ладить'),(219,'goal-oriented','целенаправленный'),(220,'furthermore','более того'),(221,'competitive','конкурентный');
/*!40000 ALTER TABLE `vocabulary` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `words`
--

DROP TABLE IF EXISTS `words`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `words` (
  `user_id` int(11) NOT NULL,
  `word_id` int(11) NOT NULL,
  `addition_time` datetime NOT NULL,
  PRIMARY KEY (`user_id`,`word_id`),
  KEY `word_id` (`word_id`),
  CONSTRAINT `words_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `words_ibfk_2` FOREIGN KEY (`word_id`) REFERENCES `vocabulary` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `words`
--

LOCK TABLES `words` WRITE;
/*!40000 ALTER TABLE `words` DISABLE KEYS */;
INSERT INTO `words` VALUES (1,1,'2021-02-26 09:30:56'),(1,3,'2021-02-27 09:39:20'),(1,51,'2021-03-13 16:28:56'),(1,121,'2021-02-28 10:27:51'),(1,182,'2021-02-22 18:46:26'),(1,200,'2021-03-07 20:00:18');
/*!40000 ALTER TABLE `words` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-05-12  7:00:36
