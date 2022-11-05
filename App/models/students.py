from App.database import db


class Student(db.Model):
  __tablename__ = 'Student'
  studentid = db.Column(db.String, primary_key=True)
  name = db.Column(db.String, nullable=False)
  faculty = db.Column(db.String, nullable=False)
  year = db.Column(db.Integer, nullable=False)
  kpoints = db.Column(db.Integer)
  reviews = db.relationship('Review', backref='Student')

  def _init_(self, studentid, name, faculty, year, kpoints):
    self.studentid = studentid
    self.name = name
    self.faculty = faculty
    self.year = year
    self.kpoints = kpoints
    self.reviews = [Review.toDict()]
    
  def toDict(self):
    return {
      'studentid':self.studentid,
      'name':self.name,
      'faculty':self.faculty,
      'year':self.year,
      'kpoints':self.kpoints,
      'reviews':self.Review.toDict()
    }

  def toJSON(self):
    return{
      'studentid':self.studentid,
      'name':self.name,
      'faculty':self.faculty,
      'year':self.year,
      'kpoints':self.kpoints
    }

  def updateKPoints(student, vote):
    if vote == "upvote":
      student.kpoints = student.kpoints + 2
    
    if vote == "downvote":
      student.kpoints = student.kpoints - 2

    return 0
