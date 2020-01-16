#import improtant modules
from flask import (
    Blueprint, flash, render_template, request, url_for, redirect
)
from .models import Comic, User, Bid, Order
from .forms import ComicForm, BidForm, InputForm
from . import db
from flask_login import login_user, login_required, logout_user
from werkzeug.utils import secure_filename
from datetime import datetime
import os


# allows user ID retrievel
from flask import session

# create a blueprint for comics once logged in
bp = Blueprint('comic', __name__, url_prefix='/comics')

#Function to check the uploaded file.
def check_upload_file(form):
    # get file data from form
    fp = form.comicImage.data
    filename = fp.filename
    # get the current path of the module file… store file relative to this path
    BASE_PATH = os.path.dirname(__file__)
    # upload file location – directory of this file/static/image
    upload_path = os.path.join(
        BASE_PATH, 'static/image', secure_filename(filename))
    # store relative path in DB as image location in HTML is relative
    db_upload_path = '/static/image/' + secure_filename(filename)
    # save the file and return the db upload path
    fp.save(upload_path)
    return db_upload_path

#Function to create a Comic
@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():

    #Grab id of user logged in.
    userID = session['id']
    
    #Grab the user account to be used later
    user = User.query.filter_by(id=userID).first()
    
    #Create a new form to create a comic
    form = ComicForm()

    #If form is validated on submission
    if form.validate_on_submit():
        print('Successfully created new comic', 'success')

        # get comic name, author name, ISBN and description from the form
        cname = form.comicName.data
        cauthor = form.authorName.data
        cisbn = form.comicISBN.data
        ccategory = form.comicCategory.data
        cdescription = form.comicDescription.data
        cprice = form.comicPrice.data

        #Create a variable to keep track of file path of stored image
        db_file_path = check_upload_file(form)

        #Create a new comic model object with variables created
        new_comic = Comic(comicTitle=cname, comicAuthor=cauthor, comicISBN=cisbn, comicCategory=ccategory,
                          comicDescription=cdescription, comicImage=db_file_path, comicPrice=cprice, sellerName=user.name, seller_id=userID)
        
        #Add the new comic
        db.session.add(new_comic)
        
        #Commit changes to DB
        db.session.commit()

        #Get all the comics created by user
        user_comics = Comic.query.filter_by(seller_id=userID).all()

        #Get the amount of comics
        user_comics_length = len(user_comics)
        
        #Return dashboard for comics
        return redirect(url_for('comic.manage', comics=user_comics, length=user_comics_length))

    #Return page with variables
    return render_template('comics/create.html', form=form, heading="Create Comic")

#Function to search for a comic
@bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():

    #Create a new search form
    form = InputForm()

    #If form is validated on submission
    if form.validate_on_submit():
        
        #Grab category data to use later
        fInput = form.inputCategory.data

        #Generate list of comics by that category
        comic_list = Comic.query.filter_by(comicCategory=fInput).all()

        #Get amount of comics
        comic_length = len(comic_list)

        #Render page with variables
        return render_template('comics/searchResults.html', comics=comic_list, length=comic_length, heading=fInput)

    #Render page with variables
    return render_template('comics/search.html', form=form)


# create a page that displays the users listed comics
@bp.route('/manage')
@login_required
def manage():

    #Grab id of user logged in
    userID = session['id']

    #Get all the comics created by user
    user_comics = Comic.query.filter_by(seller_id=userID).all()

    #Get the amount of comics
    user_comics_length = len(user_comics)

    #Render page with variables
    return render_template('comics/manage.html', comics=user_comics, length=user_comics_length)

# create a page that displays and allows editing to one of the users listed comics
@bp.route('/manage_item/<id>', methods=['GET', 'POST'])
@login_required
def manage_item(id):

    #Grab id of user logged in
    userID = session['id']

    #Get user details by userID
    user = User.query.filter_by(id=userID).first()

    #Get all bids on comic
    bids = Bid.query.filter_by(comicID=id).all()

    #Get comic details by id
    comic = Comic.query.filter_by(id=id).first()

    #Get the amount of bids
    length = len(bids)

    #Render page with variables
    return render_template('comics/manage_item.html', bids=bids, comic=comic, length=length)

#Create a page that shows previous transactions
@bp.route('/transactions')
@login_required
def past_sales():

    #Grab id of user logged in
    userID = session['id']

    #Grab all past transactions from user
    orders = Order.query.filter_by(user_id=userID).all()

    #Get the amount of orders
    length = len(orders)

    #Render page with variables
    return render_template('comics/transactions.html', orders=orders, length=length)

# create a page that displays and allows editing to one of the users listed comics
@bp.route('/out_of_stock/<id>', methods=['GET', 'POST'])
@login_required
def out_of_stock(id):

    #Get the comic details
    comic = Comic.query.filter_by(id=id).first()

    #Set comic live to False
    comic.live = False

    #Commit changes to DB
    db.session.commit()

    #Grab id of user logged in
    userID = session['id']

    #Get all comics created by user
    user_comics = Comic.query.filter_by(seller_id=userID).all()

    #Get the amount of comics
    user_comics_length = len(user_comics)
    
    #Render page with variables
    return render_template('comics/manage.html', comics=user_comics, length=user_comics_length)

# create a page that displays and allows editing to one of the users listed comics
@bp.route('/in_stock/<id>', methods=['GET', 'POST'])
@login_required
def in_stock(id):

    #Get the comic details
    comic = Comic.query.filter_by(id=id).first()

    #Set comic live to True
    comic.live = True

    #Commit changes to DB
    db.session.commit()

    #Grab id of user logged in
    userID = session['id']

    #Get all comics created by user
    user_comics = Comic.query.filter_by(seller_id=userID).all()

    #Get the amount of comics
    user_comics_length = len(user_comics)
    
    #Render page with variables
    return render_template('comics/manage.html', comics=user_comics, length=user_comics_length)

#Create a function that accepts the bid with amount specified
@bp.route('/accept_bid/<id>?amt=<amt>', methods=['GET', 'POST'])
@login_required
def accept_bid(id, amt):
    
    #Grab id of user logged in
    userID = session['id']

    #Get the details of the bid that was accepted
    bid = Bid.query.filter_by(id=id).first()

    #Get the details of the comic of which the bid was accepted
    comic = Comic.query.filter_by(id=bid.comicID).first()

    #Create a new order/transaction with the details that were grabbed.
    new_order = Order(buyerName=bid.buyerName, buyerEmail=bid.buyerEmail, purchaseTime=datetime.now(), comicTitle=comic.comicTitle,
                      comicAuthor=comic.comicAuthor, comicISBN=comic.comicISBN, comicPrice=amt, comicImage=comic.comicImage, comicID=comic.id, user_id=userID)

    #Add that new order to the DB
    db.session.add(new_order)

    #Remove that bid from the DB so it no longer appears
    Bid.query.filter_by(id=id).delete()

    #Commit changes to DB
    db.session.commit()

    #Get all comics created by user
    user_comics = Comic.query.filter_by(seller_id=userID).all()

    #Get the amount of comics
    user_comics_length = len(user_comics)

    #Render page with variables
    return redirect(url_for('comic.manage', comics=user_comics, length=user_comics_length))



# create a page that will show the details for the comic
@bp.route('show/<id>', methods=['GET', 'POST'])
@login_required
def show(id):

    #Generate new bid form
    form = BidForm()

    #Grab id of user logged in
    userID = session['id']
    
    #Get all comics created by user
    user_comics = Comic.query.filter_by(seller_id=userID).all()
    
    #Get the details of the comic
    comic = Comic.query.filter_by(id=id).first()

    #Get the details of the user logged in
    user = User.query.filter_by(id=userID).first()

    #If the comic clicked on is in the comics created by users, redirect to manage item page
    for x in user_comics:
        if comic == x:
            return redirect(url_for('comic.manage_item', id=id))

    #If the bid form is submitted succesfully.
    if form.validate_on_submit():
        
        #Grab the form details    
        bEmail = form.buyerEmail.data
        bPh = form.buyerPh.data
        bAmt = form.bidAmt.data

        # create a new bid model object
        new_bid = Bid(buyerName=user.name, buyerEmail=bEmail, buyerPhNo=bPh, bidDateTime=datetime.now(),
                      bidAmount=bAmt, comicID=id)
        
        #Store the new bid details to DB
        db.session.add(new_bid)
        
        #Commit changes to the DB
        db.session.commit()

        #Create a new search form
        form = InputForm()
        
        #Get all comics
        comics = Comic.query.all()

        #Get the number of comics
        length = len(comics)
        
        #Return dashboard for comics
        return redirect(url_for('main.index', comics=comics, length=length, form=form))

    #Render page with varaiables
    return render_template('comics/view_details.html', comic=comic, user=user, form=form)
