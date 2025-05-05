-- --------------------------------------------------------
-- Hôte:                         127.0.0.1
-- Version du serveur:           8.0.35 - MySQL Community Server - GPL
-- SE du serveur:                Win64
-- HeidiSQL Version:             12.1.0.6537
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Listage de la structure de la base pour le_trang_expi1b_coursyoga
DROP DATABASE IF EXISTS `le_trang_expi1b_coursyoga`;
CREATE DATABASE IF NOT EXISTS `le_trang_expi1b_coursyoga` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `le_trang_expi1b_coursyoga`;

-- Listage de la structure de table le_trang_expi1b_coursyoga. t_annulation
DROP TABLE IF EXISTS `t_annulation`;
CREATE TABLE IF NOT EXISTS `t_annulation` (
  `ID_AnnulerCours` int NOT NULL AUTO_INCREMENT,
  `FK_Inscrirecours` int DEFAULT NULL,
  `Raison` enum('Absent','Santé','Voyage','Problème technique','Météo','Congé','Raisons familiales','Examen','Grève','Cours remplacé','Autre') NOT NULL,
  `date_annulation` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID_AnnulerCours`),
  KEY `FK_Inscrirecours` (`FK_Inscrirecours`),
  CONSTRAINT `FK_annuler_inscrirecours` FOREIGN KEY (`FK_Inscrirecours`) REFERENCES `t_inscrirecours` (`ID_InscrireCours`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table le_trang_expi1b_coursyoga.t_annulation : ~12 rows (environ)
INSERT INTO `t_annulation` (`ID_AnnulerCours`, `FK_Inscrirecours`, `Raison`, `date_annulation`) VALUES
	(1, 7, 'Santé', '2024-05-25 21:36:19'),
	(2, NULL, 'Santé', NULL),
	(3, NULL, 'Voyage', NULL),
	(4, NULL, 'Problème technique', NULL),
	(5, NULL, 'Météo', NULL),
	(6, NULL, 'Congé', NULL),
	(7, NULL, 'Raisons familiales', NULL),
	(8, NULL, 'Examen', NULL),
	(9, NULL, 'Grève', NULL),
	(10, NULL, 'Cours remplacé', NULL),
	(11, NULL, 'Autre', NULL),
	(12, 2, 'Problème technique', '2024-05-26 12:17:31');

-- Listage de la structure de table le_trang_expi1b_coursyoga. t_avoirfonction
DROP TABLE IF EXISTS `t_avoirfonction`;
CREATE TABLE IF NOT EXISTS `t_avoirfonction` (
  `ID_avoirFonction` int NOT NULL AUTO_INCREMENT,
  `FK_Personne` int DEFAULT NULL,
  `FK_Fonction` int DEFAULT NULL,
  `Date_debut` date DEFAULT NULL,
  `Date_fin` date DEFAULT NULL,
  PRIMARY KEY (`ID_avoirFonction`),
  KEY `FK_Personne` (`FK_Personne`),
  KEY `FK_Fonction` (`FK_Fonction`),
  CONSTRAINT `t_avoirfonction_ibfk_1` FOREIGN KEY (`FK_Personne`) REFERENCES `t_personne` (`Id_personne`),
  CONSTRAINT `t_avoirfonction_ibfk_2` FOREIGN KEY (`FK_Fonction`) REFERENCES `t_fonction` (`ID_Fonction`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table le_trang_expi1b_coursyoga.t_avoirfonction : ~18 rows (environ)
INSERT INTO `t_avoirfonction` (`ID_avoirFonction`, `FK_Personne`, `FK_Fonction`, `Date_debut`, `Date_fin`) VALUES
	(1, 1, 2, '2020-01-01', NULL),
	(2, 2, 2, '2023-01-01', NULL),
	(3, 3, 5, '2023-03-15', NULL),
	(4, 4, 5, '2010-04-20', NULL),
	(5, 5, 1, '2019-06-01', '2023-02-25'),
	(6, 6, 3, '2023-07-10', NULL),
	(7, 7, 3, '2023-08-20', NULL),
	(8, 8, 4, '2000-01-01', NULL),
	(9, 9, 1, '2023-10-15', NULL),
	(10, 10, 1, '2023-11-25', NULL),
	(11, 11, 1, '2020-01-01', '2022-12-31'),
	(12, 12, 1, '2024-02-10', NULL),
	(13, 13, 1, '2024-03-20', NULL),
	(14, 14, 1, '2023-04-25', '2024-02-25'),
	(15, 5, 3, '2024-01-25', NULL),
	(16, 15, 1, '2022-06-15', NULL),
	(17, 16, 1, '2023-09-20', NULL),
	(18, 17, 1, '2023-12-12', NULL);

-- Listage de la structure de table le_trang_expi1b_coursyoga. t_cours
DROP TABLE IF EXISTS `t_cours`;
CREATE TABLE IF NOT EXISTS `t_cours` (
  `Id_cours` int NOT NULL AUTO_INCREMENT,
  `Titre` varchar(255) NOT NULL,
  `Niveau` enum('Débutant','Intermédiaire','Avancé') NOT NULL,
  `Session` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `Prix_par_session` float NOT NULL,
  `Description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `Affiche` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  PRIMARY KEY (`Id_cours`),
  UNIQUE KEY `Titre` (`Titre`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table le_trang_expi1b_coursyoga.t_cours : ~5 rows (environ)
INSERT INTO `t_cours` (`Id_cours`, `Titre`, `Niveau`, `Session`, `Prix_par_session`, `Description`, `Affiche`) VALUES
	(1, 'Yoga Début, Trouver la Sérénité', 'Débutant', 'Jan-Mars24', 200, 'Parfait pour les débutants désireux de découvrir le yoga et d\'atteindre la paix intérieure et l\'équilibre dans leur vie quotidienne.', 'https://ucarecdn.com/2681c47c-16d1-4217-b14f-633892efda4c/yoga1.jpeg'),
	(2, 'Yoga Dynamique, Renforcer le Corps', 'Intermédiaire', 'Jan-Mars24', 230, 'Un cours intermédiaire idéal pour ceux qui veulent améliorer leur force physique et leur endurance à travers des pratiques intensives.', 'https://ucarecdn.com/091e4b5e-365f-4793-acea-7270dbcc6a36/yoga3.jpeg'),
	(3, 'Yoga Avancé, Dépasser ses Limites', 'Avancé', 'Jan-Mars24', 165, 'Ce cours est pour ceux qui aspirent à maîtriser des poses complexes et à approfondir leur pratique spirituelle en dépassant leurs limites physiques et mentales', 'https://ucarecdn.com/a76fc4f1-ef06-4a26-8537-c5c1b2b3ada6/yoga4.jpeg'),
	(4, 'Début la Méditation Être Zen', 'Débutant', 'Jan-Mars24', 200, 'Ce cours initie les débutants aux techniques fondamentales de méditation, les aidant à cultiver la sérénité et à instaurer une pratique quotidienne de pleine conscience.', 'https://ucarecdn.com/1562bb1c-1456-4460-86cc-e44e152e7635/mdita.jpg'),
	(5, ' La Méditation, Cultiver Esprit', 'Intermédiaire', 'Jan-Mars24', 230, 'Ce cours intermédiaire approfondit la méditation pour ceux qui cherchent à améliorer leur conscience, rester zen et mieux se connaître à travers des pratiques guidées.', 'https://ucarecdn.com/da5d7c1b-0b24-4a3a-b4b6-389691d544d6/medita.jpeg');

-- Listage de la structure de table le_trang_expi1b_coursyoga. t_enseignercours
DROP TABLE IF EXISTS `t_enseignercours`;
CREATE TABLE IF NOT EXISTS `t_enseignercours` (
  `ID_EnseignerCours` int NOT NULL AUTO_INCREMENT,
  `FK_Cours` int DEFAULT NULL,
  `FK_Personne` int DEFAULT NULL,
  `Date_Enregistre` timestamp NULL DEFAULT (now()),
  `Description` enum('Yoga début','Méditation début','Yoga intermédiaire','Yoga avancé','Méditation intermédiaire') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`ID_EnseignerCours`) USING BTREE,
  KEY `FK_Cours` (`FK_Cours`) USING BTREE,
  KEY `FK_Personne` (`FK_Personne`) USING BTREE,
  CONSTRAINT `t_enseignercours_ibfk_1` FOREIGN KEY (`FK_Cours`) REFERENCES `t_cours` (`Id_cours`),
  CONSTRAINT `t_enseignercours_ibfk_2` FOREIGN KEY (`FK_Personne`) REFERENCES `t_personne` (`Id_personne`)
) ENGINE=InnoDB AUTO_INCREMENT=118 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;

-- Listage des données de la table le_trang_expi1b_coursyoga.t_enseignercours : ~117 rows (environ)
INSERT INTO `t_enseignercours` (`ID_EnseignerCours`, `FK_Cours`, `FK_Personne`, `Date_Enregistre`, `Description`) VALUES
	(1, 1, 5, '2023-12-20 06:00:00', 'Yoga début'),
	(2, 1, 5, '2023-12-20 06:00:00', 'Yoga début'),
	(3, 1, 5, '2023-12-20 06:00:00', 'Yoga début'),
	(4, 1, 5, '2023-12-20 06:00:00', 'Yoga début'),
	(5, 1, 5, '2023-12-20 06:00:00', 'Yoga début'),
	(6, 1, 5, '2023-12-20 06:00:00', 'Yoga début'),
	(7, 1, 5, '2023-12-20 06:00:00', 'Yoga début'),
	(8, 1, 5, '2023-12-20 06:00:00', 'Yoga début'),
	(9, 1, 5, '2023-12-20 06:00:00', 'Yoga début'),
	(10, 1, 5, '2023-12-20 06:00:00', 'Yoga début'),
	(11, 1, 5, '2023-12-20 06:00:00', 'Yoga début'),
	(12, 1, 5, '2023-12-20 06:00:00', 'Yoga début'),
	(13, 1, 5, '2023-12-20 06:00:00', 'Yoga début'),
	(14, 4, 6, '2023-12-20 06:00:00', 'Méditation début'),
	(15, 4, 6, '2023-12-20 06:00:00', 'Méditation début'),
	(16, 4, 6, '2023-12-20 06:00:00', 'Méditation début'),
	(17, 4, 6, '2023-12-20 06:00:00', 'Méditation début'),
	(18, 4, 6, '2023-12-20 06:00:00', 'Méditation début'),
	(19, 4, 6, '2023-12-20 06:00:00', 'Méditation début'),
	(20, 4, 6, '2023-12-20 06:00:00', 'Méditation début'),
	(21, 4, 6, '2023-12-20 06:00:00', 'Méditation début'),
	(22, 4, 6, '2023-12-20 06:00:00', 'Méditation début'),
	(23, 4, 6, '2023-12-20 06:00:00', 'Méditation début'),
	(24, 4, 6, '2023-12-20 06:00:00', 'Méditation début'),
	(25, 4, 6, '2023-12-20 06:00:00', 'Méditation début'),
	(26, 4, 6, '2023-12-20 06:00:00', 'Méditation début'),
	(27, 1, 5, '2023-12-20 06:00:00', 'Yoga début'),
	(28, 1, 5, '2023-12-20 06:00:00', 'Yoga début'),
	(29, 1, 5, '2023-12-20 06:00:00', 'Yoga début'),
	(30, 1, 5, '2023-12-20 06:00:00', 'Yoga début'),
	(31, 1, 5, '2023-12-20 06:00:00', 'Yoga début'),
	(32, 1, 5, '2023-12-20 06:00:00', 'Yoga début'),
	(33, 1, 5, '2023-12-20 06:00:00', 'Yoga début'),
	(34, 1, 5, '2023-12-20 06:00:00', 'Yoga début'),
	(35, 1, 5, '2023-12-20 06:00:00', 'Yoga début'),
	(36, 1, 5, '2023-12-20 06:00:00', 'Yoga début'),
	(37, 1, 5, '2023-12-20 06:00:00', 'Yoga début'),
	(38, 1, 5, '2023-12-20 06:00:00', 'Yoga début'),
	(39, 1, 5, '2023-12-20 06:00:00', 'Yoga début'),
	(40, 4, 6, '2023-12-20 06:00:00', 'Méditation début'),
	(41, 4, 6, '2023-12-20 06:00:00', 'Méditation début'),
	(42, 4, 6, '2023-12-20 06:00:00', 'Méditation début'),
	(43, 4, 6, '2023-12-20 06:00:00', 'Méditation début'),
	(44, 4, 6, '2023-12-20 06:00:00', 'Méditation début'),
	(45, 4, 6, '2023-12-20 06:00:00', 'Méditation début'),
	(46, 4, 6, '2023-12-20 06:00:00', 'Méditation début'),
	(47, 4, 6, '2023-12-20 06:00:00', 'Méditation début'),
	(48, 4, 6, '2023-12-20 06:00:00', 'Méditation début'),
	(49, 4, 6, '2023-12-20 06:00:00', 'Méditation début'),
	(50, 4, 6, '2023-12-20 06:00:00', 'Méditation début'),
	(51, 4, 6, '2023-12-20 06:00:00', 'Méditation début'),
	(52, 4, 6, '2023-12-20 06:00:00', 'Méditation début'),
	(53, 2, 7, '2023-12-20 06:00:00', 'Yoga intermédiaire'),
	(54, 2, 7, '2023-12-20 06:00:00', 'Yoga intermédiaire'),
	(55, 2, 7, '2023-12-20 06:00:00', 'Yoga intermédiaire'),
	(56, 2, 7, '2023-12-20 06:00:00', 'Yoga intermédiaire'),
	(57, 2, 7, '2023-12-20 06:00:00', 'Yoga intermédiaire'),
	(58, 2, 7, '2023-12-20 06:00:00', 'Yoga intermédiaire'),
	(59, 2, 7, '2023-12-20 06:00:00', 'Yoga intermédiaire'),
	(60, 2, 7, '2023-12-20 06:00:00', 'Yoga intermédiaire'),
	(61, 2, 7, '2023-12-20 06:00:00', 'Yoga intermédiaire'),
	(62, 2, 7, '2023-12-20 06:00:00', 'Yoga intermédiaire'),
	(63, 2, 7, '2023-12-20 06:00:00', 'Yoga intermédiaire'),
	(64, 2, 7, '2023-12-20 06:00:00', 'Yoga intermédiaire'),
	(65, 2, 7, '2023-12-20 06:00:00', 'Yoga intermédiaire'),
	(66, 5, 6, '2023-12-20 06:00:00', 'Méditation intermédiaire'),
	(67, 5, 6, '2023-12-20 06:00:00', 'Méditation intermédiaire'),
	(68, 5, 6, '2023-12-20 06:00:00', 'Méditation intermédiaire'),
	(69, 5, 6, '2023-12-20 06:00:00', 'Méditation intermédiaire'),
	(70, 5, 6, '2023-12-20 06:00:00', 'Méditation intermédiaire'),
	(71, 5, 6, '2023-12-20 06:00:00', 'Méditation intermédiaire'),
	(72, 5, 6, '2023-12-20 06:00:00', 'Méditation intermédiaire'),
	(73, 5, 6, '2023-12-20 06:00:00', 'Méditation intermédiaire'),
	(74, 5, 6, '2023-12-20 06:00:00', 'Méditation intermédiaire'),
	(75, 5, 6, '2023-12-20 06:00:00', 'Méditation intermédiaire'),
	(76, 5, 6, '2023-12-20 06:00:00', 'Méditation intermédiaire'),
	(77, 5, 6, '2023-12-20 06:00:00', 'Méditation intermédiaire'),
	(78, 5, 6, '2023-12-20 06:00:00', 'Méditation intermédiaire'),
	(79, 2, 7, '2023-12-20 06:00:00', 'Yoga intermédiaire'),
	(80, 2, 7, '2023-12-20 06:00:00', 'Yoga intermédiaire'),
	(81, 2, 7, '2023-12-20 06:00:00', 'Yoga intermédiaire'),
	(82, 2, 7, '2023-12-20 06:00:00', 'Yoga intermédiaire'),
	(83, 2, 7, '2023-12-20 06:00:00', 'Yoga intermédiaire'),
	(84, 2, 7, '2023-12-20 06:00:00', 'Yoga intermédiaire'),
	(85, 2, 7, '2023-12-20 06:00:00', 'Yoga intermédiaire'),
	(86, 2, 7, '2023-12-20 06:00:00', 'Yoga intermédiaire'),
	(87, 2, 7, '2023-12-20 06:00:00', 'Yoga intermédiaire'),
	(88, 2, 7, '2023-12-20 06:00:00', 'Yoga intermédiaire'),
	(89, 2, 7, '2023-12-20 06:00:00', 'Yoga intermédiaire'),
	(90, 2, 7, '2023-12-20 06:00:00', 'Yoga intermédiaire'),
	(91, 2, 7, '2023-12-20 06:00:00', 'Yoga intermédiaire'),
	(92, 5, 6, '2023-12-20 06:00:00', 'Méditation intermédiaire'),
	(93, 5, 6, '2023-12-20 06:00:00', 'Méditation intermédiaire'),
	(94, 5, 6, '2023-12-20 06:00:00', 'Méditation intermédiaire'),
	(95, 5, 6, '2023-12-20 06:00:00', 'Méditation intermédiaire'),
	(96, 5, 6, '2023-12-20 06:00:00', 'Méditation intermédiaire'),
	(97, 5, 6, '2023-12-20 06:00:00', 'Méditation intermédiaire'),
	(98, 5, 6, '2023-12-20 06:00:00', 'Méditation intermédiaire'),
	(99, 5, 6, '2023-12-20 06:00:00', 'Méditation intermédiaire'),
	(100, 5, 6, '2023-12-20 06:00:00', 'Méditation intermédiaire'),
	(101, 5, 6, '2023-12-20 06:00:00', 'Méditation intermédiaire'),
	(102, 5, 6, '2023-12-20 06:00:00', 'Méditation intermédiaire'),
	(103, 5, 6, '2023-12-20 06:00:00', 'Méditation intermédiaire'),
	(104, 5, 6, '2023-12-20 06:00:00', 'Méditation intermédiaire'),
	(105, 3, 7, '2023-12-20 06:00:00', 'Yoga avancé'),
	(106, 3, 7, '2023-12-20 06:00:00', 'Yoga avancé'),
	(107, 3, 7, '2023-12-20 06:00:00', 'Yoga avancé'),
	(108, 3, 7, '2023-12-20 06:00:00', 'Yoga avancé'),
	(109, 3, 7, '2023-12-20 06:00:00', 'Yoga avancé'),
	(110, 3, 7, '2023-12-20 06:00:00', 'Yoga avancé'),
	(111, 3, 7, '2023-12-20 06:00:00', 'Yoga avancé'),
	(112, 3, 7, '2023-12-20 06:00:00', 'Yoga avancé'),
	(113, 3, 7, '2023-12-20 06:00:00', 'Yoga avancé'),
	(114, 3, 7, '2023-12-20 06:00:00', 'Yoga avancé'),
	(115, 3, 7, '2023-12-20 06:00:00', 'Yoga avancé'),
	(116, 3, 7, '2023-12-20 06:00:00', 'Yoga avancé'),
	(117, 3, 7, '2023-12-20 06:00:00', 'Yoga avancé');

-- Listage de la structure de table le_trang_expi1b_coursyoga. t_fonction
DROP TABLE IF EXISTS `t_fonction`;
CREATE TABLE IF NOT EXISTS `t_fonction` (
  `ID_Fonction` int NOT NULL AUTO_INCREMENT,
  `Type_fonction` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`ID_Fonction`),
  UNIQUE KEY `Type_fonction` (`Type_fonction`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table le_trang_expi1b_coursyoga.t_fonction : ~5 rows (environ)
INSERT INTO `t_fonction` (`ID_Fonction`, `Type_fonction`) VALUES
	(5, 'Assistant'),
	(2, 'Famille'),
	(4, 'Gestionnaire'),
	(3, 'Instructeur'),
	(1, 'Membre');

-- Listage de la structure de table le_trang_expi1b_coursyoga. t_horaire
DROP TABLE IF EXISTS `t_horaire`;
CREATE TABLE IF NOT EXISTS `t_horaire` (
  `ID_horaire` int NOT NULL AUTO_INCREMENT,
  `date_cours` date DEFAULT NULL,
  `jour_semaine` varchar(50) DEFAULT NULL,
  `heure_debut` time DEFAULT NULL,
  `heure_fin` time DEFAULT NULL,
  PRIMARY KEY (`ID_horaire`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table le_trang_expi1b_coursyoga.t_horaire : ~52 rows (environ)
INSERT INTO `t_horaire` (`ID_horaire`, `date_cours`, `jour_semaine`, `heure_debut`, `heure_fin`) VALUES
	(1, '2024-01-03', 'Lundi', '19:00:00', '20:30:00'),
	(2, '2024-01-10', 'Lundi', '19:00:00', '20:30:00'),
	(3, '2024-01-17', 'Lundi', '19:00:00', '20:30:00'),
	(4, '2024-01-24', 'Lundi', '19:00:00', '20:30:00'),
	(5, '2024-01-31', 'Lundi', '19:00:00', '20:30:00'),
	(6, '2024-02-07', 'Lundi', '19:00:00', '20:30:00'),
	(7, '2024-02-14', 'Lundi', '19:00:00', '20:30:00'),
	(8, '2024-02-21', 'Lundi', '19:00:00', '20:30:00'),
	(9, '2024-02-28', 'Lundi', '19:00:00', '20:30:00'),
	(10, '2024-03-06', 'Lundi', '19:00:00', '20:30:00'),
	(11, '2024-03-13', 'Lundi', '19:00:00', '20:30:00'),
	(12, '2024-03-20', 'Lundi', '19:00:00', '20:30:00'),
	(13, '2024-03-27', 'Lundi', '19:00:00', '20:30:00'),
	(14, '2024-01-06', 'Jeudi', '19:00:00', '20:30:00'),
	(15, '2024-01-13', 'Jeudi', '19:00:00', '20:30:00'),
	(16, '2024-01-20', 'Jeudi', '19:00:00', '20:30:00'),
	(17, '2024-01-27', 'Jeudi', '19:00:00', '20:30:00'),
	(18, '2024-02-03', 'Jeudi', '19:00:00', '20:30:00'),
	(19, '2024-02-10', 'Jeudi', '19:00:00', '20:30:00'),
	(20, '2024-02-17', 'Jeudi', '19:00:00', '20:30:00'),
	(21, '2024-02-24', 'Jeudi', '19:00:00', '20:30:00'),
	(22, '2024-03-02', 'Jeudi', '19:00:00', '20:30:00'),
	(23, '2024-03-09', 'Jeudi', '19:00:00', '20:30:00'),
	(24, '2024-03-16', 'Jeudi', '19:00:00', '20:30:00'),
	(25, '2024-03-23', 'Jeudi', '19:00:00', '20:30:00'),
	(26, '2024-03-30', 'Jeudi', '19:00:00', '20:30:00'),
	(27, '2024-01-07', 'Samedi', '08:00:00', '09:30:00'),
	(28, '2024-01-07', 'Samedi', '14:00:00', '15:30:00'),
	(29, '2024-01-14', 'Samedi', '08:00:00', '09:30:00'),
	(30, '2024-01-14', 'Samedi', '14:00:00', '15:30:00'),
	(31, '2024-01-21', 'Samedi', '08:00:00', '09:30:00'),
	(32, '2024-01-21', 'Samedi', '14:00:00', '15:30:00'),
	(33, '2024-01-28', 'Samedi', '08:00:00', '09:30:00'),
	(34, '2024-01-28', 'Samedi', '14:00:00', '15:30:00'),
	(35, '2024-02-04', 'Samedi', '08:00:00', '09:30:00'),
	(36, '2024-02-04', 'Samedi', '14:00:00', '15:30:00'),
	(37, '2024-02-11', 'Samedi', '08:00:00', '09:30:00'),
	(38, '2024-02-11', 'Samedi', '14:00:00', '15:30:00'),
	(39, '2024-02-18', 'Samedi', '08:00:00', '09:30:00'),
	(40, '2024-02-18', 'Samedi', '14:00:00', '15:30:00'),
	(41, '2024-02-25', 'Samedi', '08:00:00', '09:30:00'),
	(42, '2024-02-25', 'Samedi', '14:00:00', '15:30:00'),
	(43, '2024-03-03', 'Samedi', '08:00:00', '09:30:00'),
	(44, '2024-03-03', 'Samedi', '14:00:00', '15:30:00'),
	(45, '2024-03-10', 'Samedi', '08:00:00', '09:30:00'),
	(46, '2024-03-10', 'Samedi', '14:00:00', '15:30:00'),
	(47, '2024-03-17', 'Samedi', '08:00:00', '09:30:00'),
	(48, '2024-03-17', 'Samedi', '14:00:00', '15:30:00'),
	(49, '2024-03-24', 'Samedi', '08:00:00', '09:30:00'),
	(50, '2024-03-24', 'Samedi', '14:00:00', '15:30:00'),
	(51, '2024-03-31', 'Samedi', '08:00:00', '09:30:00'),
	(52, '2024-03-31', 'Samedi', '14:00:00', '15:30:00');

-- Listage de la structure de table le_trang_expi1b_coursyoga. t_horaire_cours
DROP TABLE IF EXISTS `t_horaire_cours`;
CREATE TABLE IF NOT EXISTS `t_horaire_cours` (
  `ID_horaireCours` int NOT NULL AUTO_INCREMENT,
  `FK_Horaire` int DEFAULT NULL,
  `FK_Cours` int DEFAULT NULL,
  `date_enregistre` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID_horaireCours`),
  KEY `FK_horaire` (`FK_Horaire`) USING BTREE,
  KEY `FK_cours` (`FK_Cours`) USING BTREE,
  CONSTRAINT `horaire_cours_ibfk_1` FOREIGN KEY (`FK_Horaire`) REFERENCES `t_horaire` (`ID_horaire`),
  CONSTRAINT `horaire_cours_ibfk_2` FOREIGN KEY (`FK_Cours`) REFERENCES `t_cours` (`Id_cours`)
) ENGINE=InnoDB AUTO_INCREMENT=118 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table le_trang_expi1b_coursyoga.t_horaire_cours : ~117 rows (environ)
INSERT INTO `t_horaire_cours` (`ID_horaireCours`, `FK_Horaire`, `FK_Cours`, `date_enregistre`) VALUES
	(1, 1, 1, '2024-04-20 20:19:48'),
	(2, 2, 1, '2024-04-20 20:19:48'),
	(3, 3, 1, '2024-04-20 20:19:48'),
	(4, 4, 1, '2024-04-20 20:19:48'),
	(5, 5, 1, '2024-04-20 20:19:48'),
	(6, 6, 1, '2024-04-20 20:19:48'),
	(7, 7, 1, '2024-04-20 20:19:48'),
	(8, 8, 1, '2024-04-20 20:19:48'),
	(9, 9, 1, '2024-04-20 20:19:48'),
	(10, 10, 1, '2024-04-20 20:19:48'),
	(11, 11, 1, '2024-04-20 20:19:48'),
	(12, 12, 1, '2024-04-20 20:19:48'),
	(13, 13, 1, '2024-04-20 20:19:48'),
	(14, 1, 4, '2024-04-20 20:19:48'),
	(15, 2, 4, '2024-04-20 20:19:48'),
	(16, 3, 4, '2024-04-20 20:19:48'),
	(17, 4, 4, '2024-04-20 20:19:48'),
	(18, 5, 4, '2024-04-20 20:19:48'),
	(19, 6, 4, '2024-04-20 20:19:48'),
	(20, 7, 4, '2024-04-20 20:19:48'),
	(21, 8, 4, '2024-04-20 20:19:48'),
	(22, 9, 4, '2024-04-20 20:19:48'),
	(23, 10, 4, '2024-04-20 20:19:48'),
	(24, 11, 4, '2024-04-20 20:19:48'),
	(25, 12, 4, '2024-04-20 20:19:48'),
	(26, 13, 4, '2024-04-20 20:19:48'),
	(27, 27, 1, '2024-04-20 20:19:53'),
	(28, 29, 1, '2024-04-20 20:19:53'),
	(29, 31, 1, '2024-04-20 20:19:53'),
	(30, 33, 1, '2024-04-20 20:19:53'),
	(31, 35, 1, '2024-04-20 20:19:53'),
	(32, 37, 1, '2024-04-20 20:19:53'),
	(33, 39, 1, '2024-04-20 20:19:53'),
	(34, 41, 1, '2024-04-20 20:19:53'),
	(35, 43, 1, '2024-04-20 20:19:53'),
	(36, 45, 1, '2024-04-20 20:19:53'),
	(37, 47, 1, '2024-04-20 20:19:53'),
	(38, 49, 1, '2024-04-20 20:19:53'),
	(39, 51, 1, '2024-04-20 20:19:53'),
	(40, 27, 4, '2024-04-20 20:19:53'),
	(41, 29, 4, '2024-04-20 20:19:53'),
	(42, 31, 4, '2024-04-20 20:19:53'),
	(43, 33, 4, '2024-04-20 20:19:53'),
	(44, 35, 4, '2024-04-20 20:19:53'),
	(45, 37, 4, '2024-04-20 20:19:53'),
	(46, 39, 4, '2024-04-20 20:19:53'),
	(47, 41, 4, '2024-04-20 20:19:53'),
	(48, 43, 4, '2024-04-20 20:19:53'),
	(49, 45, 4, '2024-04-20 20:19:53'),
	(50, 47, 4, '2024-04-20 20:19:53'),
	(51, 49, 4, '2024-04-20 20:19:53'),
	(52, 51, 4, '2024-04-20 20:19:53'),
	(53, 14, 2, '2024-04-20 20:19:59'),
	(54, 15, 2, '2024-04-20 20:19:59'),
	(55, 16, 2, '2024-04-20 20:19:59'),
	(56, 17, 2, '2024-04-20 20:19:59'),
	(57, 18, 2, '2024-04-20 20:19:59'),
	(58, 19, 2, '2024-04-20 20:19:59'),
	(59, 20, 2, '2024-04-20 20:19:59'),
	(60, 21, 2, '2024-04-20 20:19:59'),
	(61, 22, 2, '2024-04-20 20:19:59'),
	(62, 23, 2, '2024-04-20 20:19:59'),
	(63, 24, 2, '2024-04-20 20:19:59'),
	(64, 25, 2, '2024-04-20 20:19:59'),
	(65, 26, 2, '2024-04-20 20:19:59'),
	(66, 14, 5, '2024-04-20 20:19:59'),
	(67, 15, 5, '2024-04-20 20:19:59'),
	(68, 16, 5, '2024-04-20 20:19:59'),
	(69, 17, 5, '2024-04-20 20:19:59'),
	(70, 18, 5, '2024-04-20 20:19:59'),
	(71, 19, 5, '2024-04-20 20:19:59'),
	(72, 20, 5, '2024-04-20 20:19:59'),
	(73, 21, 5, '2024-04-20 20:19:59'),
	(74, 22, 5, '2024-04-20 20:19:59'),
	(75, 23, 5, '2024-04-20 20:19:59'),
	(76, 24, 5, '2024-04-20 20:19:59'),
	(77, 25, 5, '2024-04-20 20:19:59'),
	(78, 26, 5, '2024-04-20 20:19:59'),
	(79, 28, 2, '2024-04-20 20:20:07'),
	(80, 30, 2, '2024-04-20 20:20:07'),
	(81, 32, 2, '2024-04-20 20:20:07'),
	(82, 34, 2, '2024-04-20 20:20:07'),
	(83, 36, 2, '2024-04-20 20:20:07'),
	(84, 38, 2, '2024-04-20 20:20:07'),
	(85, 40, 2, '2024-04-20 20:20:07'),
	(86, 42, 2, '2024-04-20 20:20:07'),
	(87, 44, 2, '2024-04-20 20:20:07'),
	(88, 46, 2, '2024-04-20 20:20:07'),
	(89, 48, 2, '2024-04-20 20:20:07'),
	(90, 50, 2, '2024-04-20 20:20:07'),
	(91, 52, 2, '2024-04-20 20:20:07'),
	(92, 28, 5, '2024-04-20 20:20:07'),
	(93, 30, 5, '2024-04-20 20:20:07'),
	(94, 32, 5, '2024-04-20 20:20:07'),
	(95, 34, 5, '2024-04-20 20:20:07'),
	(96, 36, 5, '2024-04-20 20:20:07'),
	(97, 38, 5, '2024-04-20 20:20:07'),
	(98, 40, 5, '2024-04-20 20:20:07'),
	(99, 42, 5, '2024-04-20 20:20:07'),
	(100, 44, 5, '2024-04-20 20:20:07'),
	(101, 46, 5, '2024-04-20 20:20:07'),
	(102, 48, 5, '2024-04-20 20:20:07'),
	(103, 50, 5, '2024-04-20 20:20:07'),
	(104, 52, 5, '2024-04-20 20:20:07'),
	(105, 27, 3, '2024-04-20 20:20:14'),
	(106, 29, 3, '2024-04-20 20:20:14'),
	(107, 31, 3, '2024-04-20 20:20:14'),
	(108, 33, 3, '2024-04-20 20:20:14'),
	(109, 35, 3, '2024-04-20 20:20:14'),
	(110, 37, 3, '2024-04-20 20:20:14'),
	(111, 39, 3, '2024-04-20 20:20:14'),
	(112, 41, 3, '2024-04-20 20:20:14'),
	(113, 43, 3, '2024-04-20 20:20:14'),
	(114, 45, 3, '2024-04-20 20:20:14'),
	(115, 47, 3, '2024-04-20 20:20:14'),
	(116, 49, 3, '2024-04-20 20:20:14'),
	(117, 51, 3, '2024-04-20 20:20:14');

-- Listage de la structure de table le_trang_expi1b_coursyoga. t_inscrirecours
DROP TABLE IF EXISTS `t_inscrirecours`;
CREATE TABLE IF NOT EXISTS `t_inscrirecours` (
  `ID_InscrireCours` int NOT NULL AUTO_INCREMENT,
  `FK_Personne` int DEFAULT NULL,
  `FK_Cours` int DEFAULT NULL,
  `date_inscrire` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID_InscrireCours`),
  KEY `FK_Personne` (`FK_Personne`),
  KEY `FK_Cours` (`FK_Cours`),
  CONSTRAINT `t_inscrirecours_ibfk_1` FOREIGN KEY (`FK_Personne`) REFERENCES `t_personne` (`Id_personne`),
  CONSTRAINT `t_inscrirecours_ibfk_2` FOREIGN KEY (`FK_Cours`) REFERENCES `t_cours` (`Id_cours`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table le_trang_expi1b_coursyoga.t_inscrirecours : ~12 rows (environ)
INSERT INTO `t_inscrirecours` (`ID_InscrireCours`, `FK_Personne`, `FK_Cours`, `date_inscrire`) VALUES
	(1, 1, 1, '2023-12-14 23:00:00'),
	(2, 2, 5, '2023-12-20 06:00:00'),
	(3, 9, 1, '2023-12-01 06:00:00'),
	(4, 10, 2, '2023-12-20 06:00:00'),
	(5, 11, 3, '2023-12-20 06:00:00'),
	(6, 12, 4, '2023-12-20 06:00:00'),
	(7, 13, 5, '2023-12-20 06:00:00'),
	(8, 14, 1, '2023-12-14 23:00:00'),
	(9, 16, 2, '2023-12-20 06:00:00'),
	(10, 17, 3, '2023-12-20 06:00:00'),
	(11, 15, 5, '2023-06-20 05:00:00'),
	(12, 18, 4, '2024-05-13 19:03:00');

-- Listage de la structure de table le_trang_expi1b_coursyoga. t_payement
DROP TABLE IF EXISTS `t_payement`;
CREATE TABLE IF NOT EXISTS `t_payement` (
  `ID_payement` int NOT NULL AUTO_INCREMENT,
  `FK_Inscrirecours` int DEFAULT NULL,
  `Montant_principal` decimal(10,2) DEFAULT NULL,
  `Rabais` decimal(10,2) DEFAULT NULL,
  `Description_Rabais` enum('rabais famille','welcome20%','special 50%','Aucune Rabais') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `Montant_paye` decimal(10,2) DEFAULT NULL,
  `Montant_restant` decimal(10,2) DEFAULT NULL,
  `Mode_paiement` enum('Carte de crédit','PayPal','Virement bancaire','TWINT','Espèces') NOT NULL,
  `Statut` enum('en attente','réussi','payé partiel','échoué') NOT NULL,
  `Date_paiement` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID_payement`),
  KEY `FK_Inscrirecours` (`FK_Inscrirecours`),
  CONSTRAINT `t_payercours_ibfk_1` FOREIGN KEY (`FK_Inscrirecours`) REFERENCES `t_inscrirecours` (`ID_InscrireCours`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table le_trang_expi1b_coursyoga.t_payement : ~12 rows (environ)
INSERT INTO `t_payement` (`ID_payement`, `FK_Inscrirecours`, `Montant_principal`, `Rabais`, `Description_Rabais`, `Montant_paye`, `Montant_restant`, `Mode_paiement`, `Statut`, `Date_paiement`) VALUES
	(1, 1, 200.00, 1.00, 'rabais famille', 0.00, 0.00, 'Carte de crédit', 'réussi', '2023-12-21 23:00:00'),
	(2, 2, 230.00, 1.00, 'rabais famille', 0.00, 0.00, 'Carte de crédit', 'réussi', '2023-12-22 23:00:00'),
	(3, 3, 200.00, 0.20, 'welcome20%', 160.00, 0.00, 'Virement bancaire', 'en attente', '2023-12-23 23:00:00'),
	(4, 4, 230.00, 0.00, 'Aucune Rabais', 230.00, 0.00, 'PayPal', 'réussi', '2023-01-21 23:00:00'),
	(5, 5, 165.00, 0.00, 'Aucune Rabais', 165.00, 0.00, 'Virement bancaire', 'réussi', '2023-01-21 23:00:00'),
	(6, 6, 200.00, 0.00, 'Aucune Rabais', 200.00, 0.00, 'Carte de crédit', 'en attente', '2023-12-26 23:00:00'),
	(7, 7, 230.00, 0.00, 'Aucune Rabais', 230.00, 0.00, 'PayPal', 'en attente', '2023-12-27 23:00:00'),
	(8, 8, 200.00, 0.00, 'Aucune Rabais', 200.00, 0.00, 'Espèces', 'réussi', '2023-12-28 23:00:00'),
	(9, 9, 230.00, 0.50, 'special 50%', 115.00, 0.00, 'Espèces', 'réussi', '2023-12-21 23:00:00'),
	(10, 10, 165.00, 0.00, 'Aucune Rabais', 165.00, 0.00, 'Carte de crédit', 'réussi', '2023-12-22 23:00:00'),
	(11, 11, 230.00, 0.20, 'welcome20%', 150.00, 79.54, 'Virement bancaire', 'réussi', '2023-11-04 23:00:00'),
	(14, 12, 200.00, 0.20, 'welcome20%', 95.00, 104.60, 'PayPal', 'réussi', '2024-05-26 13:58:01');

-- Listage de la structure de table le_trang_expi1b_coursyoga. t_personne
DROP TABLE IF EXISTS `t_personne`;
CREATE TABLE IF NOT EXISTS `t_personne` (
  `Id_personne` int NOT NULL AUTO_INCREMENT,
  `Nom` varchar(30) NOT NULL,
  `Prenom` varchar(50) NOT NULL,
  `Date_naissance` date DEFAULT NULL,
  `NumeroAVS` char(13) DEFAULT NULL,
  `Sexe` enum('Masculin','Féminin') NOT NULL,
  `date_enregistre` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`Id_personne`),
  UNIQUE KEY `Unique_Personne` (`NumeroAVS`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table le_trang_expi1b_coursyoga.t_personne : ~20 rows (environ)
INSERT INTO `t_personne` (`Id_personne`, `Nom`, `Prenom`, `Date_naissance`, `NumeroAVS`, `Sexe`, `date_enregistre`) VALUES
	(1, 'Dubois', 'Jean', '1975-01-01', '7563690321254', 'Masculin', '2024-03-14 21:00:03'),
	(2, 'Martin', 'Sonoko', '1978-06-15', '7563337951326', 'Féminin', '2024-03-14 21:00:03'),
	(3, 'Garcia', 'Ana', '1980-03-20', '7566664567890', 'Féminin', '2024-03-14 21:00:03'),
	(4, 'Sato', 'Takeshi', '1983-09-10', '7569996543210', 'Masculin', '2024-03-14 21:00:03'),
	(5, 'Ruchet', 'Marie', '1986-12-05', '7561477890123', 'Féminin', '2024-03-14 21:00:03'),
	(6, 'Yamamoto', 'Hiroshi', '1989-05-22', '7562586549870', 'Masculin', '2024-03-14 21:00:03'),
	(7, 'Nguyen', 'Sophie', '1992-08-18', '7567893333456', 'Féminin', '2024-03-14 21:00:03'),
	(8, 'Roy', 'Michel', '1995-11-03', '7566546667210', 'Masculin', '2024-03-14 21:00:03'),
	(9, 'Tran', 'Léa', '1998-04-29', '7568529633690', 'Féminin', '2024-03-14 21:00:03'),
	(10, 'Tanaka', 'Sakura', '2002-07-14', '7569633337410', 'Féminin', '2024-03-14 21:00:03'),
	(11, 'Muller', 'Chandy', '1999-05-20', '7564443333333', 'Masculin', '2024-03-14 21:00:03'),
	(12, 'Berger', 'Pierre', '2000-10-10', '7567777776666', 'Masculin', '2024-03-14 21:00:03'),
	(13, 'Lam', 'Yuki', '1995-08-15', '7566663333333', 'Masculin', '2024-03-14 21:00:03'),
	(14, 'Choi', 'Kenji', '1997-12-02', '7569999444444', 'Masculin', '2024-03-14 21:00:03'),
	(15, 'Schneider', 'Emilie', '1993-03-08', '7563331111111', 'Féminin', '2024-03-14 21:00:03'),
	(16, 'Bianchi', 'Luca', '1996-09-25', '7566662222222', 'Masculin', '2024-03-14 21:00:03'),
	(17, 'Wang', 'Li', '2000-12-12', '7569998888888', 'Féminin', '2024-03-14 21:00:03'),
	(18, 'Nguyen', 'Titoo', '2024-04-29', '1111324678890', 'Féminin', '2024-04-20 08:40:53'),
	(19, 'mykano', 'joki', '1991-09-26', '3425618999999', 'Féminin', '2024-05-26 14:40:53'),
	(20, 'trsoll', 'Stella', '2000-01-26', '2343211222228', 'Masculin', '2024-05-26 14:55:58');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
