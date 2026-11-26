CREATE DATABASE health_wellness;
USE health_wellness;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE habits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    habit_type VARCHAR(50),
    target_amount INT,
    current_amount INT,
    date DATE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE health_tips (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200),
    content TEXT,
    category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE progress_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    metric_type VARCHAR(50),
    value DECIMAL(10,2),
    date DATE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
