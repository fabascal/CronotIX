from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = StringField('Email',
                         id='email_login',
                         validators=[DataRequired()])
    password = PasswordField('Password',
                             id='pwd_login',
                             validators=[DataRequired()])
    submit = SubmitField('Acceder')
    
class ForgotPasswordForm(FlaskForm):
    email = StringField('Email',
                         id='email_forgot',
                         validators=[DataRequired()])
    submit = SubmitField('Recuperar')