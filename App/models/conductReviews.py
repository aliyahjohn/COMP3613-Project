from App.database import db

class Review(db.Model):
  __tablename__ = 'Review'
  reviewId = db.Column(db.Integer, primary_key=True)
  text = db.Column(db.String, nullable=False)
  studentId = db.Column(db.Integer, db.ForeignKey('Student.studentId'), nullable=False)  
  id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
  user = db.relationship('User') 

  def _init_(self, id, text, studentId):
    self.id = id
    self.text = text
    self.studentId = studentId
    self.id = id
    self.user = user


    
