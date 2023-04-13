CREATE DATABASE IF NOT EXISTS lovify;
USE lovify;
CREATE TABLE messaggi (
    ID int NOT NULL AUTO_INCREMENT,
    receiver varchar(255),
    sender varchar(255),
    textSent varchar(255), 
    msgRead varchar(255), 
    PRIMARY KEY(ID)
) AUTO_INCREMENT = 100 ;