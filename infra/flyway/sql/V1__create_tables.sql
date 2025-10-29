-- V1__create_tables.sql
CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    isbn VARCHAR(100) UNIQUE,
    author VARCHAR(255),
    category VARCHAR(255),
    state VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS books_genres (
    book_id INTEGER REFERENCES books(id),
    genre VARCHAR(100),
    PRIMARY KEY (book_id, genre)
);
