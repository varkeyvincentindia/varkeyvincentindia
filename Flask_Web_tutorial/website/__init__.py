import imp
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'adcddggjwoicna' #For encrypting and 
    #secure the cookies and session data related to our website.
    app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')

    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    """
        So where do we
        need to go if we're not
        logged in? So
        essentially where
        should flask redirect
        us if the user is not
        logged in and there's a
        login required? Well,
        we want to redirect to
        auth.login,
    """
    login_manager.init_app(app) #Telling the login manager which app we are using

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    """ What this is doing is this
        is telling flask how we
        load a user. Now 'User.query.get' this
        works very similar to
        'filter_by', except by
        default, it's going to
        look for the primary
        key. 
        So when you use
        'get', you don't have to
        specify like 'ID=ID'. 
        It just knows that
        it's going to look for
        the primary key and
        check if it's equal to
        whatever we pass, 
    """

    return app
def create_database(app):
    if not path.exists('website/' + DB_NAME): # Whether the database 'database.db' file exists or not
        db.create_all(app=app)
        print('Created Database!')