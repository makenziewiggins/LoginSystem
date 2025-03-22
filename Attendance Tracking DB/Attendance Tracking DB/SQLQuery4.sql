ALTER TABLE Courses ADD 
    course_name VARCHAR(100) NOT NULL,
    course_description TEXT,
    course_number VARCHAR(20) UNIQUE NOT NULL;
