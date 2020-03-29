from resume import db,login_manager
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
    posts= db.relationship('posts',backref='author',lazy=True)
    education = db.relationship('education',backref='edu',lazy=True)
    experience = db.relationship('experience',backref='exp',lazy=True)
    projects = db.relationship('projects',backref='pro',lazy=True)

    def __retr__(self):
        return  "User {}  Email {}  Image {}".format(self.username,self.email,self.image_file)
    



#class userdetails(db.Model):
  #  id = db.Column(db.Integer, primary_key=True)


class posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow())
    content = db.Column(db.Text,nullable=False)
    user_id= db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __retr__(self):
        return  "Title {}  Date {}  ".format(self.title,self.date)

class education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    start = db.Column(db.DateTime,nullable=False,default=datetime.utcnow())
    end = db.Column(db.DateTime,nullable=False,default=datetime.utcnow())
    cgpa = db.Column(db.Integer,nullable=False)
    user_id= db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __retr__(self):
        return  "name {}  cgpa {}  user_id {}".format(self.name,self.cgpa,self.user_id)





class experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100),nullable=False)
    position = db.Column(db.String(100),nullable=False)
    startexp = db.Column(db.DateTime,nullable=False,default=datetime.utcnow())
    endexp = db.Column(db.DateTime,nullable=False,default=datetime.utcnow())
    content = db.Column(db.Text,nullable=False)
    user_id= db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __retr__(self):
        return  "company {}  position {}  user_id {}".format(self.company,self.position,self.user_id)



class projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projectname = db.Column(db.String(100),nullable=False)
    startpro = db.Column(db.DateTime,nullable=False,default=datetime.utcnow())
    endpro = db.Column(db.DateTime,nullable=False,default=datetime.utcnow())
    description = db.Column(db.Text,default=None)
    url = db.Column(db.String(100),default=None)
    user_id= db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __retr__(self):
        return  "projectname {}    user_id {}".format(self.projectname,self.user_id)










def init_db():
    db.create_all()


if __name__ == '__main__':
    init_db()
