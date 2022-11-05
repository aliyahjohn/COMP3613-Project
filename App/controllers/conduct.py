from App.models import Student
from App.database import db

def create_student(name,studentId,faculty,year,kpoints):
    newstudent = Student(name = data['name'] , studentId = data['studentId'], faculty = data['faculty'], year = data['year'], kpoints = 10)
    db.session.add(newstudent)
    db.session.commit()
    return newstudent

def get_all_students():
    return Student.query.all()

def get_all_students_json():
    students = Student.query.all()
    if not students:
        return 'No Students.'
    students = [student.toJSON() for student in students]
    return students #return always

def search_all_students(id):
    student = Student.query.filter_by(studentId=id).first()
    if student: 
        student = student.toJSON()
        return student
    return None

def search_all_students_json(id): ##return object no JSON
    student = Student.query.filter_by(studentId=id).first()
    if student: 
        return student
    return None

def delete_student(id):
   student = search_all_students_json(id)
   if student:
     db.session.delete(student)
     db.session.commit()
     return 'Student Deleted'
   else:
     return 'No student found by that ID'

