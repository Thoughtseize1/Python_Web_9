--Знайти середній бал у групах з певного предмета.
SELECT
g.name AS "Group name",
ROUND(AVG(gr.grade),2) as Average_grade
FROM grades as gr
	JOIN students AS s ON s.id = gr.student_id
	JOIN groups as g ON s.id = g.id
GROUP BY g.name