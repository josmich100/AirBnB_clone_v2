-- Creates the database hbnb_test_db with specified parameters
-- Create database
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Creates user if doesn't exist and sets password
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- Grants privileges to user on database and performance_schema
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';

-- Flush privileges to apply the changes
FLUSH PRIVILEGES;
