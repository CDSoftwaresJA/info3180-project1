from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField ,SubmitField
from wtforms.validators import DataRequired, Email

class EmailPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    gender = StringField('Gender', validators=[DataRequired()])
    biography = StringField('Biography', validators=[DataRequired()])
    picture = FileField("Please select an image to upload", validators=[FileRequired()])






































