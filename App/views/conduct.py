from flask import Blueprint, redirect, render_template, request, send_from_directory

conduct_views = Blueprint('conduct_views', __name__, template_folder='../templates')

@conduct_views.route('/conduct', methods=['GET'])
def conduct_page():
    students = Student.query.all()
    return render_template('conduct.html')


#RETURN RENDER TEMPLATE STATEMENTS OF NO USE BECAUSE NO UI, INSTEAD INFO WILL BE PRINTED TO CONSOLE
#/POSTMAN RETURN

@conduct_views.route('/conduct/add', methods=['GET', 'POST'])
def addStudent():

    newstudent = Student(name = data['name'] , studentId = data['studentId'], faculty = data['faculty'], year = data['year'], kpoints = data['kpoints'])
    if newstudent: #already exists
      db.session.merge(newstudent)
      db.session.commit()
    else:
      db.session.add(newstudent)
      db.session.commit()

    students = Student.query.all()
    # return render_template('conduct.html', student = 0, students = students)
    



@conduct_views.route('/conduct/search', methods=['GET'])
def searchStudents():
    data = request.form 
    student = Student.query.filter_by(studentId=data['studentId']).first()
#return student 

@conduct_views.route('/conduct/<studentId>', methods=['GET'])
def displayStudentProfile(id):
    student = Student.query.filter_by(studentId = id).first()
#return student profile 
#list of reviews are part of student profile: can upvote or downvote each review
#update karma points
    reviews = Review.query.all(studentId = id).first()
    for review in reviews:
        if student.reviews:
            upvotes = thisstudent.review.upvotes
            downvotes = thisstudent.review.downvotes

            #calc

        totalkP = totalkP + karmapoints
    
    thisstudent.kpoints = totalkP
    db.session.commit()



@conduct_views.route('/conduct/review/<studentId>', methods=['GET', 'POST'])
def reviewStudent(id):
  data = request.form
  thisstudent = Student.query.filter_by(isbn = data['id']).first()
      
  if thisstudent:
    review = Review(text = data['rtext'] , studentId = Student(studentId = thisstudent.studentId), upvotes = 0, downvotes = 0)
    if review:
      db.session.merge(review)
      db.session.commit()
    else:
      db.session.add(review)
      db.session.commit()
       
    #update karma points
    for review in reviews:
        if student.reviews:
            upvotes = thisstudent.review.upvotes
            downvotes = thisstudent.review.downvotes

            #calc

        totalkP = totalkP + karmapoints
    
    thisstudent.kpoints = totalkP
    db.session.commit()
    

#DELETE REVIEW
@conduct_views.route('/conduct/<reviewId>/<studentId>', methods=['DELETE'])
def deleteReview(revieId, studentId):
  student = Student.query.filter_by(studentId = studentId).first()
  review = Review.query.filter_by(reviewId = student.reviews.reviewId).first()
  
  if review:
    db.session.delete(review)
    db.session.commit()


#DELETE STUDENT
@conduct_views.route('/conduct/delete/<studentId>', methods=['DELETE'])
def deleteStudent(id):
  student = Student.query.filter_by(studentId = studentId).first()
  
  if review:
    db.session.delete(student)
    db.session.commit()


