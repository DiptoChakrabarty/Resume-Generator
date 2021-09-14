from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed,FileField
from wtforms import StringField, PasswordField,SubmitField,BooleanField,TextAreaField
from wtforms.fields.html5  import DateField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError,Regexp
from resume.models import UserModel
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
        users = UserModel.find_by_username(username.data)
        if users:
            raise ValidationError('Username used already')

    def validate_email(self,email):
        email = UserModel.find_by_email(email.data)
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
            username = UserModel.find_by_username(new_username.data)
            if username:
                raise ValidationError("Username Already present")
    def validate_email(self,new_email):
        if new_email != current_user.email:
            emailid = UserModel.find_by_email(new_email.data)
            if emailid:
                return ValidationError("Email Id used already")


class posting(FlaskForm):
    title = StringField("Name",
        validators=[DataRequired(),Length(min=5)])
    content = TextAreaField("Description",
        validators=[DataRequired(),Length(min=15)])
    submit = SubmitField("Create Post")



 #Education
class useredu(FlaskForm):
    college = StringField("College",
        validators=[DataRequired(),Length(min=5)])
    start = DateField('Start Date', format='%Y-%m-%d', 
         validators=[DataRequired()])
    end  = DateField('End Date', format='%Y-%m-%d', 
        validators=[DataRequired()])

    def validate_end(form, field):
    	if field.data < form.start.data:
    		raise ValidationError("End date cannot be earlier than start date.")

    cgpa  = StringField("CGPA",
        validators=[DataRequired()])  
    submit = SubmitField("Add Education")


  #Work Experience
class userexp(FlaskForm):
    company = StringField("Company",
        validators=[DataRequired(),Length(min=5)])
    position = StringField("Position",
        validators=[DataRequired(),Length(min=5)])
    startexp = DateField('Start Date', format='%Y-%m-%d', 
         validators=[DataRequired()])
    endexp  = DateField('End Date', format='%Y-%m-%d', 
        validators=[DataRequired()])

    def validate_endexp(form, field):
    	if field.data < form.startexp.data:
    		raise ValidationError("End date cannot be earlier than start date.")

    content = TextAreaField("Description",
        validators=[DataRequired(),Length(min=15)])
    submit = SubmitField("Add Work Experience")
    
    # Projects
class userpro(FlaskForm):
    projectname = StringField("Project Name",
        validators=[DataRequired(),Length(min=3)])
    startpro = DateField('Start Date', format='%Y-%m-%d', 
         validators=[DataRequired()])
    endpro  = DateField('End Date', format='%Y-%m-%d', 
        validators=[DataRequired()])

    def validate_endpro(form, field):
    	if field.data < form.startpro.data:
    		raise ValidationError("End date cannot be earlier than start date.")
    		
    description = TextAreaField("Description",
        validators=[Length(min=10)])
    url = StringField("Project Url",
        validators=[Length(min=5)])
    submit = SubmitField("Add Projects")


class resumebuilder(FlaskForm):
    name= StringField("Name",
        validators=[DataRequired(),Length(min=5)])
    designation = StringField("Designation",
        validators=[DataRequired(),Length(min=3)])
    email = StringField("Email Id",
        validators=[Email(),DataRequired()])
    phoneno= StringField("Phone No",
        validators=[Regexp('^[0-9]*$'),DataRequired()])
    profile = TextAreaField("Description",
        validators=[Length(min=10)])

    
    submit = SubmitField("Create Resume")


class usersk(FlaskForm):
    skillname = StringField("Skill Name",
        validators=[DataRequired(),Length(min=3)])
    
    submit = SubmitField("Add Another skill")

class achieve(FlaskForm):
    achname = StringField("Acheivement",
        validators=[DataRequired(),Length(min=3)])
    achdesc = TextAreaField("Description",
        validators=[Length(min=10)])

    
    submit = SubmitField("Add")

class requestresetform(FlaskForm):
    email = StringField("Email",
        validators=[DataRequired(),Length(min=5)])
    submit = SubmitField("Reset Password")

    def validate_email(self,email):
        user_email = UserModel.find_by_email(email.data)
        if user_email is None:
            raise ValidationError("The email is unverified please register using this email")

class resetpassword(FlaskForm):
    password = PasswordField('Password',
        validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
        validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Change Password')





     