from App.database import db

class Student(db.Model):
  __tablename__ = 'Student'
  studentId = db.Column(db.String, primary_key=True)
  fName = db.Column(db.String, nullable=False)
  lName = db.Column(db.String, nullable=False)
  faculty = db.Column(db.String, nullable=False)
  year = db.Column(db.Integer, nullable=False)
  kpoints = db.Column(db.Integer, nullable=False)
  reviews = db.relationship('Review', backref='Student')

  def _init_(self, studentId, fName, lName):
    self.studentId = studentId
    self.fName = fName
    self.lName = lName
    self.faculty = faculty
    self.year = year
    self.kpoints = kpoints
    self.reviews = [Review.toDict()]
    
  def toDict(self):
    return {
      'studentId':self.studentId,
      'fName':self.fName,
      'lName':self.lName, 
      'faculty':self.faculty,
      'year':self.year,
      'kpoints':self.kpoints,
      'reviews':self.Review.toDict()
    }