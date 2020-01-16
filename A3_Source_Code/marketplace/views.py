#import important modules
from flask import ( 
    Blueprint, flash, render_template, request, url_for, redirect
) 
from .models import Comic,Bid,User,Order
from .forms import ComicForm, RegisterForm, LoginForm, InputForm
from . import db


#Create new blueprint called 'main'
bp = Blueprint('main', __name__)

#Create a route to display the idnex page
@bp.route('/', methods=['GET', 'POST'])
def index():

    #Create a new search form
    form = InputForm()

    #Get all comics
    comics = Comic.query.all()

    #Get the number of comics
    length = len(comics)
    
    #If category search form validates on submit
    if form.validate_on_submit():

        #Grab category input to display as title on rendered page
        fInput = form.inputCategory.data

        #Get a list of comics in that category
        comic_list = Comic.query.filter_by(comicCategory=fInput).all()

        #Get the length of that list
        comic_length = len(comic_list)

        #Render search results page with variables
        return render_template('comics/searchResults.html', comics=comic_list, length=comic_length, heading=fInput)

    #Render index page with variables
    return render_template('index.html', comics=comics, length=length, form=form)


