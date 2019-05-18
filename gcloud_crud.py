from flask import Flask, request, jsonify
from dashboardConfig import app,db,ma


db.metadata.clear()
class LMSUser(db.Model):
    LMSUserID = db.Column(db.Integer, primary_key = True)
    UserName = db.Column(db.String(100),nullable = False, unique = True)
    FirstName = db.Column(db.String(100),nullable = False)
    LastName = db.Column(db.String(100),nullable = False)
    Email = db.Column(db.String(100),nullable = False)
    Book = db.relationship('BookBorrowed', backref='user')


class Book(db.Model):
    BookID = db.Column(db.Integer, primary_key = True)
    Title = db.Column(db.String(100),nullable = False)
    Author = db.Column(db.String(100),nullable = False)
    PublishedDate = db.Column(db.String(100),nullable = False)
    Borrowed = db.relationship('BookBorrowed', backref='bbook')
    def __init__(self,Title,Author,PublishedDate):
        self.Title = Title
        self.Author = Author
        self.PublishedDate = PublishedDate


class BookBorrowed(db.Model):
    BookBorrowedID = db.Column(db.Integer, primary_key = True)
    LMSUserID = db.Column(db.Integer,db.ForeignKey('lms_user.LMSUserID'),nullable=False)
    BookID = db.Column(db.Integer,db.ForeignKey('book.BookID'),nullable=False)
    BorrowedDate = db.Column(db.String(100),nullable=False)
    ReturnedDate = db.Column(db.String(100),nullable=False)
    def __init__(self,LMSUserID,BookID,BorrowedDate,ReturnedDate):
        self.LMSUserID = LMSUserID
        self.BookID = BookID
        self.BorrowedDate = BorrowedDate
        self.ReturnedDate = ReturnedDate

class LmsUserSchema(ma.Schema):
    class Meta:
        fields = ('LMSUserID','UserName','Password','patientAge','FirstName','LastName','Email')

lmsuser_schema = LmsUserSchema()
lmsusers_schema = LmsUserSchema(many=True)

class BookSchema(ma.Schema):
    class Meta:
        fields = ('BookID','Title','Author','PublishedDate')

book_schema = BookSchema()
books_schema = BookSchema(many=True)

class BookBorrowedSchema(ma.Schema):
    class Meta:
        fields = ('BookBorrowedID','LMSUserID','BookID','BorrowedDate','ReturnedDate')

bookborrowed_schema = BookBorrowedSchema()
booksborrowed_schema = BookBorrowedSchema(many=True)


@app.route('/book',methods=["POST"])
def add_book():
    data = request.get_json()
    new_book = Book(data["Title"],data["Author"],data["PublishedDate"])
    db.session.add(new_book)
    db.session.commit()
    return book_schema.jsonify(new_book)

@app.route('/book',methods=["GET"])
def get_all_books():
    all_books = Book.query.all()
    result = books_schema.dump(all_books)
    return  jsonify(result.data)

@app.route("/book/<BookID>",methods=["DELETE"])
def rm_book(BookID):
    book = Book.query.filter_by(BookID=BookID).first()
    db.session.delete(book)
    db.session.commit()

@app.route("/book/t/<title>",methods=["GET"])
def get_title(title):
    books = Book.query.filter(Book.Title==title).all()
    if len(books) > 1:
        result = books_schema.dump(books)
        return jsonify(result.data)
    result = book_schema.dump(books)
    return jsonfy(result.data)

@app.route("/book/a/<author>",methods=["GET"])

def get_author(author):
    books = Book.query.filter(Book.Author==author).all()
    if len(books) > 1:
        result = books_schema.dump(books)
        return jsonify(result.data)
    result = book_schema.dump(books)
    return jsonfy(result.data)
    
@app.route("/book/p/<publisheddate>",methods=["GET"])

def get_publisheddate(publisheddate):
    books = Book.query.filter(Book.PublishedDate==publisheddate).all()
    if len(books) > 1:
        result = books_schema.dump(books)
        return jsonify(result.data)
    result = book_schema.dump(books)
    return jsonfy(result.data)


@app.route("/borrowed",methods=["POST"])
def add_borrowedbook():
    data = request.get_json()
    new_borrowed = BookBorrowed(data["LMSUserID"], data["BookID"], data["BorrowedDate"], data["ReturnedDate"])
    db.session.add(new_borrowed)
    db.session.commit()
    return bookborrowed_schema.jsonify(new_borrowed)

@app.route("/borrowed",methods=["GET"])    
def get_all():
    borrowbooks = BookBorrowed.query.all()
    result = booksborrowed_schema.dump(borrowbooks)
    return  jsonify(result.data)

@app.route("/borrowed/<id>",methods=["DELETE"])
def rm_borrowedbook(id):
    borrowed = BookBorrowed.query.filter_by(BookBorrowedID=id).first()
    db.session.delete(borrowed)
    db.session.commit()

@app.route("/borrowed/<lmsuserid>",methods=["GET"])
def get_all_borrowed(lmsuserid):
    borrowedbooks = BookBorrowed.query.filter(BookBorrowed.LMSUserID==lmsuserid).all()
    if len(books) > 1:
        result = books_schema.dump(books)
        return jsonify(result.data)
    result = book_schema.dump(books)
    return jsonfy(result.data)

if __name__=='__main__':
    app.run(host="10.132.105.95",port=8000,debug=True)
