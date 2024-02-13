CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    password TEXT,
    role INTEGER
);

CREATE TABLE forums (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    visible BOOLEAN
);
