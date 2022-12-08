import requests
from threading import Thread
from time import sleep

from data_access import *
from tables import *
from application import app

test_dao = DataAccess("localhost", "root", "123456", "f22_databases")
test_host = "0.0.0.0"
test_port = 5011
test_url = f"http://{test_host}:{test_port}"

def test_env(f):
    def wrapped(*args, **kwargs):
        test_dao.delete_all(Attendance)
        test_dao.delete_all(Section)
        test_dao.delete_all(Course)

        print(f"Begin test {f.__name__} ...")

        f(*args, **kwargs)

        print(f"Test {f.__name__} passed!")
        
        test_dao.delete_all(Attendance)
        test_dao.delete_all(Section)
        test_dao.delete_all(Course)
    return wrapped

@test_env
def test_health():
    res = requests.get(test_url + "/api/health")
    assert(res.status_code == 200)
    assert("Good" in res.text)
    

@test_env
def test_course():
    res = requests.post(test_url + "/api/courses/create", json = {
        "course_name": "Cloud Computing",
        "prof_name": "Donald",
        "time": "Friday"
    })
    assert(res.status_code == 200)
    assert("SUCCESS" in res.text)


    res = requests.post(test_url + "/api/courses/create", json = {
        "course_name": "Operating System",
        "prof_name": "Jason",
        "time": "Friday"
    })
    assert(res.status_code == 200)
    assert("SUCCESS" in res.text)


    res = requests.get(test_url + "/api/courses")
    assert(res.status_code == 200)
    assert("Cloud Computing" in res.text)
    assert("Operating System" in res.text)


    res = requests.get(test_url + "/api/courses/Cloud Computing")
    assert(res.status_code == 200)
    assert("Cloud Computing" in res.text)
    assert("Donald" in res.text)

@test_env
def test_sections():
    res = requests.post(test_url + "/api/courses/create", json = {
        "course_name": "Cloud Computing",
        "prof_name": "Donald",
        "time": "Friday"
    })
    assert(res.status_code == 200)
    assert("SUCCESS" in res.text)


    res = requests.post(test_url + "/api/courses/Cloud Computing/sections/create", json = {
        "year": "2022",
        "month": "10",
        "day": "23"
    })
    print(res.text)
    assert(res.status_code == 200)
    assert("SUCCESS" in res.text)

    res = requests.post(test_url + "/api/courses/Cloud Computing/sections/create", json = {
        "year": "2022",
        "month": "11",
        "day": "24"
    })
    assert(res.status_code == 200)
    assert("SUCCESS" in res.text)

    res = requests.post(test_url + "/api/courses/Cloud Computing/sections/create", json = {
        "year": "2022",
        "month": "11",
        "day": "25"
    })
    assert(res.status_code == 200)
    assert("SUCCESS" in res.text)

    res = requests.post(test_url + "/api/courses/Cloud Computing/sections/create", json = {
        "year": "2022",
        "month": "11",
        "day": "26"
    })
    assert(res.status_code == 200)
    assert("SUCCESS" in res.text)


    res = requests.get(test_url + "/api/courses/Cloud Computing/sections")
    assert(res.status_code == 200)
    assert("26" in res.text)
    assert("25" in res.text)
    assert("24" in res.text)

@test_env
def test_checkin():
    res = requests.post(test_url + "/api/courses/create", json = {
        "course_name": "Cloud Computing",
        "prof_name": "Donald",
        "time": "Friday"
    })
    assert(res.status_code == 200)
    assert("SUCCESS" in res.text)

    res = requests.post(test_url + "/api/courses/Cloud Computing/sections/create", json = {
        "year": "2022",
        "month": "11",
        "day": "23"
    })
    print(res.text)
    assert(res.status_code == 200)
    assert("SUCCESS" in res.text)

    res = requests.post(test_url + "/api/courses/Cloud Computing/sections/create", json = {
        "year": "2022",
        "month": "11",
        "day": "24"
    })
    assert(res.status_code == 200)
    assert("SUCCESS" in res.text)

    res = requests.post(test_url + "/api/courses/Cloud Computing/checkin", json = {
        "year": "2022",
        "month": "11",
        "day": "23",
        "student_id": "1234"
    })
    assert(res.status_code == 200)
    assert("SUCCESS" in res.text)

    res = requests.post(test_url + "/api/courses/Cloud Computing/checkin", json = {
        "year": "2022",
        "month": "11",
        "day": "24",
        "student_id": "1234"
    })
    assert(res.status_code == 200)
    assert("SUCCESS" in res.text)

    res = requests.post(test_url + "/api/courses/Cloud Computing/checkin", json = {
        "year": "2022",
        "month": "11",
        "day": "23",
        "student_id": "5678"
    })
    assert(res.status_code == 200)
    assert("SUCCESS" in res.text)

    res = requests.get(test_url + "/api/courses/Cloud Computing/presence")
    assert("\"2022-11-23\": 2" in res.text)
    assert("\"2022-11-24\": 1" in res.text)

@test_env
def test_students_presence():
    res = requests.post(test_url + "/api/courses/create", json = {
        "course_name": "Cloud Computing",
        "prof_name": "Donald",
        "time": "Friday"
    })
    assert(res.status_code == 200)
    assert("SUCCESS" in res.text)

    res = requests.post(test_url + "/api/courses/Cloud Computing/sections/create", json = {
        "year": "2022",
        "month": "11",
        "day": "23"
    })
    print(res.text)
    assert(res.status_code == 200)
    assert("SUCCESS" in res.text)

    res = requests.post(test_url + "/api/courses/Cloud Computing/sections/create", json = {
        "year": "2022",
        "month": "11",
        "day": "24"
    })
    assert(res.status_code == 200)
    assert("SUCCESS" in res.text)

    res = requests.post(test_url + "/api/courses/Cloud Computing/checkin", json = {
        "year": "2022",
        "month": "11",
        "day": "23",
        "student_id": "1234"
    })
    assert(res.status_code == 200)
    assert("SUCCESS" in res.text)

    res = requests.post(test_url + "/api/courses/Cloud Computing/checkin", json = {
        "year": "2022",
        "month": "11",
        "day": "24",
        "student_id": "1234"
    })
    assert(res.status_code == 200)
    assert("SUCCESS" in res.text)

    res = requests.post(test_url + "/api/courses/Cloud Computing/checkin", json = {
        "year": "2022",
        "month": "11",
        "day": "23",
        "student_id": "5678"
    })
    assert(res.status_code == 200)
    assert("SUCCESS" in res.text)

    res = requests.get(test_url + "/api/students/1234/presence")
    assert("\"Cloud Computing\": 2" in res.text)

    res = requests.get(test_url + "/api/students/5678/presence")
    assert("\"Cloud Computing\": 1" in res.text)
    

if __name__ == '__main__':
    Thread(target=lambda: app.run(test_host, test_port)).start()
    sleep(0.2)
    test_health()
    test_course()
    test_sections()
    test_checkin()
    test_students_presence()