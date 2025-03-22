SELECT c.name, COUNT(*) as present_count
FROM attendance a
JOIN courses c ON a.course_id = c.id
WHERE a.status = 'present'
GROUP BY c.name
