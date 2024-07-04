from flask import Flask
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# class Author(db.Model):
#     __tablename__ = 'authors'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255), nullable=False)
#     age = db.Column(db.Integer, nullable=False)
#     avg_rating = db.Column(db.Real, nullable=False)
#     books = db.relationship("Book")

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    cover = db.Column
    isbn = db.Column(db.String(255), nullable=False)
    author_name = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    user_rating = db.Column(db.Real, nullable=False)
    shelf = db.Column(db.String(255), nullable=False)
    amnt_pages = db.Column(db.Integer, nullable=False, default=0)
    date_added = db.Column(db.DateTime, default=datetime.datetime.now())
    finished_date = db.Column(db.DateTime)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    favourite_genre = db.Column(db.String(255), nullable=False)
    books = db.relationship("Book")

class Shelf_Type(db.Model):
    __tablename__ = 'shelf_types'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(255), nullable=False)
    books = db.relationship("Book")