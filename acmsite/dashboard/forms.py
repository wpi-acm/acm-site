from flask_wtf import FlaskForm
from wtforms.fields import PasswordField
from wtforms.validators import DataRequired

class PasswordForm(FlaskForm):
    current_password = PasswordField('Current Password')
    new_password = PasswordField('New Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm New Password',
                                     validators=[DataRequired()])
