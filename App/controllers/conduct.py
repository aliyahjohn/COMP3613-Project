from App.models import Student
from App.database import db


def create_student(name , studentId, faculty, year, kpoints):
    newstudent = Student(name = name, studentId = studentId, faculty = faculty, year = year, kpoints = kpoints)
    return newstudent

def get_all_students():
    return Student.query.all()

def get_all_students_json():
    students = Student.query.all()
    if students:
        students = [student.toJSON() for student in students]
        return students
    if not students:
        return "No Students Found"

def search_all_students(id): 
    student = Student.query.filter_by(studentId=id).first()
    if student: 
        return student
    return None

def search_all_students_json(id): 
    student = Student.query.filter_by(studentId=id).first()
    if student: 
        student = student.toJSON()
        return student
    return None

def delete_student(student):
    db.session.delete(student)
    db.session.commit()
    return None

def update_student_name(id, data): ##return object no JSON
    student = Student.query.filter_by(studentId=id).first()
    if student:
        student.name = data
        db.session.add(student)
        return db.session.commit()
    return None

def update_student_faculty(id, data): ##return object no JSON
    student = Student.query.filter_by(studentId=id).first()
    if student:
        student.faculty = data
        db.session.add(student)
        return db.session.commit()
    return None
