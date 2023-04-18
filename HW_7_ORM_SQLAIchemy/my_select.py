from sqlalchemy import func, desc, select, and_

from src.models import Teacher, Student, Discipline, Grade, Group
from src.db import session


def select_1():
    """
    Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
    :return: list[dict]
    """
    result = session.query(Student.fullname,
                           func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade) \
        .join(Student) \
        .group_by(Student.id) \
        .order_by(desc('avg_grade')) \
        .limit(5).all()
    return result


def select_2(discipline="Defence Against the Dark Arts"):
    """
    Знайти студента із найвищим середнім балом з певного предмета.
    :return: list[dict]
    """
    result = session.query(Discipline.name,
                           Student.fullname,
                           func.max(Grade.grade).label('max_grade')) \
        .select_from(Grade) \
        .join(Discipline) \
        .join(Student) \
        .filter(Discipline.name == discipline) \
        .group_by(Student.id, Discipline.name) \
        .order_by(desc('max_grade')) \
        .first()
    return result


def select_3(discipline="Defence Against the Dark Arts"):
    """
    Знайти середній бал у групах з певного предмета.
    """
    result = session.query(Discipline.name,
                           Group.name,
                           func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade) \
        .join(Discipline) \
        .join(Student) \
        .join(Group) \
        .filter(Discipline.name == discipline) \
        .group_by(Group.name, Discipline.name) \
        .all()
    return result


def select_4():
    """
    Знайти середній бал на потоці (по всій таблиці оцінок).
    """
    result = session.query(func.round(func.avg(Grade.grade), 2).label('avg_grade_from_all')) \
        .select_from(Grade) \
        .all()
    return result


def select_5(teacher="Albus Dumbledore"):
    """
    Знайти які курси читає певний викладач.
    """
    result = session.query(
        Discipline.name
    ) \
        .select_from(Discipline) \
        .join(Teacher) \
        .filter(Teacher.fullname == teacher) \
        .all()
    return [row[0] for row in result]


def select_6(group_name="Gryffindor"):
    """
    Знайти список студентів у певній групі.
    """
    result = session.query(
        Student.fullname
    ) \
        .select_from(Student) \
        .join(Group) \
        .filter(Group.name == group_name) \
        .all()
    return [row[0] for row in result]


def select_7(group_name="Gryffindor", discipline="Defence Against the Dark Arts"):
    """
    Знайти оцінки студентів у окремій групі з певного предмета.
    """
    result = session.query(
        Student.fullname,
        Group.name,
        Discipline.name,
        Grade.grade
    ) \
        .select_from(Grade) \
        .join(Discipline) \
        .join(Student) \
        .join(Group) \
        .filter(Group.name == group_name, Discipline.name == discipline) \
        .all()
    return result


def select_8(teacher="Albus Dumbledore"):
    """
    Знайти середній бал, який ставить певний викладач зі своїх предметів.
    """
    result = session.query(
        Teacher.fullname,
        Discipline.name,
        func.round(func.avg(Grade.grade), 2)
    ) \
        .select_from(Grade) \
        .join(Discipline) \
        .join(Teacher) \
        .filter(Teacher.fullname == teacher) \
        .group_by(Teacher.fullname, Discipline.name) \
        .all()

    return result


def select_9(student_id=5):
    """
    Знайти список курсів, які відвідує студент.
    """
    result = session.query(
        Student.fullname,
        Discipline.name) \
        .select_from(Grade) \
        .join(Discipline) \
        .join(Student) \
        .filter(Student.id == student_id) \
        .group_by(Student.fullname, Discipline.name) \
        .all()

    return result


def select_10(teacher_id=1, student_id=12):
    """
    Список курсів, які певному студенту читає певний викладач.
    """
    result = session.query(
        Discipline.name,
        Student.fullname,
        Teacher.fullname) \
        .select_from(Grade) \
        .join(Discipline) \
        .join(Student) \
        .join(Teacher) \
        .where(and_(Student.id == student_id, Teacher.id == teacher_id)) \
        .group_by(Discipline.name, Student.fullname, Teacher.fullname) \
        .all()

    return [row[0] for row in result]


if __name__ == '__main__':
    print(select_10())
