from . import db
from datetime import datetime
from flask_login import UserMixin

#Class to create a User object.
class User(db.Model,UserMixin):
    __tablename__='users' # table name
    id = db.Column(db.Integer, primary_key=True) # auto generated
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def __repr__(self): #string print method
        return "<Name: {}, ID: {}>".format(self.name, self.id)

    comics = db.relationship('Comic', backref='user')
    orders = db.relationship('Order', backref='user')

#Class to create a User object.
class Comic(db.Model):
    __tablename__='comics' # table name
    id = db.Column(db.Integer, primary_key=True) # auto generated
    comicTitle = db.Column(db.String(100), index=True, nullable=False)
    comicAuthor = db.Column(db.String(100), index=True, nullable=False)
    comicISBN = db.Column(db.Integer, index=True, nullable=False)
    comicCategory = db.Column(db.String(100), index=True, nullable=False)
    comicDescription = db.Column(db.String(300), index=True, nullable=False)
    comicImage = db.Column(db.String(100), index=True, nullable=False)
    comicPrice = db.Column(db.Integer, nullable=False)
    sellerName = db.Column(db.String(100), index=True, nullable=False)
    live = db.Column(db.Boolean, default=True, nullable=False)

    # define the foreign key - refers to <tablename.primarykey>
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self): #string print method
        return "<Name: {}, ID: {}>".format(self.comicTitle, self.id)

    bids = db.relationship('Bid', backref='comic')

#Class to create a User object.
class Bid(db.Model):
    __tablename__='bids' # table name
    id = db.Column(db.Integer, primary_key=True) # auto generated
    buyerName = db.Column(db.String(100), index=True, nullable=False)
    buyerEmail = db.Column(db.String(100), index=True, nullable=False)
    buyerPhNo = db.Column(db.Integer, index=True, nullable=False)
    bidDateTime = db.Column(db.DateTime, nullable=False, default=datetime.now())
    bidAmount = db.Column(db.Integer, nullable=False)

    # define the foreign key - refers to <tablename.primarykey>
    comicID = db.Column(db.Integer, db.ForeignKey('comics.id'))

#Class to create a User object.
class Order(db.Model):
    __tablename__='orders' # table name
    id = db.Column(db.Integer, primary_key=True) # auto generated
    buyerName = db.Column(db.String(100), index=True, nullable=False)
    buyerEmail = db.Column(db.String(100), index=True, nullable=False)
    purchaseTime = db.Column(db.DateTime, nullable=False, default=datetime.now())
    comicTitle = db.Column(db.String(100), index=True, nullable=False)
    comicAuthor = db.Column(db.String(100), index=True, nullable=False)
    comicISBN = db.Column(db.Integer, index=True, nullable=False)
    comicPrice = db.Column(db.Integer, nullable=False)
    comicImage = db.Column(db.String(100), index=True, nullable=False)
    comicID = db.Column(db.Integer, index=True, nullable=False)

    # define the foreign key - refers to <tablename.primarykey>
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
