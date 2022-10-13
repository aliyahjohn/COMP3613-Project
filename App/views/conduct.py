from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.database import db

from App.controllers import (
    get_all_students,
    get_all_students_json,
    search_all_students,
    get_all_reviews_json,
    search_all_reviews
)

from App.models import Student

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
  
  newstudent = Student(name = data['name'] , studentId = data['studentId'], faculty = data['faculty'], year = data['year'], kpoints = 0)
  
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




#DELETE STUDENT: BUGGED
@conduct_views.route('/conduct/delete', methods=['DELETE'])
def deleteStudent():
    data = request.get_json() 
    student = search_all_students(data['id'])
    if student:
      db.session.delete(student)
      db.session.commit()
    else:
      return 'No student found by that ID'
      


#ADD REVIEW FOR STUDENT: NOT TESTED
@conduct_views.route('/conduct/reviewStudent', methods=['POST'])
def reviewStudent():
  data = request.get_json()
      
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


#VOTE ON REVIEW: NOT TESTED
@conduct_views.route('/conduct/review/vote', methods =['POST'])
def voteReview():
  data = request.get_json() 
  vote = data['vote']
  review = search_all_reviews(data['reviewId'])

  if review == None:
    return 'Incorrect Review ID.'

  student = search_all_students(data['studentId'])
  if student == None:
    return 'Incorrect Student ID.'

  if (vote == "downvote") OR (vote == "upvote"):
    Review.updateVotes(vote, review)
    Student.updateKPoints(student)
    return 'Vote Added'
  return 'Error: Vote must be upvote or downvote'


#DELETE REVIEW: NOT TESTED
@conduct_views.route('/conduct/deleteReview', methods=['DELETE'])
def deleteReview():
  data = request.get_json()
  review = search_all_reviews(data['reviewId']) 
  
  if review:
    db.session.delete(review)
    db.session.commit()
    return 'Review Deleted'
  return 'Incorrect Review Id'





