/*
SQLyog Ultimate v13.1.1 (64 bit)
MySQL - 10.4.24-MariaDB : Database - login_users
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`login_users` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `login_users`;

/*Table structure for table `login_users` */

DROP TABLE IF EXISTS `login_users`;

CREATE TABLE `login_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `phone` int(10) NOT NULL,
  `description` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `image` text NOT NULL,
  `status` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4;

/*Data for the table `login_users` */

insert  into `login_users`(`id`,`username`,`email`,`password`,`phone`,`description`,`address`,`image`,`status`) values 
(8,'jean','jeanzambrano2020@itp.edu.co','24fa7932432756103d3090f9f4afc3ec255979968c426f326eaba9b6b5cc344e',1111111111,'venta de chisme','el chiste','/static/cambiar_avatar/abou.jpg','1'),
(16,'lis','inspiratedylarky@gmail.com','24fa7932432756103d3090f9f4afc3ec255979968c426f326eaba9b6b5cc344e',666666,'mocoa-riding','mocoa','/static/cambiar_avatar/ima.jpg','1');

/*Table structure for table `productos` */

DROP TABLE IF EXISTS `productos`;

CREATE TABLE `productos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `descripción` varchar(255) NOT NULL,
  `precio` varchar(255) NOT NULL,
  `estado` varchar(255) NOT NULL,
  `imagen` text NOT NULL,
  `id_user` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `productos_usuarios_fk` (`id_user`),
  CONSTRAINT `productos_usuarios_fk` FOREIGN KEY (`id_user`) REFERENCES `login_users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;

/*Data for the table `productos` */

insert  into `productos`(`id`,`nombre`,`descripción`,`precio`,`estado`,`imagen`,`id_user`) values 
(2,'cebolla','kilo de cebolla','333','disponible','/static/cambiar_avatar/bans.jpg',16),
(3,'papa','kilo de papa','1111','disponible','/static/cambiar_avatar/china.jpg',16),
(4,'cebolla','kilo de cebolla cabezona','333','disponible','/static/cambiar_avatar/americana.jpg',8);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
