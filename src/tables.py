from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import declarative_base
from flask import json

Base = declarative_base()


'''
Data models for attendance microservice.
See db/DDL.sql for the table definitions in database.
'''


class Course(Base):
    __tablename__ = "courses"

    course_id = Column(Integer, primary_key = True, autoincrement = True)
    course_name = Column(String(128), unique = True)
    prof_name = Column(String(128))
    time = Column(String(128))

    def __str__(self) -> str:
        return json.dumps({
            "course_id": self.course_id, "course_name": self.course_name,
            "prof_name": self.prof_name, "time": self.time})


class Section(Base):
    __tablename__ = "sections"

    section_id = Column(Integer, primary_key = True, autoincrement = True)
    course_id = Column(Integer, ForeignKey("courses.course_id"), nullable = False)
    section_date = Column(Date, nullable = False)

    def __str__(self) -> str:
        return json.dumps({
            "section_id": self.section_id,
            "course_id": self.course_id, "section_date": self.section_date})


class Attendance(Base):
    __tablename__ = "attendances"

    section_id = Column(Integer, ForeignKey("sections.section_id"), primary_key = True)
    student_id = Column(Integer, primary_key = True, nullable = False)
