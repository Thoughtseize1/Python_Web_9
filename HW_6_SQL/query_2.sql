--Знайти студента із найвищим середнім балом з певного предмета.
SELECT
	s2.title AS "Subject",
	s.fullname AS "Student",
	ROUND(AVG(g.grade),2) as Average_grade
FROM grades AS g
	JOIN students AS s ON s.id = g.student_id
	JOIN subjects AS s2 ON s2.id = g.subject_id
WHERE s2.id = 4
GROUP BY s.fullname
ORDER BY Average_grade DESC 
LIMIT 1;