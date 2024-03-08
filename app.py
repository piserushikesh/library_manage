from flask import jsonify, make_response, request, render_template
from library_management.functions import get_all_books, get_all_users
from library_management import db
from library_management import app
from library_management.models import Users,Books

@app.route("/welcome")
def welcome():
    return "Welcome To Genzeon Library"

@app.route('/')
def indexLibrarian():
    global isStudent
    isStudent=False
    books = get_all_books()
    return render_template('index.html', books=books)

@app.route('/members')
def indexStudent():
    global isStudent
    isStudent=True
    books = get_all_books()
    return render_template('index.html', books=books, isStudent=isStudent)

@app.route("/book_added", methods=["POST"])
def book_added():
    data = request.json
    bookName = data.get("bookName")
    authorName = data.get("authorName")

    if bookName and authorName:
        book = Books(
            bookName=bookName,
            authorName=authorName,
        )
        db.session.add(book)
        db.session.commit()
        return make_response(
            {"message": "Book added"},
            201
        )
    return make_response(
        {"message": "Unable to add book"},
        500
    )


@app.route("/user_added", methods=["POST"])
def user_added():
    data = request.json
    firstName = data.get("firstName")
    lastName = data.get("lastName")
    email =  data.get("email")

    if firstName and lastName and email :
        user = Users(
            email = email,
            firstName = firstName,
            lastName = lastName
        )
        db.session.add(user)
        db.session.commit()
        return make_response(
            {"message":"User added"},
            201
        )
    return make_response(
            {"message":"Unable to add user"},
            500
        )


@app.route("/update_book/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = Books.query.get(book_id)

    if not book:
        return make_response(
            {"message": f"Book with ID {book_id} not found"},
            404
        )

    data = request.json
    if "bookName" in data:
        book.bookName = data["bookName"]
    if "authorName" in data:
        book.authorName = data["authorName"]
    if "issuerId" in data:
        book.issuerId = data["issuerId"]
    

    db.session.commit()
    return jsonify({"message": f"Book with ID {book_id} updated successfully"})

@app.route('/add_book', methods=['POST'])
def add_book():
    bookName = request.form['bookName']
    authorName = request.form['authorName']
    new_book = Books(bookName=bookName, authorName=authorName)
    db.session.add(new_book)
    db.session.commit()
    # books.append({'bookName': bookName, 'authorName': authorName})
    return render_template('index.html', books=get_all_books())

@app.route("/update_user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = Users.query.get(user_id)

    if not user:
        return make_response(
            {"message": f"User with ID {user_id} not found"},
            404
        )

    data = request.json
    if "firstName" in data:
        user.firstName = data["firstName"]
    if "lastName" in data:
        user.lastName = data["lastName"]
    if "email" in data:
        user.email = data["email"]
    

    db.session.commit()
    return jsonify({"message": f"User with ID {user_id} updated successfully"})


# @app.route("/delete_book/<int:book_id>", methods=["DELETE"])
# def delete_book(book_id):
#     book = Books.query.get(book_id)

#     if book:
#         db.session.delete(book)
#         db.session.commit()
#         return make_response(
#             {"message": f"Book with ID {book_id} deleted"},
#             200
#         )
#     else:
#         return make_response(
#             {"message": f"Book with ID {book_id} not found"},
#             404
#         )

@app.route('/delete_book/<int:book_id>', methods=['GET'])
def delete_book(book_id):
    book_to_delete = Books.query.get_or_404(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return render_template('index.html', books=get_all_books(), isStudent=isStudent)

@app.route("/delete_user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = Users.query.get(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
        return make_response(
            {"message": f"User with ID {user_id} deleted"},
            200
        )
    else:
        return make_response(
            {"message": f"User with ID {user_id} not found"},
            404
        )


@app.route("/users", methods=["GET"])
def users():
    all_users = get_all_users()
    user_list = []

    for user in all_users:
        user_list.append({
            "id": user.id,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "email": user.email
        })

    return jsonify({"users": user_list})


@app.route("/books", methods=["GET"])
def books():
    all_books = get_all_books()
    book_list = []

    for book in all_books:
        book_list.append({
            "id": book.id,
            "bookName": book.bookName,
            "authorName": book.authorName,
            # Add other attributes as needed
        })

    return jsonify({"books": book_list})


@app.route('/edit_book', methods=['POST'])
def edit_book():
    # Fetch the book from the database
    book = Books.query.get_or_404(request.form['editBookId'])

    # Update the book details based on the form data
    book.bookName = request.form['editBookName']
    book.authorName = request.form['editAuthorName']

    # Commit the changes to the database
    db.session.commit()

    return render_template('index.html', books=get_all_books(), isStudent=isStudent)

@app.route('/search_book', methods=['GET'])
def searchBook():
    searchText = request.args.get('title_or_author', '')
    searchedBooks = Books.query.filter(Books.bookName.ilike(f'%{searchText}%') | Books.authorName.ilike(f'%{searchText}%')).all()
    # searchedBooks = searchBookFunc(searchText, books)
    return render_template('index.html', books=get_all_books(), searchedBooks=searchedBooks, isStudent=isStudent)


if __name__ == "__main__":
    app.run(debug=True,port=5001)