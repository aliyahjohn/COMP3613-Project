from App.models import Review
from App.database import db
from json import *

def create_review(text, studentId, upvotes, downvotes, userid):
    review = Review(text = text , studentId = studentId, upvotes = upvotes, downvotes = downvotes, userid = userid)
    if review: #already exists
      db.session.merge(review)
      db.session.commit()
    else:
      db.session.add(review)
      db.session.commit()
   

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


def delete_review(review):
    db.session.delete(review)
    db.session.commit()
    return None