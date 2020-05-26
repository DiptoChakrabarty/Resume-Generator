from flask import Flask
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import subprocess as sp
from flask_mail import Mail



app =  Flask(__name__)

app.config['SECRET_KEY'] = 'e23739c67eade607c64f90c3ebb479ca' #Prevents XSS
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

app.config["MAIL_SERVER"] = "smtp.google.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = 
app.config["MAIL_PASSWORD"] = 
mail = Mail(app)

db = SQLAlchemy(app)
db.create_all()
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'   #provide login path first

@app.before_first_request
def create_tables():
    db.create_all()




from resume import routes