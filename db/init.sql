CREATE DATABASE IF NOT EXISTS lovify;
USE lovify;
CREATE TABLE messaggi (
    ID int,
    sender varchar(255),
    receiver varchar(255),
    textSent varchar(255), 
    msgRead varchar(255)
);