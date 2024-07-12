from flask import Flask
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    user_rating = db.Column(db.Float, nullable=False, default=0)
    shelf_id = db.Column(db.Integer, db.ForeignKey('shelf_types.id'), nullable=False)
    amnt_pages = db.Column(db.Integer, nullable=False, default=0)
    date_added = db.Column(db.DateTime, default=datetime.datetime.now())
    finished_date = db.Column(db.DateTime, default=None)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    favourite_genre = db.Column(db.String(255), nullable=False)
    books = db.relationship("Book", backref="user", lazy=True)

class Shelf_Type(db.Model):
    __tablename__ = 'shelf_types'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(255), nullable=False)
    books = db.relationship("Book", backref="shelf_type", lazy=True)

class Book_Image(db.Model):
    __tablename__ = 'book_images'
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(255), nullable=False)
    cover_url = db.Column(db.String(255), nullable=False)