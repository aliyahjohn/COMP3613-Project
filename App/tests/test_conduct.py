import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import create_db
from App.models import User
from App.controllers import (
    create_student,
    get_all_students_json,
    search_all_students,
    search_all_students_,
    delete_student
)

from wsgi import app


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''




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

    def test_create_student(self):
        student = create_student("Betty", "816000000", "FST", "2020", "10")
        assert student.name == "Betty"

    def test_get_all_students_json(self):
        students_json = get_all_students_json()
        self.assertListEqual([{"name":"Betty", "studentId":"816000000", "faculty":"FST", "year":2020, "kpoints":10}], students_json)

    def test_search_all_students(self):
        id = "816000000"
        student_json = search_all_students(816000000)
        assert student_json.name == "Betty"

    def test_delete_student(self):
        student = search_all_students_(816000000)
        delete_student(student)
        student = search_all_students_(816000000)
        self.assertListEqual(None, student) 
