import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import create_db
from App.models import Student
from App.controllers import (
    create_student,
    get_all_students_json,
    search_all_students,
    search_all_students_json,
    delete_student
)

from wsgi import app


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''

class UserUnitTests(unittest.TestCase):

    def test_student_profile(self):
        student = Student("spongebob", "816000001", "FST", "2020", "10")
        assert student.name == "spongebob"



'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db(app)
    yield app.test_client()
    os.unlink(os.getcwd()+'/App/test.db')


class StudentsIntegrationTests(unittest.TestCase):
    
    #checks if a student profile was created
    def test_create_student(self):
        student = create_student("Betty", "816000000", "FST", "2020", "10")
        assert student.name == "Betty"

    #checks if data from the student table was retrieved
    def test_get_all_students_json(self):
        students_json = get_all_students_json()
        self.assertListEqual([{"name":"Betty", "studentId":"816000000", "faculty":"FST", "year":2020, "kpoints":10}], students_json)

    #checks to see if a student was be found by ID
    def test_search_all_students(self):
        id = "816000000"
        student_json = search_all_students(816000000)
        assert student_json.name == "Betty"

    #checks to see if name was be changed    
    def test_update_student_name(self):
        student = search_all_students_json("816000000")
        update_student_name("816000001", "Boop")
        assert student.name == "Boop"

    #checks to see if faculty was be changed    
    def test_update_student_faculty(self):
        student = search_all_students_json("816000000")
        update_student_faculty("816000001", "FHE")
        assert student.faculty == "FHE"

    #checks if student was deleted
    def test_delete_student(self):
        student = search_all_students_(816000000)
        delete_student(student)
        student = search_all_students_(816000000)
        self.assertListEqual(None, student) 
