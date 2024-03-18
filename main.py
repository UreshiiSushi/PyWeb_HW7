"""    1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
    2. Знайти студента із найвищим середнім балом з певного предмета.
    3. Знайти середній бал у групах з певного предмета.
    4. Знайти середній бал на потоці (по всій таблиці оцінок).
    5. Знайти які курси читає певний викладач.
    6. Знайти список студентів у певній групі.
    7. Знайти оцінки студентів у окремій групі з певного предмета.
    8. Знайти середній бал, який ставить певний викладач зі своїх предметів.
    9. Знайти список курсів, які відвідує певний студент.
    0. Список курсів, які певному студенту читає певний викладач."""
from models import Groups, Grades, Students, Studyes, Teachers
from sqlalchemy import create_engine, func, desc
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql+psycopg2://postgres:forpost@localhost/university")
engine.connect()
DBSession = sessionmaker(bind=engine)
session = DBSession()


def print_result(result):
    for line in result:
        if line:
            print(line)


def one():
    query = (
        session.query(
            Students.name, func.round(func.avg(Grades.grade), 2).label("avg_grade")
        )
        .select_from(Grades)
        .join(Students)
        .group_by(Students.id)
        .order_by(desc("avg_grade"))
        .limit(5)
        .all()
    )
    print_result(query)


def two():
    query = (
        session.query(
            Students.name,
            func.round(func.avg(Grades.grade), 2).label("avg_grade"),
            Studyes.name,
        )
        .select_from(Grades)
        .join(Students)
        .join(Groups)
        .join(Studyes)
        .where(Studyes.id == 4)
        .group_by(Students.id)
        .group_by(Students.name)
        .group_by(Studyes.name)
        .order_by(desc("avg_grade"))
        .limit(1)
        .all()
    )
    print_result(query)


def three():
    query = (
        session.query(
            Groups.name,
            func.round(func.avg(Grades.grade), 2).label("avg_grade"),
            Studyes.name,
        )
        .select_from(Grades)
        .join(Students)
        .join(Groups)
        .join(Studyes)
        .where(Studyes.id == 3)
        .group_by(Studyes.name)
        .group_by(Groups.id)
        .all()
    )
    print_result(query)


def four():
    query = (
        session.query(
            func.round(func.avg(Grades.grade), 2).label("avg_grade"),
        )
        .select_from(Grades)
        .all()
    )
    print_result(query)


def five():
    query = (
        session.query(Teachers.name, Studyes.name)
        .select_from(Teachers)
        .join(Studyes)
        .where(Teachers.id == 5)
        .all()
    )
    print_result(query)


def six():
    query = (
        session.query(
            Groups.name,
            Students.name,
        )
        .select_from(Groups)
        .join(Students)
        .where(Groups.id == 3)
        .all()
    )
    print_result(query)


def seven():
    query = (
        session.query(
            Groups.name,
            Students.name,
            Studyes.name,
            Grades.grade,
        )
        .select_from(Grades)
        .join(Students)
        .join(Groups)
        .join(Studyes)
        .where(Studyes.id == 4)
        .where(Groups.id == 3)
        .all()
    )
    print_result(query)


def eight():
    query = (
        session.query(
            Teachers.name,
            Studyes.name,
            func.round(func.avg(Grades.grade), 2),
        )
        .select_from(Grades)
        .join(Studyes)
        .join(Teachers)
        .where(Teachers.id == 5)
        .group_by(Teachers.id)
        .group_by(Studyes.name)
        .all()
    )
    print_result(query)


def nine():
    query = (
        session.query(
            Students.name,
            Studyes.name,
        )
        .select_from(Grades)
        .join(Studyes)
        .join(Students)
        .where(Students.id == 4)
        .group_by(Students.id)
        .group_by(Studyes.name)
        .all()
    )
    print_result(query)


def ten():
    query = (
        session.query(
            Students.name,
            Studyes.name,
            Teachers.name,
        )
        .select_from(Grades)
        .join(Studyes)
        .join(Students)
        .join(Teachers)
        .where(Teachers.id == 5)
        .where(Students.id == 6)
        .group_by(Students.name)
        .group_by(Teachers.id)
        .group_by(Studyes.name)
        .all()
    )
    print_result(query)


if __name__ == "__main__":
    dic = {
        "1": one,
        "2": two,
        "3": three,
        "4": four,
        "5": five,
        "6": six,
        "7": seven,
        "8": eight,
        "9": nine,
        "0": ten,
    }
    answer = None
    while answer != "e":
        print(__doc__)
        answer = input("What query do you want to execute? (type e for exit)")
        if answer.isdigit():
            print()
            dic.get(answer)()
            print()