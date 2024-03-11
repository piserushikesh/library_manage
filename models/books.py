from app import db

class Books(db.Model):
    __tablename__ = "Books"
    id = db.Column(db.Integer, primary_key=True)
    bookName = db.Column(db.String(50), nullable = False)
    authorName = db.Column(db.String(50), nullable = False)
    issuerId = db.Column(db.Integer, db.ForeignKey("Users.id"))

    @property
    def serialize(self):

        return {
            "id": self.id,
            "bookName":self.bookName

        }