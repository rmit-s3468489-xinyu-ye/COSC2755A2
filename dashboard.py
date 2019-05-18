from flask import Flask,render_template,flash, request,redirect,url_for
from dashboard_config import app, root_url
from wtforms import PasswordField, TextField, Form, TextAreaField, SelectField, SubmitField
from wtforms.validators import regexp, InputRequired, Email, Length, EqualTo
from flask_wtf import FlaskForm
import json
import requests

class BookForm(FlaskForm):
    Title = TextField("Title: ",validators=[InputRequired(message="The title field can not be empty!")],
    render_kw={"placeholder":"The title of book"})
    Author = TextField("Author: ",validators=[InputRequired(message="The author field can not be empty!")],
    render_kw={"placeholder":"the author of book"})
    PublishedDate = TextField("PublishedDate: ",validators=[InputRequired(message="The publish date field can not be empty!")],
    render_kw={"placeholder":"the published date of book"})


@app.route("/")
@app.route("/home")
@app.route('/index')
def home():
    """ 
    the route of home page 
    """
    return render_template("index.html")

@app.route("/booklist/",methods=["GET","POST"])
@app.route("/booklist",methods=["GET","POST"])
def booklist():
    form = BookForm()
    books = []
    if form.validate_on_submit():
        Title = form.Title.data
        Author = form.Author.data
        PublishedDate = form.PublishedDate.data
        send_data = {"Title":Title,"Author":Author,"PublishedDate":PublishedDate}
        url = root_url + "/book"
        books = json.loads(requests.get(url).text)
        requests.post(url,data=json.dumps(send_data),headers={'Content-Type': 'application/json'})
        return redirect(url_for('booklist'))
    return render_template('book.html',form=form,books=books)



if __name__ == "__main__":
    app.run(host="127.0.0.1",port=5000,debug=True)
