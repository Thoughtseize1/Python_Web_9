--Знайти список студентів у певній групі.
SELECT
	st.fullname as Student,
	g.name as [Group]
FROM students AS st
	JOIN groups AS g ON g.id = st.group_id 
WHERE g.id = 2 --Star_Wars_guys
ORDER BY Student; 