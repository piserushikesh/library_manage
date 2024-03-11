from app import db

class Users(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50), nullable = False)
    lastName = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(100),unique=True, nullable=False)
    books = db.relationship('Books', backref="users")

    def __repr__(self):
        return f'<User {self.firstName} {self.id}>'
    