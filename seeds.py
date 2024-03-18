from datetime import datetime
from faker import Faker
from models import Groups, Grades, Students, Studyes, Teachers
from random import randint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

NUMBER_STUDENTS = 50
NUMBER_GROUPS = 3
NUMBER_COURSES = 8
NUMBER_TEACHERS = 5
NUMBER_GRADES = 1000

engine = create_engine("postgresql+psycopg2://postgres:1234Qwe@localhost/university")
engine.connect()
DBSession = sessionmaker(bind=engine)
session = DBSession()


def generate_fake_data(number_students, number_teachers, number_grades):
    fake_students = []
    fake_groups = ["OMT-96-1", "OMT-99-2", "PTM-12-1"]
    fake_courses = [
        "Бази даних",
        "Креслення",
        "Матан",
        "Українська мова",
        "Англійська мова",
        "Економіка",
        "Теормех",
        "Металографія",
    ]
    fake_teachers = []
    fake_grades = []

    fake_data = Faker("uk_UA")
    Faker.seed(0)

    # generate students
    for _ in range(number_students):
        fake_students.append(
            fake_data.first_name_nonbinary() + " " + fake_data.last_name_nonbinary()
        )

    # generate teachers
    for _ in range(number_teachers):
        fake_teachers.append(
            fake_data.first_name_nonbinary() + " " + fake_data.last_name_nonbinary()
        )

    # generate grades
    for _ in range(number_grades):
        fake_grades.append(randint(1, 10))

    return fake_students, fake_groups, fake_courses, fake_teachers, fake_grades


def prepare_data(students, groups, courses, teachers, grades):
    for_students = []
    for student in students:
        for_students.append((student, randint(1, NUMBER_GROUPS)))

    for_studyes = []
    for course in courses:
        for_studyes.append((course, randint(1, NUMBER_TEACHERS)))

    for_grades = []
    for grade in grades:
        for_grades.append(
            (
                grade,
                datetime(2023, randint(1, 12), randint(1, 28)).date(),
                randint(1, NUMBER_STUDENTS),
                randint(1, NUMBER_COURSES),
            )
        )

    return for_students, groups, for_studyes, teachers, for_grades


def insert_data_to_db(students, groups, courses, teachers, grades) -> None:
    for item in groups:
        group = Groups(name=item)
        session.add(group)
    session.commit()
    for item in teachers:
        teacher = Teachers(name=item)
        session.add(teacher)
    session.commit()
    for item in students:
        student = Students(name=item[0], group_id=item[1])
        session.add(student)
    session.commit()
    for item in courses:
        study = Studyes(name=item[0], teacher_id=item[1])
        session.add(study)
    session.commit()
    for item in grades:
        grade = Grades(
            grade=item[0], date=item[1], student_id=item[2], study_id=item[3]
        )
        session.add(grade)

    session.commit()


if __name__ == "__main__":
    students, groups, courses, teachers, grades = prepare_data(
        *generate_fake_data(NUMBER_STUDENTS, NUMBER_TEACHERS, NUMBER_GRADES)
    )
    insert_data_to_db(students, groups, courses, teachers, grades)