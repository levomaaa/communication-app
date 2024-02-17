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

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    forum_id INTEGER REFERENCES forums (id),
    visible BOOLEAN
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users (id),
    thread_id INTEGER REFERENCES threads (id),
    forum_id INTEGER REFERENCES forums (id),
    sent_at TIMESTAMP,
    visible BOOLEAN
);