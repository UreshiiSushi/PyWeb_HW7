import datetime
from sqlalchemy import create_engine, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import (
    sessionmaker,
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)

# Initializing table into DB, if we need


class Base(DeclarativeBase):
    pass


class Teachers(Base):
    __tablename__ = "teachers"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)


class Groups(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)


class Students(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    group_id = mapped_column(ForeignKey("groups.id"))
    group: Mapped["Groups"] = relationship(Groups)


class Studyes(Base):
    __tablename__ = "studyes"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    teacher_id = mapped_column(ForeignKey("teachers.id"))
    teacher: Mapped["Teachers"] = relationship(Teachers)


class Grades(Base):
    __tablename__ = "grades"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    grade: Mapped[int] = mapped_column(Integer)
    date: Mapped[datetime.datetime] = mapped_column(DateTime)
    student_id = mapped_column(ForeignKey("students.id"))
    student: Mapped["Students"] = relationship(Students)
    study_id = mapped_column(ForeignKey("studyes.id"))
    study: Mapped["Studyes"] = relationship(Studyes)


if __name__ == "__main__":
    engine = create_engine(
        "postgresql+psycopg2://postgres:1234Qwe@localhost/university", echo=True
    )
    engine.connect()
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    Base.metadata.create_all(engine)
    session.commit()