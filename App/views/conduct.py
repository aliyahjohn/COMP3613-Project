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

@conduct_views.route('/conduct', methods=['GET'])
def conduct_page():
    students = get_all_students_json() #from conduct controller
    return jsonify(students)


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
    


@conduct_views.route('/conduct/search', methods=['GET'])
def searchStudents():
    data = request.get_json() 
    student = search_all_students(data['id'])
    if student:
      return jsonify(student)
    return 'No student found by that ID'



@conduct_views.route('/conduct/<studentId>', methods=['GET'])
def displayStudentProfile(id):
  ##view student profile with all reviews
    thisstudent = search_all_students(studentId)
    student = search_all_students(data['id'])
    if student:
      return jsonify(student)
    return 'No student found by that ID'


#ADD REVIEW FOR STUDENT
@conduct_views.route('/conduct/review/<studentId>', methods=['GET', 'POST'])
def reviewStudent(id):
  # data = request.form
  thisstudent = search_all_students(id)
      
  if thisstudent:
    review = Review(text = data['rtext'] , studentId = Student(studentId = thisstudent.studentId), upvotes = 0, downvotes = 0)
    if review:
      db.session.merge(review)
      db.session.commit()
    else:
      db.session.add(review)
      db.session.commit()
       
       #CALC OF KARMA POINTS SHOULD BE A FUNCTION WITHIN ONE OF THE MODEL FILES
    #update karma points
    for review in reviews:
        if student.reviews:
            upvotes = thisstudent.review.upvotes
            downvotes = thisstudent.review.downvotes

            #calc needed to product karmapoints - possible for loop 
            upVScore = upvotes * 2.5
            downVScore = downvotes * 2.5
            karmapoints = upVscore - downVScore
            
        totalkP = totalkP + karmapoints
    
    thisstudent.kpoints = totalkP
    db.session.commit()
  
#ADD UPVOTE FOR A REVIEW
#ADD DOWNVOTE FOR A REVIEW


#DELETE REVIEW
@conduct_views.route('/conduct/<reviewId>/<studentId>', methods=['DELETE'])
def deleteReview(reviewId, studentId):
  student = search_all_students(studentId)
  review = search_all_reviews(studentId) 
  
  if review:
    db.session.delete(review)
    db.session.commit()
    return 'Review Deleted'
  return 'No review found by that ID'




#DELETE STUDENT
@conduct_views.route('/conduct/delete/<studentId>', methods=['DELETE'])
def deleteStudent(id):
  student = search_all_students(studentId)
  
  if student:
    db.session.delete(student)
    db.session.commit()
    return 'Student Deleted'
  return 'No student found by that ID'

