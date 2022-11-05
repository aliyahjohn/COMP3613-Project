from App.models import Review, Student
from App.database import db
from json import *
from App.controllers import(
    get_all_students,
    get_all_students_json,
    search_all_students_,
    search_all_students
)

def reviewStudent(studentId, data):
  #data = request.get_json()
      
  thisstudent = search_all_students_(studentId)

  if thisstudent:
    review = Review(text= data , studentId = thisstudent.studentId, upvotes = 0, downvotes = 0, userid = user.id)
    db.session.add(review)
    db.session.commit()
    return 'Review Added'
  return 'Error: Student not found'


def get_all_reviews_json(student):
    reviews = student.reviews
    if not reviews:
        return []
    reviews = [review.toJSON() for review in reviews]
    return reviews 

def search_all_reviews(id):
    review = Review.query.filter_by(studentId=id).first()
    if review: 
        return review
    return None

def search_all_reviews_byid(id):
    review = Review.query.filter_by(reviewId=id).first()
    if review: 
        return review
    return None

