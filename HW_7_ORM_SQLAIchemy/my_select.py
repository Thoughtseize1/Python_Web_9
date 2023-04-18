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


def select_11(teacher_id=2, student_id=21):
    """
    Середній бал, який певний викладач ставить певному студентові
    """
    result = (
        session.query(
            func.round(func.avg(Grade.grade), 1).label('Success_rate'),
            Student.fullname,
            Teacher.fullname
        )
        .select_from(Grade)
        .join(Discipline)
        .join(Student)
        .join(Teacher)
        .filter(Student.id == student_id, Teacher.id == teacher_id)
        .group_by(Student.id, Teacher.id)
        .all()
    )

    return result[0] if result else tuple(result)


def select_12(group_id=3, discipline_id=1):
    """Оцінки студентів у певній групі з певного предмета на останньому занятті.
    """
    sub_query = (
        session.query(
            Grade.date_of
        )
        .select_from(Grade)
        .join(Student)
        .join(Group)
        .filter(Group.id == group_id, Grade.discipline_id == discipline_id)
        .order_by(desc(Grade.date_of))
        .limit(1)
        .all()
    )
    result = (
        session.query(
            Grade.grade,
            Student.fullname,
            Group.name,
            Grade.date_of
        )
        .select_from(Grade)
        .join(Discipline)
        .join(Student)
        .join(Group)
        .filter(Group.id == group_id, Discipline.id == discipline_id, Grade.date_of == sub_query[0][0])
        .group_by(Student.id, Group.id, Discipline.id, Grade.date_of, Grade.id)
        .order_by(desc(Grade.grade))
        .all()
    )
    return result


if __name__ == '__main__':
    print(select_12())
