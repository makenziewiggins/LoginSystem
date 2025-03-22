CREATE TABLE attendance (
    id INT IDENTITY(1,1) PRIMARY KEY,
    student_id INT,
    course_id INT,
    date DATE NOT NULL,
    status CHAR(7) NOT NULL CHECK (status IN ('Present', 'Absent')),
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);