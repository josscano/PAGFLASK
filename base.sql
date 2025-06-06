CREATE DATABASE burgerlab;

USE burgerlab;

CREATE TABLE burger(
    burger_id INT AUTO_INCREMENT PRIMARY KEY,
    burger_name VARCHAR(50),
    burger_description VARCHAR(100),
    burger_price DECIMAL(10,2),
    burger_image VARCHAR(100),
    burger_category VARCHAR(50),
    burger_date DATE
);