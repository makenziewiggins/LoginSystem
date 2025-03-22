INSERT INTO users (username, password) 
VALUES ('admin', HASHBYTES('SHA2_256', 'password123'));