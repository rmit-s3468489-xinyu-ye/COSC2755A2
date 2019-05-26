from flask import Flask,render_template,flash, request,redirect,url_for,session
from dashboard_config import app, root_url
from wtforms import PasswordField, TextField, Form, TextAreaField, SelectField, SubmitField
from wtforms.validators import regexp, InputRequired, Email, Length, EqualTo
from flask_wtf import FlaskForm
import json
import requests


class BookForm(FlaskForm):
    """
    the form is used for adding a book to the database
    """
    Title = TextField("Title: ",validators=[InputRequired(message="The title field can not be empty!")],
    render_kw={"placeholder":"The title of book"})
    Author = TextField("Author: ",validators=[InputRequired(message="The author field can not be empty!")],
    render_kw={"placeholder":"the author of book"})
    PublishedDate = TextField("PublishedDate: ",validators=[InputRequired(message="The publish date field can not be empty!")],
    render_kw={"placeholder":"the published date of book"})


@app.route("/")
@app.route("/home/")
@app.route('/index/')
def home():
    """ 
    the route of home page 
    """
    return render_template("index.html")

@app.route("/booklist/",methods=["GET","POST"])
def booklist():
    """
    the route of book list page, this page can 
    view all of the book store in the google clooud sql, and 
    also can remove any of it, and add any book to database.
    """
    form = BookForm()
    url = root_url + "/book"
    books = json.loads(requests.get(url).text)
    style_list = ["success","warning","danger","warning","info","warning"]
    i = 0
    for item in books:
        item['hover'] = style_list[i%6]
        i += 1
    if form.validate_on_submit():
        Title = form.Title.data
        Author = form.Author.data
        PublishedDate = form.PublishedDate.data
        send_data = {"Title":Title,"Author":Author,"PublishedDate":PublishedDate}
        requests.post(url,data=json.dumps(send_data),headers={'Content-Type': 'application/json'})
        return redirect(url_for('booklist'))
    if request.method == "POST" and request.form.get('bId'):
        url = url + "/" + request.form.get('bId')
        requests.delete(url)
        return redirect(url_for('booklist'))
    return render_template('book.html',form=form,books=books)

@app.route("/userlist/",methods=["GET","POST"])
def userlist():
    """
    the route of user information, the admin can view all of the user information here
    """
    url = root_url + "/user"
    users = json.loads(requests.get(url).text)
    style_list = ["success","warning","danger","warning","info","warning"]
    i = 0
    for item in users:
        item['hover'] = style_list[i%6]
        i += 1
    return render_template('user.html',users=users)

@app.route("/borrowedlist/",methods=["GET","POST"])
def borrowedlist():
    """
    the route of borrow information
    """
    url = root_url + "/borrowed"
    borrowed = json.loads(requests.get(url).text)
    style_list = ["success","warning","danger","warning","info","warning"]
    num = 1
    for item in borrowed:
        item['itemID'] = num
        item['hover'] = style_list[(num-1)%6]
        url_uname = root_url + "/user/" + str(item["LMSUserID"])
        item['uName'] = json.loads(requests.get(url_uname).text)['UserName']
        url_bookinfo = root_url + "/book/" + str(item['BookID'])
        book = json.loads(requests.get(url_bookinfo).text)
        item['bTitle'] = book['Title']
        item['bAuthor'] = book['Author']
        item['bPublishDate'] = book['PublishedDate']
        num += 1
    if request.method == "POST":
        return render_template("analysis.html")
    return render_template('borrowedbook.html',borrowed = borrowed)

@app.route("/contact/")
def contact():
    """
    group members' information
    """
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1",port=5000,debug=True)
