from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
from flask_login import current_user
from app.errors.authErrors import ( 
    InvalidLoginSessionError,
    InvalidCurrentPasswordError
)
from app.auth.models import User
from app import bcrypt

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
class ChangePasswordForm(FlaskForm):
    current_password = StringField('Current Password')
    new_password = PasswordField('New Password')
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Update')

    def validate_current_password(self, current_password):
        if current_password == "" or current_password is not None:
            if current_user.get_id() is not None:
                user = User.query.filter_by(id=current_user.get_id()).first()
                if not bcrypt.check_password_hash(user.password, current_password.data):
                    raise InvalidCurrentPasswordError()
            else:
                raise InvalidLoginSessionError()