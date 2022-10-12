from App.database import db

class Review(db.Model):
  __tablename__ = 'Review'
  reviewId = db.Column(db.Integer, primary_key=True)
  text = db.Column(db.String, nullable=False)
  studentId = db.Column(db.Integer, db.ForeignKey('Student.studentId'), nullable=False)  
  upvotes = db.Column(db.Integer, nullable=True)  
  downvotes = db.Column(db.Integer, nullable=True)  
  userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
  user = db.relationship('User') 

  def _init_(self, id, text, studentId, upvotes, downvotes, userid, user):
    self.reviewId = id
    self.text = text
    self.studentId = studentId
    self.upvotes = upvotes
    self.downvotes = downvotes
    self.userid = userid
    self.user = user


    
