--Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
SELECT
	s.fullname AS "Student name",
	gr.name AS "Group",
	ROUND(AVG(g.grade),2) as "Average grade"
FROM grades AS g
	LEFT JOIN students s ON s.id = g.student_id
	LEFT JOIN [groups] gr ON gr.id = s.group_id 
GROUP BY s.fullname
ORDER BY "Average grade" DESC 
LIMIT 5;