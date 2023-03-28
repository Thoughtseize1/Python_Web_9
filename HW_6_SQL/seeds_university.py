from datetime import datetime, timedelta, date
from faker import Faker
from random import randint, choice
import sqlite3
from pprint import pprint


SUBJECTS = [
    "Math",
    "Computer science",
    "Economics",
    "English Language and Literature",
    "Physicist",
    "Business Administration",
    "Mechanical Engineering",
    "Sociology",
]

GROUPS = ["DC_guys", "Star_Wars_guys", "Marvel_guys"]
TEACHERS_FULLNAMES = [
    "Nikola Tesla",
    "Stephen Hawking",
    "Marie Curie",
    "Thomas Edison",
]
NUMBER_OF_TEACHERS = len(TEACHERS_FULLNAMES)
NUMBER_OF_STUDENTS = 55
TEACHERS = []
DB_NAME = "university.db"

my_fake = Faker()


def make_connection(sql, data):
    with sqlite3.connect(DB_NAME) as con:
        cur = con.cursor()
        cur.executemany(sql, data)
        con.commit()


connect = sqlite3.connect("university.db")
cur = connect.cursor()

# ---Adding teachers:
def seed_teachers():
    sql_insert_teachers = "INSERT INTO teachers(fullname) VALUES(?);"
    make_connection(
        sql_insert_teachers,
        zip(
            TEACHERS_FULLNAMES,
        ),
    )


def seed_students():
    sql_insert_students = "INSERT INTO students(fullname, group_id) VALUES(?, ?);"
    students = [my_fake.name() for _ in range(NUMBER_OF_STUDENTS)]
    make_connection(
        sql_insert_students,
        zip(
            students,
            iter(randint(1, len(GROUPS)) for _ in range(NUMBER_OF_STUDENTS)),
        ),
    )


def seed_groups():
    sql_insert_groups = "INSERT INTO groups(name) VALUES(?);"
    make_connection(sql_insert_groups, zip(GROUPS))


def seed_subjects():
    sql_insert_subjects = "INSERT INTO subjects(title, teacher_id) VALUES(?, ?);"
    make_connection(
        sql_insert_subjects,
        zip(
            SUBJECTS, iter(randint(1, NUMBER_OF_TEACHERS) for _ in range(len(SUBJECTS)))
        ),
    )


def get_list_date(start, end):
    result = []
    current_date = start
    while current_date <= end:
        if current_date.isoweekday() < 6:
            result.append(current_date)
        current_date += timedelta(1)
    return result


def seed_grades():
    start_date = datetime.strptime("2022-09-01", "%Y-%m-%d")
    end_date = datetime.strptime("2023-06-11", "%Y-%m-%d")

    sql_insert_grades = (
        "INSERT INTO grades(subject_id, student_id, grade, date_of) VALUES(?, ?, ?, ?);"
    )
    list_days = get_list_date(start_date, end_date)
    grades = []
    for day in list_days:
        random_discipline = randint(1, len(SUBJECTS))
        radom_student = [randint(1, NUMBER_OF_STUDENTS) for _ in range(5)]
        for student in radom_student:
            grades.append((random_discipline, student, randint(1, 12), day.date()))

    make_connection(sql_insert_grades, grades)


if __name__ == "__main__":
    # try:
    #     seed_teachers()
    #     seed_groups()
    #     seed_subjects()
    #     seed_students()
    # except sqlite3.Error as error:
    #     pprint(error)

    seed_grades()
