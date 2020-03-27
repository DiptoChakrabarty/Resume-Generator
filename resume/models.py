from videos import db,login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(id):
    return user.query.get(int(id))


class user(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    image_file = db.Column(db.String(20),nullable=False,default='default.jpg')
    password =  db.Column(db.String(60),nullable=False)
    posts= db.relationship('posts',backref='author',lazy=True)# One to Many Relation

    def __retr__(self):
        return  "User {}  Email {}  Image {}".format(self.username,self.email,self.image_file)
