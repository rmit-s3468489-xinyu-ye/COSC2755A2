from flask import Flask, request, jsonify
from dashboard_config import app,db,ma,get_host_ip
from datetime import datetime, timedelta
from sqlalchemy import and_
import json


db.metadata.clear()
class LMSUser(db.Model):
    LMSUserID = db.Column(db.Integer, primary_key = True)
    UserName = db.Column(db.String(100),nullable = False, unique = True)
    FirstName = db.Column(db.String(100),nullable = False)
    LastName = db.Column(db.String(100),nullable = False)
    Email = db.Column(db.String(100),nullable = False)
    Book = db.relationship('BookBorrowed', backref='user')
    def __init__(self,UserName,FirstName,LastName,Email):
        self.UserName = UserName
        self.FirstName = FirstName
        self.LastName = LastName
        self.Email = Email


class Book(db.Model):
    BookID = db.Column(db.Integer, primary_key = True)
    Title = db.Column(db.String(100),nullable = False)
    Author = db.Column(db.String(100),nullable = False)
    PublishedDate = db.Column(db.String(100),nullable = False)
    BarcodeData = db.Column(db.String(100))
    Borrowed = db.relationship('BookBorrowed', backref='bbook')
    def __init__(self,Title,Author,PublishedDate,BarcodeData=""):
        self.Title = Title
        self.Author = Author
        self.PublishedDate = PublishedDate
        self.BarcodeData = BarcodeData


class BookBorrowed(db.Model):
    BookBorrowedID = db.Column(db.Integer, primary_key = True)
    LMSUserID = db.Column(db.Integer,db.ForeignKey('lms_user.LMSUserID'),nullable=False)
    BookID = db.Column(db.Integer,db.ForeignKey('book.BookID'),nullable=False)
    BorrowedDate = db.Column(db.DateTime,default = datetime.now())
    ReturnedDate = db.Column(db.DateTime,default = datetime.now() + timedelta(days=7))
    def __init__(self,LMSUserID,BookID,BorrowedDate,ReturnedDate):
        self.LMSUserID = LMSUserID
        self.BookID = BookID
        self.BorrowedDate = BorrowedDate
        self.ReturnedDate = ReturnedDate

class LmsUserSchema(ma.Schema):
    class Meta:
        fields = ('LMSUserID','UserName','FirstName','LastName','Email')

lmsuser_schema = LmsUserSchema()
lmsusers_schema = LmsUserSchema(many=True)

class BookSchema(ma.Schema):
    class Meta:
        fields = ('BookID','Title','Author','PublishedDate','BarcodeData')

book_schema = BookSchema()
books_schema = BookSchema(many=True)

class BookBorrowedSchema(ma.Schema):
    class Meta:
        fields = ('BookBorrowedID','LMSUserID','BookID','BorrowedDate','ReturnedDate')

bookborrowed_schema = BookBorrowedSchema()
booksborrowed_schema = BookBorrowedSchema(many=True)


@app.route('/user',methods=["POST"])
def add_user():
    data = request.get_json()
    new_user = LMSUser(data["UserName"],data["FirstName"],data["LastName"],data["Email"])
    db.session.add(new_user)
    db.session.commit()
    return lmsuser_schema.jsonify(new_user)

@app.route('/user',methods=["GET"])
def get_users():
    all_users = LMSUser.query.all()
    result = lmsusers_schema.dump(all_users)
    return jsonify(result.data)

@app.route('/user/<uid>',methods=["GET"])
def get_one_user(uid):
    usrname = LMSUser.query.filter_by(LMSUserID=uid).first()
    result = lmsuser_schema.dump(usrname)
    return jsonify(result.data)

@app.route('/user/n/<uname>',methods=["GET"])
def get_one_user_by_name(uname):
    usrname = LMSUser.query.filter_by(UserName=uname).first()
    result = lmsuser_schema.dump(usrname)
    return jsonify(result.data)

@app.route('/book',methods=["POST"])
def add_book():
    data = request.get_json()
    new_book = Book(data["Title"],data["Author"],data["PublishedDate"])
    db.session.add(new_book)
    db.session.commit()
    return book_schema.jsonify(new_book)

@app.route('/book/i',methods=["POST"])
def get_book_id():
    data = request.get_json()
    book = Book.query.filter(and_(Book.Title==data["Title"],Book.Author==data["Author"],Book.PublishedDate==data["PublishedDate"])).first()
    result = book_schema.dump(book)
    return jsonify(result.data)

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

@app.route("/book/<BookID>",methods=["GET"])
def get_one_book(BookID):
    book = Book.query.filter_by(BookID=BookID).first()
    result = book_schema.dump(book)
    return jsonify(result.data)

@app.route("/book/b/",methods=["PUT"])
def modify_barcode():
    data = request.get_json()
    book = Book.query.filter(and_(Book.Title == data['Title'],
    Book.Author == data['Author'],Book.PublishedDate == data['PublishedDate'])).first()
    book.BarcodeData = data["BarcodeData"]
    db.session.commit()
    return book_schema.jsonify(book)

@app.route("/book/b/<barcode>",methods=["GET"])
def get_by_barcode(barcode):
    data = json.loads(barcode)
    book = Book.query.filter(Book.BarcodeData==data['barcode'])
    print(book)
    result = book_schema.dump(book)
    print(result.data)
    return jsonify(result.data)

@app.route("/book/t/<title>",methods=["GET"])
def get_title(title):
    books = Book.query.filter(Book.Title==title).all()
    result = books_schema.dump(books)
    return jsonify(result.data)


@app.route("/book/a/<author>",methods=["GET"])

def get_author(author):
    books = Book.query.filter(Book.Author==author).all()
    result = books_schema.dump(books)
    return jsonify(result.data)

    
@app.route("/book/p/<publisheddate>",methods=["GET"])

def get_publisheddate(publisheddate):
    books = Book.query.filter(Book.PublishedDate==publisheddate).all()
    result = books_schema.dump(books)
    return jsonify(result.data)


@app.route("/borrowed",methods=["POST"])
def add_borrowedbook():
    data = request.get_json()
    new_borrowed = BookBorrowed(data["LMSUserID"], data["BookID"], 
    datetime.now(), datetime.now() + timedelta(days=7))
    db.session.add(new_borrowed)
    db.session.commit()
    return bookborrowed_schema.jsonify(new_borrowed)


@app.route("/borrowed",methods=["GET"])    
def get_all():
    borrowbooks = BookBorrowed.query.all()
    result = booksborrowed_schema.dump(borrowbooks)
    return  jsonify(result.data)

@app.route("/return/<data>",methods=["DELETE"])    
def return_by_barcode(data):
    data = json.loads(data)
    book = BookBorrowed.query.filter(and_(BookBorrowed.BookID==data['BookID'],BookBorrowed.LMSUserID==data['LMSUserID'])).first()
    db.session.delete(book)
    db.session.commit()

@app.route("/borrowed/<id>",methods=["DELETE"])
def rm_borrowedbook(id):
    borrowed = BookBorrowed.query.filter_by(BookBorrowedID=id).first()
    db.session.delete(borrowed)
    db.session.commit()

@app.route("/borrowed/u/<lmsuserid>",methods=["GET"])
def get_all_borrowed_from_user(lmsuserid):
    borrowedbooks = BookBorrowed.query.filter(BookBorrowed.LMSUserID==lmsuserid).all()
    result = booksborrowed_schema.dump(borrowedbooks)
    return jsonify(result.data)

@app.route("/borrowed/b/<BookID>",methods=["GET"])
def get_all_borrowed_from_book(BookID):
    borrowedbooks = BookBorrowed.query.filter(BookBorrowed.BookID==BookID).all()
    result = booksborrowed_schema.dump(borrowedbooks)
    return jsonify(result.data)

if __name__=='__main__':
    host = get_host_ip()
    app.run(host=host,port=8000,debug=True)
