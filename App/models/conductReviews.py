from App.database import db #ensure all pages import correctly

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

  def toJSON(self):
    return{
      'reviewId':self.reviewId,
      'text':self.text,
      'studentId':self.studentId,
      'upvotes':self.upvotes,
      'downvotes':self.downvotes,
      'userid':self.userid,
    }

  def updateVotes(vote, review):
    if vote == "upvote":
      review.upvotes = review.upvotes + 1
    else:
      review.downvotes = review.downvotes + 1
    