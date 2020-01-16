from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, SelectField, FileField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange
from flask_wtf.file import FileField, FileAllowed, FileRequired

#Allowed file types for comic images   
ALLOWED_FILE = {'jpg', 'JPG'}

#Login form
class LoginForm(FlaskForm):
    username = StringField("User Name", validators=[
                           InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[
                             InputRequired('Enter user password')])
    submit = SubmitField("Login")

#Registration form
class RegisterForm(FlaskForm):
    username = StringField("User Name", validators=[InputRequired()])
    email = EmailField("Email Address", validators=[
                        Email("Please enter a valid email")])

    # linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[InputRequired(),
                                                     EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    # submit button
    submit = SubmitField("Register")

#Comic form
class ComicForm(FlaskForm):
    comicName = StringField('Comic Name', validators=[
                            InputRequired('Enter comic name')])
    authorName = StringField("Author's Name", validators=[
                             InputRequired("Enter Author's name")])
    comicISBN = StringField("ISBN", validators=[InputRequired("Enter ISBN")])
    comicCategory = SelectField("Category", choices=[(
        'action', 'Action'), ('horror', 'Horror'), ('fantasy', 'Fantasy'), ('comedy', 'Comedy')])
    comicDescription = TextAreaField('Description',
                                     validators=[InputRequired(), Length(min=10, max=200)])

    comicPrice = IntegerField('Price',
                                     validators=[InputRequired("Please enter a price"), NumberRange(min=1, max=1000, message="Please enter a number between $1 and $1000")])
    comicImage=FileField('Destination Image',
                           validators=[FileRequired(message='Image can not be empty'),
                                       FileAllowed(ALLOWED_FILE, message='Only support jpg, JPG')])
    submit=SubmitField("Create")

#Bid form
class BidForm(FlaskForm):
    buyerEmail=EmailField("Email Address", validators=[
                        Email("Please enter a valid email")])
    buyerPh=IntegerField("Mobile", validators=[InputRequired()])
    bidAmt=IntegerField("Bid", validators=[
                            InputRequired('Please enter your bid.'), NumberRange(min=1, max=1000, message="Please enter a bid between $1 and $1000")])
    submit=SubmitField("Create Bid")

#Category search form
class InputForm(FlaskForm):
    inputCategory=SelectField("", choices=[(
        'action', 'Action'), ('horror', 'Horror'), ('fantasy', 'Fantasy'), ('comedy', 'Comedy')])
    submit=SubmitField("Search")
