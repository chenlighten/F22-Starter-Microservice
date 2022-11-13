import json
from datetime import datetime
from flask import Flask, Response, request
from flask_cors import CORS
from tables import Course, Section, Attendance
from data_access import DataAccess


# Create the Flask application object.
app = Flask(__name__,
            static_url_path='/',
            static_folder='static/class-ui/',
            template_folder='web/templates')

CORS(app)

dao = DataAccess("localhost", "root", "123456", "f22_databases")


'''
Global error handler, we can raise exceptions anywhere in the code,
and error message will be returned to the request sender.
Todo: more return codes and messages.
'''
@app.errorhandler(Exception)
def handle_exception(e):
    return Response(
        str(e),
        status = 500,
        content_type="application.json"
    )


@app.get("/api/health")
def get_health():
    t = str(datetime.now())
    msg = {
        "name": "F22-Starter-Microservice",
        "health": "Good",
        "at time": t
    }

    # DFF TODO Explain status codes, content type, ... ...
    result = Response(json.dumps(msg), status=200, content_type="application/json")

    return result


'''
Create a new course.
Request body:
{
    "course_name": "{some name}",
    "prof_name": "{professor's name}",
    "time": "{a string describing the time for the course}"
}
Course name must be unique.
'''
@app.post("/api/courses/create")
def courses_create_post():
    json_body = request.json()
    course = Course(
        course_name = json_body.get("course_name"),
        prof_name = json_body.get("prof_name"),
        time = json_body["time"])
    
    dao.insert(course)

    return Response("SUCCESS", status = 200, content_type="text/plain")


'''
Get all the courses information.
'''
@app.get("/api/courses")
def courses_all_get():
    res: list[str] = list(map(str, dao.select_all(Course)))
    return Response(json.dumps(res), status = 200, content_type="application/json")


'''
Get the information of one certain course.
'''
@app.get("/api/courses/<course_name>")
def courses_get(course_name: str):
    res: Course = dao.select_one_by(Course, lambda: Course.course_name == course_name)
    return Response(str(res), status = 200, content_type="application/json")


'''
Create a new section for a course.
Course name should be written in the path.
Request body should contain the date for the course section:
{
    "year": 2022,
    "month": 10,
    "day": 1
}
'''
@app.post("/api/courses/<course_name>/sections/create")
def sections_create_post(course_name: str):
    json_body = request.json()
    course: Course = dao.select_one_by(Course, lambda: Course.course_name == course_name)
    date = datetime.date(
        json_body.get("year"),
        json_body.get("month"),
        json_body.get("day")
    )

    section = Section(course_id = course.course_id, section_date = date)

    dao.insert(section)
    
    return Response("SUCCESS", status = 200, content_type="text/plain")


'''
Query all the sections for a course.
'''
@app.get("/api/courses/<course_name>/sections")
def sections_all_get(course_name: str):
    course: Course = dao.select_one_by(Course, lambda: Course.course_name == course_name)
    res: list[str] = list(map(str, dao.select_all_by(Section, lambda: Section.course_id == course.course_id)))
    return Response(json.dumps(res), status = 200, content_type="application/json")


'''
Checkin a student for a course section.
Course name should be in the path.
Request body should contain the date and student id.
{
    "year": 2022,
    "month": 10,
    "day": 1,
    "student_id": "{student's uni or some id}"
}
'''
@app.post("/api/courses/<course_name>/checkin")
def courses_checkin_post(course_name: str):
    course: Course = dao.select_one_by(Course, lambda: Course.course_name == course_name)
    json_body = request.json()
    date = datetime.date(
        int(json_body.get("year")),
        int(json_body.get("month")),
        int(json_body.get("day"))
    )
    student_id = json_body.get("student_id")

    section: Section = dao.select_one_by(Section,
        lambda: Section.course_id == course.course_id and Section.section_date == date)
    atten: Attendance = Attendance(student_id = student_id, section_id = section.section_id)

    dao.insert(atten)

    return Response("SUCCESS", status = 200, content_type="text/plain")


'''
Query how many students were present in all the sections of a course.
'''
@app.get("/api/courses/<course_name>/presence")
def courses_presence_get(course_name: str):
    course: Course = dao.select_one_by(Course, lambda: Course.course_name == course_name)
    sections: list[Section] = dao.select_all_by(Section, lambda: Section.course_id == course.course_id)

    res: list[dict] = [{str(section.section_date): 
            dao.select_size_by(Attendance, lambda: Attendance.section_id == section.section_id)}
        for section in sections]
    
    return Response(json.dumps(res), status = 200, content_type="application/json")


'''
Query how many times a student was present in all courses.
'''
@app.get("/api/students/<student_id>/presence")
def students_presence_get(student_id: str):
    # First need to check if the student id is valid
    # Rely on student enrollment service
    
    # Very bad implementation, modify it with more effective query later
    res = {}
    courses: list[Course] = dao.select_all(Course)
    for course in courses:
        course_sections = dao.select_all_by(Section.section_id, lambda: Section.course_id == course.course_id)
        student_sections = dao.select_all_by(Attendance.section_id, lambda: Attendance.student_id == student_id)
        res[course.course_name] = len(set(course_sections) & set(student_sections))
    
    return Response(json.dumps(res), status = 200, content_type="application/json")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011)
