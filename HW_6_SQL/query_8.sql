-- Знайти середній бал, який ставить певний викладач зі своїх предметів.
SELECT 
	teacher.fullname AS Teacher,
	sub.title AS Subject,
	ROUND(AVG(rg.grade),2) as average_grade
FROM grades AS rg
	JOIN subjects AS sub ON sub.id = rg.subject_id 
	JOIN teachers AS teacher ON teacher.id  = sub.teacher_id
WHERE teacher.id = 4
GROUP BY sub.title;