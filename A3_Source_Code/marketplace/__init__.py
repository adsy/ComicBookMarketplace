# import flask - from the package import class
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import os

from flask_login import LoginManager

db = SQLAlchemy()

# create a function that creates a web application
# a web server will run this web application

def create_app():

    #Initialise instance of flask app and set secret_key
    app = Flask(__name__)
    app.debug = True
    app.secret_key = 'utroutoru'
    
    
    #Set the app configuration data
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///marketplace.sqlite'
    
    #Initalise db from Heroku
    #app.config.from_mapping(
        # Flask-SQLAlchemy settings
    #    SQLALCHEMY_DATABASE_URI=os.environ['DATABASE_URL'],
    #)

    #Initialise db with app
    db.init_app(app)

    #Initialise bootstrap with app
    bootstrap = Bootstrap(app)

    # initialize the login manager
    login_manager = LoginManager()

    #Create upload folder and config for image uploads
    UPLOAD_FOLDER = '/static/image'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    #Create error handler for page not found
    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    #Create error handler for internal server error
    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html'), 500

    # set the name of the login function that lets user login
    # in our case it is auth.login (blueprintname.viewfunction name)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # create a user loader function takes userid and returns User
    from .models import User  # importing here to avoid circular references
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # importing views module here to avoid circular references
    # a commonly used practice.
    from . import views
    app.register_blueprint(views.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import comics
    app.register_blueprint(comics.bp)

    return app
