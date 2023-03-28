--Знайти список курсів, які відвідує студент.
SELECT
  st.id AS ID, 
  st.fullname AS Student,
  sub.title AS Subject
FROM grades AS gr
  JOIN subjects AS sub ON gr.subject_id = sub.id
  JOIN students AS st ON gr.student_id = st.id
WHERE st.id = 55 --'Christina King'
GROUP BY Subject;