from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField, SelectField, EmailField, FileField
from wtforms.validators import DataRequired, EqualTo, Length

# ### User Access Forms ###
class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class UserSignupForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=50)])
    email = EmailField("Email", validators=[DataRequired(), Length(max=50)])
    password_hash = PasswordField("Password", validators=[DataRequired(), EqualTo('password_hash2'), Length(min=6)])
    password_hash2 = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Sign up")

class UserEditForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=50)])
    email = EmailField("Email", validators=[DataRequired(), Length(max=50)])
    active = SelectField("Active", choices=[('y', 'Yes'), ('n', 'No')])
    admin = SelectField("Admin", choices=[('y', 'Yes'), ('n', 'No')])
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match!'), Length(min=6, message="password to short")])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField("Save")

class PasswordResetForm(FlaskForm):
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match!'), Length(min=6, message="password to short")])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField("Save")

class UserSignupForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=50)])
    email = EmailField("Email", validators=[DataRequired(), Length(max=50)])
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match!'), Length(min=6, message="password to short")])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField("Sign Up")

class SetupForm(FlaskForm):
    name = StringField("Your Name", validators=[DataRequired(), Length(max=50)])
    email = EmailField("Your Email Address", validators=[DataRequired(), Length(max=50)])
    password_hash = PasswordField('Your Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match!'), Length(min=6, message="password to short")])
    password_hash2 = PasswordField('Confirm Your Password', validators=[DataRequired()])
    sitename = StringField("New Site Name", validators=[DataRequired(), Length(max=20)])
    signup = SelectField("Allow New Signups", choices=[("y", "Yes"), ("n", "No")])
    submit = SubmitField("Setup")

# ### Pictures Forms ###
class PictureUploadForm(FlaskForm):
    desc = StringField("Description", validators=[DataRequired(), Length(max=80)])
    picture = FileField("Select Picture", validators=[DataRequired()])
    submit = SubmitField("Upload")

class PictureUpdateForm(FlaskForm):
    desc = StringField("Rename Description", validators=[DataRequired(), Length(max=30)])
    submit = SubmitField("Update")