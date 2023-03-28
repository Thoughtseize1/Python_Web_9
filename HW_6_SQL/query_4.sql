--Знайти середній бал на потоці (по всій таблиці оцінок).
SELECT
	ROUND(AVG(rg.grade),2) as average_grade
FROM grades AS rg;