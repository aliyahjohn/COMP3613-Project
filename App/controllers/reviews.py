from App.models import Review
from App.database import db
from json import *



def get_all_reviews_json(student):
    reviews = student.reviews
    if not reviews:
        return []
    reviews = [review.toJSON() for review in reviews]
    return reviews 

def search_all_reviews(id):
    review = Review.query.filter_by(studentid=id).first()
    if review: 
        return review
    return None

def search_all_reviews_byid(id):
    review = Review.query.filter_by(reviewId=id).first()
    if review: 
        return review
    return None

