-- Drop the database if it exists
DROP DATABASE IF EXISTS flask_feedback;

-- Create a new database
CREATE DATABASE flask_feedback;

-- Connect to the new database
\c flask_feedback

-- Create tables
CREATE TABLE users (
    username VARCHAR(20) PRIMARY KEY,
    password TEXT NOT NULL,
    email VARCHAR(50) NOT NULL,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL
);

CREATE TABLE feedback (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    username VARCHAR(20) REFERENCES users(username) NOT NULL
);

-- Insert sample data into users table
INSERT INTO users (username, password, email, first_name, last_name)
VALUES
    ('suchi.sundar', 'peach100', 'example@gmail.com', 'Suchi', 'Sundar'),
    ('nico.sundar', 'skatebird', 'example2@gmail.com', 'Nico', 'Sundar'),
    ('mia.blanco', 'lemonade', 'example3@gmail.com', 'Mia', 'Blanco');

-- Insert sample data into feedback table
INSERT INTO feedback (title, content, username)
VALUES
    ('My First Review', 'I hope this works!', 'suchi.sundar'),
    ('My Second Review', 'It is working!', 'suchi.sundar'),
    ('What is This', 'I am hungry', 'nico.sundar'),
    ('Wow!', 'Genius', 'mia.blanco');
