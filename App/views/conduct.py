from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.database import db

from App.controllers import (
    get_all_students,
    get_all_students_json,
    search_all_students,
    get_all_reviews_json,
    search_all_reviews,
    search_all_students_json,
    search_all_reviews_byid
)

from App.models import Student, Review

conduct_views = Blueprint('conduct_views', __name__, template_folder='../templates')


#VIEW ALL STUDENTS
@conduct_views.route('/conduct', methods=['GET'])
def conduct_page():
    students = get_all_students_json() #from conduct controller
    return jsonify(students)




#ADD STUDENT
@conduct_views.route('/conduct/add', methods=['POST'])
def addStudent():
  #receive from json request instead of from form data, backend only
  data = request.get_json() 
  
  newstudent = Student(name = data['name'] , studentId = data['studentId'], faculty = data['faculty'], year = data['year'], kpoints = 10)
  
  if newstudent: #if already exists
    db.session.merge(newstudent)
    db.session.commit()
  else:
    db.session.add(newstudent)
    db.session.commit()

  return 'Student List Updated'
    

#SEARCH STUDENT
@conduct_views.route('/conduct/search', methods=['GET'])
def searchStudents():
    data = request.get_json() 
    student = search_all_students(data['id'])
    if student:
      return jsonify(student)
    else:
      return 'No student found by that ID'




#DELETE STUDENT
@conduct_views.route('/conduct/delete', methods=['DELETE'])
def deleteStudent():
    data = request.get_json() 
    student = search_all_students_(data['id'])

    if student:
      db.session.delete(student)
      db.session.commit()
      return 'Student Deleted'
    else:
      return 'No student found by that ID'


#ADD REVIEW FOR STUDENT
@conduct_views.route('/conduct/reviewStudent', methods=['POST'])
def reviewStudent():
  data = request.get_json()
      
  thisstudent = search_all_students_(data['studentId'])

  if thisstudent:
    review = Review(text = data['rtext'] , studentId = data['studentId'], upvotes = 0, downvotes = 0, userid = data['id'])
    if review: #already exists
      db.session.merge(review)
      db.session.commit()
    else:
      db.session.add(review)
      db.session.commit()
    return 'Review Added'
  return 'Error: Student not found'



#VIEW STUDENT REVIEWS
@conduct_views.route('/conduct/studentReviews', methods=['GET'])
def allReviews():
    data = request.get_json()
    student = search_all_students_(data['studentId'])
  
    if student:
      studentReviews = get_all_reviews_json(student)
      return jsonify(studentReviews)
    else:
      return 'No student found by that ID'




#VOTE ON REVIEW
@conduct_views.route('/conduct/review/vote', methods =['POST'])
def voteReview():
  data = request.get_json() 
  vote = data['vote']
  
  if (vote == 'downvote') or (vote == 'upvote'):
    review = search_all_reviews_byid(data['reviewId'])
    if review == None:
      return 'Error: Review not found.'
    else:
      Review.updateVotes(vote, review)

    studentOBJ = search_all_students_(review.studentId)
    Student.updateKPoints(studentOBJ, vote)
    return 'Vote Added'
    
  return 'Error: Vote must be upvote or downvote'



#DELETE REVIEW
@conduct_views.route('/conduct/deleteReview', methods=['DELETE'])
def deleteReview():
  data = request.get_json()
  student = search_all_students_(data['studentId'])
  review = search_all_reviews(student.studentId) 
  
  if review:
    # if (data['currentuser'] != review.userid):
    #   return 'You do not have authorization to delete this review.'
    # else:
    db.session.delete(review)
    db.session.commit()
    return 'Review Deleted'

  return 'Incorrect Review Id'





