-- Creates the database hbnb_dev_db with specified parameters
-- Create database
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- Creates user if doesn't exist and sets password
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- Grants privileges to user on database and performance_schema
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';

-- Flush privileges to apply the changes
FLUSH PRIVILEGES;
