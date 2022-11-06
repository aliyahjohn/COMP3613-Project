import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import create_db
from App.models import Review
from App.controllers import (
    create_review,
    get_all_reviews_json,
    search_all_reviews,
    delete_review,
    search_all_students_json
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


class ReviewsIntegrationTests(unittest.TestCase):

    #checks to see if a review was created
    def test_create_review(self):
        review = create_review("Great student", "816000000", 0, 0, 1)
        assert review.text == "Great student"

    #checks to see if all reviews for a student was retrieved
    def test_get_all_reviews_json(self):
        student = search_all_students_json(816000000)
        reviews_json = get_all_reviews_json(student) #assume student != None
        self.assertListEqual([{"reviewId":1, "text":"Great student", "studentId":"816000000", "upvotes":0, "downvotes":0, "userid":1}], reviews_json)

    #checks to see if reviews with a certain studentID was retrieved
    def test_search_all_reviews(self):
        id = "816000000"
        review_json = search_all_reviews(816000000)
        assert review_json.text == "Great student"

    #checks to see if review was deleted
    def test_delete_review(self):
        review = search_all_reviews(816000000)
        delete_review(review)
        review = search_all_reviews(816000000)
        self.assertListEqual(None, review) 