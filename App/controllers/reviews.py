from App.models import Review
from App.database import db
from json import *


def get_all_reviews_json():
    reviews = Review.query.all()
    if not reviews:
        return []
    reviews = [review.toJSON() for review in reviews]
    return reviews #return always

def search_all_reviews(id):
    review = Review.query.filter_by(studentId=id).first()
    if review: 
        return review
    return None
