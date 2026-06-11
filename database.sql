CREATE DATABASE IF NOT EXISTS library_system_db;
USE library_system_db;

DROP TABLE IF EXISTS book_authors;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS authors;
DROP TABLE IF EXISTS members;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS publishers;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    role ENUM('admin', 'user') NOT NULL DEFAULT 'user',
    status ENUM('Active', 'Inactive') NOT NULL DEFAULT 'Active'
);

CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE publishers (
    publisher_id INT AUTO_INCREMENT PRIMARY KEY,
    publisher_name VARCHAR(120) NOT NULL UNIQUE
);

CREATE TABLE authors (
    author_id INT AUTO_INCREMENT PRIMARY KEY,
    author_name VARCHAR(120) NOT NULL
);

CREATE TABLE books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    isbn VARCHAR(30) NOT NULL UNIQUE,
    category_id INT NOT NULL,
    publisher_id INT NOT NULL,
    publication_year INT,
    status ENUM('Available', 'Borrowed') NOT NULL DEFAULT 'Available',
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    FOREIGN KEY (publisher_id) REFERENCES publishers(publisher_id)
);

CREATE TABLE book_authors (
    book_id INT NOT NULL,
    author_id INT NOT NULL,
    PRIMARY KEY (book_id, author_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES authors(author_id) ON DELETE CASCADE
);

CREATE TABLE members (
    member_id INT AUTO_INCREMENT PRIMARY KEY,
    member_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL,
    address VARCHAR(255),
    status ENUM('Active', 'Inactive') NOT NULL DEFAULT 'Active'
);

INSERT INTO users (username, email, password, role, status)
VALUES
('admin', 'admin@library.com', 'admin123', 'admin', 'Active'),
('student', 'student@library.com', 'student123', 'user', 'Active');

INSERT INTO categories (category_name)
VALUES ('Fiction'), ('Science'), ('Technology'), ('History');

INSERT INTO publishers (publisher_name)
VALUES ('Penguin Books'), ('Oxford Press'), ('Pearson');

INSERT INTO authors (author_name)
VALUES ('George Orwell'), ('Stephen Hawking'), ('Robert C. Martin');

INSERT INTO books (title, isbn, category_id, publisher_id, publication_year, status)
VALUES
('1984', '9780451524935', 1, 1, 1949, 'Available'),
('A Brief History of Time', '9780553380163', 2, 2, 1988, 'Available'),
('Clean Code', '9780132350884', 3, 3, 2008, 'Borrowed');

INSERT INTO book_authors (book_id, author_id)
VALUES (1, 1), (2, 2), (3, 3);

INSERT INTO members (member_name, email, phone, address, status)
VALUES
('Himath Chandrasena', 'himath@example.com', '+94 77 123 4567', 'Colombo, Sri Lanka', 'Active'),
('Demo Student', 'student@example.com', '+94 71 987 6543', 'Kandy, Sri Lanka', 'Active');
