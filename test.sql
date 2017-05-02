/*
SQLyog Trial v12.12 (64 bit)
MySQL - 5.5.34 : Database - weido
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`weido` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `weido`;

/*Table structure for table `hotword` */

DROP TABLE IF EXISTS `hotword`;

CREATE TABLE `hotword` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `keyword` varchar(40) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `type` int(11) DEFAULT NULL COMMENT '类别',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

/*Table structure for table `type` */

DROP TABLE IF EXISTS `type`;

CREATE TABLE `type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` varchar(40) DEFAULT NULL COMMENT 'value',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

/*Table structure for table `wd_article` */

DROP TABLE IF EXISTS `wd_article`;

CREATE TABLE `wd_article` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `article_title` varchar(40) DEFAULT NULL COMMENT '文章标题',
  `article_desc` varchar(200) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '文章描述',
  `account_name` varchar(40) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '公众号名称',
  `article_head` varchar(300) DEFAULT NULL COMMENT '图片',
  `article_url` varchar(500) DEFAULT NULL COMMENT '文章地址',
  `account_logo` varchar(300) DEFAULT NULL COMMENT '公众号LOGO',
  `openid` varchar(60) DEFAULT NULL COMMENT '公众账号',
  `ext` varchar(300) DEFAULT NULL COMMENT '扩展请求',
  `doc_id` varchar(80) DEFAULT NULL,
  `tpl_id` int(11) DEFAULT NULL COMMENT '类型ID',
  `class_id` int(11) DEFAULT NULL,
  `visit_times` int(11) DEFAULT NULL COMMENT '访问次数',
  `publish_time` datetime DEFAULT NULL COMMENT '发布时间',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

/*Table structure for table `wd_article_hot` */

DROP TABLE IF EXISTS `wd_article_hot`;

CREATE TABLE `wd_article_hot` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `article_title` varchar(40) DEFAULT NULL COMMENT '文章标题',
  `article_desc` varchar(200) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '文章描述',
  `account_name` varchar(40) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '公众号名称',
  `article_head` varchar(300) DEFAULT NULL COMMENT '图片',
  `article_url` varchar(500) DEFAULT NULL COMMENT '文章地址',
  `account_logo` varchar(300) DEFAULT NULL COMMENT '公众号LOGO',
  `openid` varchar(60) DEFAULT NULL COMMENT '公众账号',
  `ext` varchar(150) DEFAULT NULL COMMENT '扩展请求',
  `doc_id` varchar(80) DEFAULT NULL,
  `tpl_id` int(11) DEFAULT NULL COMMENT '类型ID',
  `class_id` int(11) DEFAULT NULL,
  `visit_times` int(11) DEFAULT NULL COMMENT '访问次数',
  `publish_time` datetime DEFAULT NULL COMMENT '发布时间',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8;

/*Table structure for table `wd_public_account` */

DROP TABLE IF EXISTS `wd_public_account`;

CREATE TABLE `wd_public_account` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `account` varchar(30) DEFAULT NULL COMMENT '账号',
  `name` varchar(20) DEFAULT NULL COMMENT '名称',
  `openid` varchar(60) DEFAULT NULL COMMENT 'openid',
  `ext` varchar(150) DEFAULT NULL COMMENT '扩展',
  `hotkey` varchar(20) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '热词',
  `logo` varchar(300) DEFAULT NULL,
  `type` int(11) DEFAULT NULL COMMENT '大分类',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=119 DEFAULT CHARSET=utf8 COMMENT='公众号';

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
