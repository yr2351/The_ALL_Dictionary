DROP DATABASE IF EXISTS cse416; -- Temporary code
CREATE DATABASE IF NOT EXISTS cse416 DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci; -- Temporary code
USE cse416; -- Temporary code

DROP TABLE IF EXISTS Account;
CREATE TABLE IF NOT EXISTS Account (
  email VARCHAR(100) NOT NULL,
  isAdmin BOOLEAN,
  del VARCHAR(1) DEFAULT 'n',
  PRIMARY KEY (email)
) ENGINE=INNODB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS UserAccount;
CREATE TABLE IF NOT EXISTS UserAccount (
  email VARCHAR(100) NOT NULL,
  password VARCHAR(100) NOT NULL,
  name VARCHAR(100) NOT NULL,
  profilePictureURL VARCHAR(1000),
  PRIMARY KEY (email),
  FOREIGN KEY (email) REFERENCES Account(email) ON DELETE CASCADE
) ENGINE=INNODB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS HasSearchHistory;
CREATE TABLE IF NOT EXISTS HasSearchHistory (
  email VARCHAR(100) NOT NULL,
  idx INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
  word VARCHAR(100) NOT NULL,
  regDate DATETIME NOT NULL,
  FOREIGN KEY (email) REFERENCES UserAccount(email) ON DELETE NO ACTION
) ENGINE=INNODB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS HasSourceOrder;
CREATE TABLE IF NOT EXISTS HasSourceOrder (
  email VARCHAR(100) NOT NULL,
  idx INTEGER NOT NULL,
  source VARCHAR(500) NOT NULL,
  PRIMARY KEY (email, idx),
  FOREIGN KEY (email) REFERENCES UserAccount(email) ON DELETE NO ACTION
) ENGINE=INNODB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `packages`;
CREATE TABLE `packages` (
  `email` VARCHAR(100) NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE (`email`, `name`),
  FOREIGN KEY (email) REFERENCES UserAccount(email) ON DELETE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `words`;
CREATE TABLE `words` (
  `email` VARCHAR(100) NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `pos` varchar(45) DEFAULT NULL,
  `meaning` longtext,
  `image` longtext,
  PRIMARY KEY (`id`),
  FOREIGN KEY (email) REFERENCES UserAccount(email) ON DELETE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `sets`;
CREATE TABLE `sets` (
  `email` VARCHAR(100) NOT NULL,
  `p_id` int(11) NOT NULL,
  `w_id` int(11) NOT NULL,
  PRIMARY KEY (`p_id`,`w_id`),
  FOREIGN KEY (email) REFERENCES UserAccount(email) ON DELETE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* END: Note Card */

DROP TABLE IF EXISTS Quiz;
CREATE TABLE IF NOT EXISTS Quiz (
  qid INT(50) NOT NULL AUTO_INCREMENT,
  email VARCHAR(100) NOT NULL, 
  problem VARCHAR(200) NOT NULL,
  option1 VARCHAR(50) NOT NULL,
  option2 VARCHAR(50) NOT NULL,
  option3 VARCHAR(50) NOT NULL,
  option4 VARCHAR(50) NOT NULL,
  answer VARCHAR(50) NOT NULL,
  PRIMARY KEY (qid),
  FOREIGN KEY (email) REFERENCES UserAccount(email) ON DELETE NO ACTION
) ENGINE=INNODB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS WordsChallenge;
CREATE TABLE IF NOT EXISTS WordsChallenge (
  qid INT(50) NOT NULL,
  question VARCHAR(50) NOT NULL,
  option1 VARCHAR(50) NOT NULL,
  option2 VARCHAR(50) NOT NULL,
  option3 VARCHAR(50) NOT NULL,
  option4 VARCHAR(50) NOT NULL,
  answer VARCHAR(50) NOT NULL
) ENGINE=INNODB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS Ranking;
CREATE TABLE IF NOT EXISTS Ranking (
  email VARCHAR(100) DEFAULT 'No one ranked yet.',
  score INT(11) DEFAULT 0,
  date TIMESTAMP DEFAULT 0,
  FOREIGN KEY (email) REFERENCES UserAccount(email) ON DELETE NO ACTION
) ENGINE=INNODB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS History;
CREATE TABLE IF NOT EXISTS History (
  email VARCHAR(100) NOT NULL,
  score INT(11) NOT NULL,
  question VARCHAR(100) NOT NULL,
  rightans VARCHAR(100) NOT NULL,
  wrongans VARCHAR(100) NOT NULL,
  date TIMESTAMP NOT NULL,
  FOREIGN KEY (email) REFERENCES UserAccount(email) ON DELETE NO ACTION
) ENGINE=INNODB DEFAULT CHARSET=utf8;

INSERT INTO WordsChallenge (qid, question, option1, option2, option3, option4, answer) VALUES ('1', 'Fruit which color is red', 'Apple', 'Mango', 'Melon', 'Orange', 'Apple');
INSERT INTO WordsChallenge (qid, question, option1, option2, option3, option4, answer) VALUES ('2', 'Fruit which color is yellow', 'Strawberry', 'Banana', 'Blueberry', 'Water Melon', 'Banana');
INSERT INTO WordsChallenge (qid, question, option1, option2, option3, option4, answer) VALUES ('3', 'Fruit which color is green', 'Apple', 'Mango', 'Melon', 'Water Melon', 'Melon');
INSERT INTO WordsChallenge (qid, question, option1, option2, option3, option4, answer) VALUES ('4', 'Fruit which has stripe', 'Pineapple', 'Banana', 'Cherry', 'Water Melon', 'Water Melon');
INSERT INTO WordsChallenge (qid, question, option1, option2, option3, option4, answer) VALUES ('5', 'King of the jungle', 'Tarzan', 'Monkey', 'Anaconda', 'Killer Bee', 'Tarzan');
