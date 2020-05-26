from resume import db,login_manager,app
from flask_login import UserMixin
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as serializer


@login_manager.user_loader
def load_user(id):
    return user.query.get(int(id))


class user(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    image_file = db.Column(db.String(20),nullable=False,default='default.jpg')
    password =  db.Column(db.String(60),nullable=False)
    #education
    education = db.relationship('education',backref='edu',lazy=True)
    #experience
    experience = db.relationship('experience',backref='exp',lazy=True)
    #projects
    projects = db.relationship('projects',backref='pro',lazy=True)
    #userdetails
    userdetails = db.relationship('userdetails',backref='details',lazy=True)
    #skills
    skills = db.relationship('skills',backref='skill',lazy=True)
    #achievements
    achievements = db.relationship('achievements',backref='ach',lazy=True)

    def __retr__(self):
        return  "User {}  Email {}  Image {}".format(self.username,self.email,self.image_file)
    
    def reset_token(self,expires_sec=1800):
        s = serializer(app.config['SECRET_KEY'],expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")



class userdetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20),nullable=False)
    email = db.Column(db.String(120),nullable=False)
    designation = db.Column(db.String(120),nullable=False)
    phoneno =  db.Column(db.String(15),nullable=False)
    profile = db.Column(db.Text,nullable=False)
    user_id= db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)






class education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    start = db.Column(db.DateTime,nullable=False,default=datetime.today())
    end = db.Column(db.DateTime,nullable=False,default=datetime.today())
    cgpa = db.Column(db.Integer,nullable=False)
    user_id= db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __retr__(self):
        return  "name {}  cgpa {}  user_id {}".format(self.name,self.cgpa,self.user_id)





class experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100),nullable=False)
    position = db.Column(db.String(100),nullable=False)
    startexp = db.Column(db.DateTime,nullable=False,default=datetime.today())
    endexp = db.Column(db.DateTime,nullable=False,default=datetime.today())
    content = db.Column(db.Text,nullable=False)
    user_id= db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __retr__(self):
        return  "company {}  position {}  user_id {}".format(self.company,self.position,self.user_id)



class projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projectname = db.Column(db.String(100),nullable=False)
    startpro = db.Column(db.DateTime,nullable=False,default=datetime.today())
    endpro = db.Column(db.DateTime,nullable=False,default=datetime.today())
    description = db.Column(db.Text,default=None)
    url = db.Column(db.String(100),default=None)
    user_id= db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __retr__(self):
        return  "projectname {}    user_id {}".format(self.projectname,self.user_id)

class skills(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skillname = db.Column(db.String(100),nullable=False)
    user_id= db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

class achievements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    achname = db.Column(db.String(100),nullable=False)
    achdesc = db.Column(db.Text(100),nullable=False)
    user_id= db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)















def init_db():
    db.create_all()


if __name__ == '__main__':
    init_db()
