-- Create the table that will hold common passwords
CREATE TABLE common_passwords (
    password TEXT PRIMARY KEY
);

-- Load data from the file (the file is placed in the container root)
COPY common_passwords (password) FROM '/common_passwords.txt' (FORMAT csv, DELIMITER E'\n', QUOTE E'\x01');

-- Table for logging user logins
CREATE TABLE "2402056" (
    username VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);