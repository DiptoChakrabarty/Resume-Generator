from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed,FileField
from wtforms import StringField, PasswordField,SubmitField,BooleanField,TextAreaField,DateField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from resume.models import user,posts
from flask_login import current_user

class Reg(FlaskForm):
    username =  StringField('Username',
        validators=[DataRequired(),Length(min=5,max=20)])
    email = StringField('Email',
        validators=[DataRequired(),Email()])
    password = PasswordField('Password',
        validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
        validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        users = user.query.filter_by(username=username.data).first()
        if users:
            raise ValidationError('Username used already')

    def validate_email(self,email):
        email = user.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email used already')


class Login(FlaskForm):
    email = StringField('Email',
        validators=[DataRequired(),Email()])
    password = PasswordField('Password',
        validators=[DataRequired()])
    remember =  BooleanField('Remember Me')
    submit = SubmitField('Login')


class account(FlaskForm):
    new_username = StringField("New Username",
        validators=[DataRequired(),Length(min=3,max=20)])
    new_email = StringField("New EmailId",
        validators=[Email(),DataRequired()])
    '''new_password = PasswordField("New Password",
        validators=[DataRequired(),Length(min=7,max=15)])
    confirm_new_password = PasswordField("Confirm New Password",
        validators=[DataRequired(),Length(min=7,max=15)])  '''
    picture = FileField("Update Profile Picture",validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update Account')
    def validate_username(self,new_username):
        if new_username.data != current_user.username:
            username = user.query.filter_by(username=new_username.data)
            if username:
                raise ValidationError("Username Already present")
    def validate_email(self,new_email):
        if new_email != current_user.email:
            emailid = user.query.filter_by(email=new_email.data)
            if emailid:
                return ValidationError("Email Id used already")


class posting(FlaskForm):
    title = StringField("Name",
        validators=[DataRequired(),Length(min=5)])
    content = TextAreaField("Description",
        validators=[DataRequired(),Length(min=15)])
    submit = SubmitField("Create Post")

class resumebuilder(FlaskForm):
    name= StringField("Name",
        validators=[DataRequired(),Length(min=5)])
    email = StringField("Email Id",
        validators=[DataRequired(),Length(min=5)])
    phoneno= StringField("Phone No",
        validators=[DataRequired(),Length(min=5)])
    
    #Education
    college = StringField("College",
        validators=[DataRequired(),Length(min=5)])
    start = DateField('Start Date', format='%m/%d/%Y', 
         validators=[DataRequired()])
    end  = DateField('End Date', format='%m/%d/%Y', 
        validators=[DataRequired()])
    cgpa  = StringField("CGPA",
        validators=[DataRequired()])
    
    #Work Experience
    company = StringField("Company",
        validators=[DataRequired(),Length(min=5)])
    position = StringField("Position",
        validators=[DataRequired(),Length(min=5)])
    startexp = DateField('Start Date', format='%m/%d/%Y', 
         validators=[DataRequired()])
    endexp  = DateField('End Date', format='%m/%d/%Y', 
        validators=[DataRequired()])
    content = TextAreaField("Description",
        validators=[DataRequired(),Length(min=15)])

    
    submit = SubmitField("Create Resume")

     