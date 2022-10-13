from App.models import Student
from App.database import db

def get_all_students():
    return Student.query.all()

def get_all_students_json():
    students = Student.query.all()
    if not students:
        return []
    students = [student.toJSON() for student in students]
    return students #return always

def search_all_students(id):
    student = Student.query.filter_by(studentId=id).first()
    if student: 
        return student
    return None
