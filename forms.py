from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField, FileField, TextAreaField, FloatField
from wtforms.validators import Length, EqualTo, DataRequired
from flask_wtf.file import FileRequired, FileAllowed

class AddProduct(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    file = FileField('File', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    price = FloatField('Price', validators=[DataRequired()])
    ingredients = TextAreaField('Ingredients', validators=[DataRequired()])
    submit = SubmitField('Add Product')

    def __str__(self):
        return f"{self.name}"
    
class RegisterForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField(label="Password", validators=[DataRequired(), Length(min=4, max=80)])
    confirm_password = PasswordField(label="Confirm Password", validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    register = SubmitField(label="Register")

class LoginForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    login = SubmitField(label="Login")
    