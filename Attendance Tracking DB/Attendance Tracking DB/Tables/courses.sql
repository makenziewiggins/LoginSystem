CREATE TABLE courses (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    course_number VARCHAR(20) UNIQUE NOT NULL
);