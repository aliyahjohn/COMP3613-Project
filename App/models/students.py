from App.database import db


class Student(db.Model):
  __tablename__ = 'Student'
  studentId = db.Column(db.String, primary_key=True)
  name = db.Column(db.String, nullable=False)
  faculty = db.Column(db.String, nullable=False)
  year = db.Column(db.Integer, nullable=False)
  kpoints = db.Column(db.Integer)
  reviews = db.relationship('Review', backref='Student')

  def _init_(self, studentId, name, faculty, year, kpoints):
    self.studentId = studentId
    self.name = name
    self.faculty = faculty
    self.year = year
    self.kpoints = kpoints
    self.reviews = [Review.toDict()]
    
  def toDict(self):
    return {
      'studentId':self.studentId,
      'name':self.name,
      'faculty':self.faculty,
      'year':self.year,
      'kpoints':self.kpoints,
      'reviews':self.Review.toDict()
    }

  def toJSON(self):
    return{
      'studentId':self.studentId,
      'name':self.name,
      'faculty':self.faculty,
      'year':self.year,
      'kpoints':self.kpoints
    }

  def updateKPoints(student):
    if student.reviews:
      i = 0
      while i < len(student.reviews):
        upvotes = student.reviews[i].upvotes * 2.5
        downvotes = student.reviews[i].downvotes * 2.5
        karma = upvotes - downvotes
        student.kpoints = student.kpoints + karma

    return 0
