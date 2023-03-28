--Знайти оцінки студентів у окремій групі з певного предмета.
SELECT
	st.fullname as Student,
	gr.name as "Group",
	sub.title as Subject,
	g.grade as Grade
FROM grades AS g
	JOIN subjects AS sub ON g.subject_id = sub.id
	JOIN students AS st ON g.student_id = st.id
	JOIN [groups] AS gr ON gr.id  = st.group_id 
WHERE gr.id = 2 AND sub.id = 4
ORDER BY Student;