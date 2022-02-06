from . import db # from the current package (website) import the object
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # One to many relationship one person can have multiple notes
    # Each notes should be uniquely mapped to 1 person so foreignkey
    # here we are using the data member of 'User'
    # so user.id (in sql object is represented with lowercase)

class User(db.Model, UserMixin): # inheriting UserMixin and db.model
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    # this is how we define a schema 
    # the 'User' object has to conform to this schema
    notes = db.relationship('Note') 
    """
        All users should be able to find all of
        their notes

        it will
        pretty much tell flask
        and tell SQL alchemy
        and do your magic. And
        every time we create a
        note add into this
        user's notes
        relationship, uh, that
        note ID. 

        When you do the
        foreign key, you have
        lowercase. And when you
        do the relationship,
        you're referencing the
        name of the class,
        which is obviously
        capital.
    """
