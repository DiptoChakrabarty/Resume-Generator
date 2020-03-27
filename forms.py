from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed,FileField
from wtforms import StringField, PasswordField,SubmitField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from videos.models import user
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