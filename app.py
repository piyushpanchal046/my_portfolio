from flask import Flask, render_template, request
import json
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from datetime import datetime

with open("name.json") as u:
    name = json.load(u)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]= name["url"]["database"]  # database name left
db=SQLAlchemy(app)

app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME =name["url"]["mail"],
    MAIL_PASSWORD = name["url"]["pass"] #   'Sangeeta@511'
)

mail=Mail(app)
class Contacts(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    username= db.Column(db.String(20),nullable=False)
    email = db.Column(db.String(20), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(20), nullable=True)

class Image(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    uname= db.Column(db.String(20),nullable=False)
    urli= db.Column(db.String(20), nullable=False)


@app.route("/")
def home():
    bg = Image.query.filter_by(uname="bg_home").first()
    logo=  Image.query.filter_by(uname="logo").first()
    return render_template("index.html",name=name,bgimage=bg,logo=logo)


@app.route("/about")
def about():
    bg = Image.query.filter_by(uname="bg_about").first()
    logo = Image.query.filter_by(uname="logo").first()
    return render_template("about.html",name=name,bgimage=bg,logo=logo)


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if(request.method== "POST"):
        tname = request.form.get("uname")
        temail = request.form.get("gmail")
        tmessage = request.form.get("mes")
        entry = Contacts(username=tname, email=temail, message=tmessage, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
        msg = mail.send_message(tname,
                                sender=name["url"]["mail"],
                                recipients=["piyushflask@gmail.com"],

                                body="new message from "+tname+"\n" + "Email ID: "+ temail+ "\n" + "message: \n"+ tmessage
                                 )
        reply = mail.send_message("Reply from Piyush Panchal",
                                sender=name["url"]["mail"],
                                recipients=[temail],
                                body="I received your email "+tname+".\n I will reply as soon as possible\n Thank you for visiting my website."
                                )
    bg = Image.query.filter_by(uname="bg_contact").first()
    logo = Image.query.filter_by(uname="logo").first()
    return render_template("contact.html",name=name,bgimage=bg,logo=logo)


@app.route("/projects")
def projects():
    bg = Image.query.filter_by(uname="bg_projects").first()  #  bg = Image.query.filter_by(uname="bg_projects").first()
    logo = Image.query.filter_by(uname="logo").first()       # variable= table_name.query.filter_by(column_name==to be match and get the row data ="uname_column name").first()
    project1 = Image.query.filter_by(uname="first_project").first()
    project2 = Image.query.filter_by(uname="2nd_Project").first()  # html_variable = python_variable
    project3 = Image.query.filter_by(uname="soon").first()   # html_variable = python_variable
    return render_template("projects.html", name=name,bgimage=bg,logo=logo,project1=project1,project2=project2,project3=project3)


#if __name__ == "__main__":
#    app.run()
