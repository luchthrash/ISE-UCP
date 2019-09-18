from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class ChangePasswordForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Current password', validators=[DataRequired()])
    newPassword = PasswordField('New password', validators=[DataRequired()])
    confirmNewPassword = PasswordField('Confirm new password', validators=[DataRequired()])
    submit = SubmitField('Submit')