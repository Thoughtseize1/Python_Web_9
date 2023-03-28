--Знайти які курси читає певний викладач.
SELECT
	t.fullname AS "Teacher name",
	s.title AS "Subject"
FROM teachers t
	JOIN subjects AS s ON s.teacher_id = t.id
WHERE t.id = 2 --Stephen Hawking