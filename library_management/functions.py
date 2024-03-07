from .models import Books, Users 
from . import db

def get_all_users():
    """Get all users from the database."""
    users = Users.query.all()
    return users

def get_all_books():
    """Get all books from the database."""
    books = Books.query.all()
    return books
