CREATE TABLE common_passwords (
    password TEXT PRIMARY KEY
);

COPY common_passwords (password) FROM '/common_passwords.txt';

CREATE TABLE "2402056" (
    username VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);