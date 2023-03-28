--Список курсів, які певному студенту читає певний викладач.

SELECT
  sub.title AS Subject,
  st.fullname AS Student,
  t.fullname AS Teacher
FROM grades AS gr
	JOIN subjects AS sub ON gr.subject_id = sub.id
  JOIN students AS st ON gr.student_id = st.id
  JOIN teachers AS t ON sub.teacher_id = t.id
WHERE st.id = 24 AND t.id = 4 --Sudent: Michael Cortez. Teacher: Thomas Edison
GROUP BY Subject;