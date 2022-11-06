import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import create_db
from App.models import User, Student
from App.controllers import (
    create_user,
    get_all_users_json,
    authenticate,
    get_user,
    get_user_by_username,
    update_user,
    create_student,
    get_all_students,
    get_all_students_json,
    search_all_students,
    update_student_name,
    update_student_faculty,
    reviewStudent,
    get_all_reviews_json,
    search_all_reviews,
    search_all_students_,
    search_all_reviews_byid
)

from wsgi import app


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass")
        assert user.username == "bob"


    # pure function no side effects or integrations called
    def test_toJSON(self):
        user = User("bob", "bobpass")
        user_json = user.toJSON()
        self.assertDictEqual(user_json, {"id":None, "username":"bob"})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)

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


def test_authenticate():
    user = create_user("bob", "bobpass")
    assert authenticate("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("rick", "bobpass")
        assert user.username == "rick"

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"

class StudentsIntegrationTests(unittest.TestCase):

    def test_create_student(self):
        student = create_student("spongebob", "816000001", "FST", "2020", "10")
        assert student.name == "spongebob"
  
    def test_get_all_student_json(self):
        students_json = get_all_students_json()
        self.assertListEqual([{"studentId":"816000001", "name":"spongebob", "faculty":"FST", "year": 2020, "kpoints": 10}], students_json)  

 
    #def test_delete_student(self):

  
    def test_create_review(self):
        review = reviewStudent("816000001", "good student")
        assert review.text == "good student"


    #def test_delete_review():

    
    #def test_get_all_student_reviews_json(): #not sure if this is json

