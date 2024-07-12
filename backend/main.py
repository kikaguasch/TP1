from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, User, Book, Shelf_Type
from datetime import datetime, timedelta
from sqlalchemy.orm import scoped_session, sessionmaker 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
port = 5000
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql+psycopg2://federica:2308@localhost:5432/books'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

@app.route("/")
def home():
    return """
    <html>
    <body>
    <h1>Welcome to our library API</h1>
    <a href="/books">Go to all libraries</a>
    </body>
    </html>  
    """
#get users
@app.route("/users/", methods=['GET'])
def users():
    try:
        users = User.query.all()
        bibliotecas_data = []
        for user in users:
            user_data = {
                'id': user.id,
                'name': user.name,
                'age': user.age,
                'favourite_genre': user.favourite_genre
            }
            bibliotecas_data.append(user_data)
        return jsonify(bibliotecas_data)
    except:
        return jsonify({'message': 'No hay lectores'}), 404

#create users    
@app.route("/users/", methods=['POST'])
def new_user():
    try:
        user = User()
        data = request.json
        user.name = data.get('name')
        user.age = data.get('age')
        user.favourite_genre = data.get('favourite_genre')
        new_shelf = User(name=user.name, age=user.age, favourite_genre=user.favourite_genre)
        db.session.add(new_shelf)
        db.session.commit()

        return jsonify({'message': 'Usuario creado correctamente'}), 201 #creado
    except Exception as error:
        return jsonify({'message': 'No se puedo crear el usuario'}), 400

#get user by id
@app.route("/users/<user_id>", methods=['GET'])
def user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User could not be found'}), 404
        user_data = {
            'id': user.id,
            'name': user.name,
            'age': user.age,
            'favourite_genre': user.favourite_genre
        }
        return jsonify(user_data)
    except:
        return jsonify({'message': 'El usuario no existe'}), 404

#get shelves from each user by id
@app.route("/users/<user_id>/shelves", methods=['GET'])
def user_libraries(user_id):
    try:
        shelves = db.session.query(Shelf_Type).join(Book).join(User).filter(User.id == user_id).all()
        shelves_data = []
        for shelf in shelves: #para cada 'estante' le asigna un id, tipo de estante y libros
            shelf_data = {
                'id': shelf.id,
                'type': shelf.type,
                'books': []
            }
            for book in shelf.books: 
                book_data = {
                    'id': book.id,
                    'cover': book.cover,
                    'isbn': book.isbn,
                    'title': book.title,
                    'user_rating': book.user_rating,
                    'amnt_pages': book.cant_pages,
                    'date_added': book.date_added.isoformat(),
                    'finished_date': book.finished_date.isoformat() if book.finished_date else None,
                    'author': book.author_name
                }
                shelf_data['books'].append(book_data)
                shelves_data.append(shelf_data)
            return jsonify(shelves_data)
    except:
        return jsonify({'message': 'No shelves available'}), 404   

#new book to specific shelf by ide and user by id
@app.route("/users/<user_id>/new_book/<shelf_id>", methods=['POST'])
def new_book(user_id, shelf_id):
    try:
        shelf = Shelf_Type.query.get(shelf_id)
        if not shelf:
            return jsonify({'message': 'Shelf could not be found'}), 404
        data = request.json
        book = Book(cover=data.get('cover'), isbn=data.get('isbn'), title=data.get('title'), user_rating=data.get('user_rating'), cant_pages=data.get('cant_pages'), date_added=datetime.now(), finished_date=data.get('finished_date'), author_name=data.get('author_name'), shelf=shelf)
        db.session.add(new_book)
        db.session.commit()

        book_data = {
            'id': new_book.id,
            'cover': new_book.cover,
            'isbn': new_book.isbn,
            'title': new_book.title,
            'user_rating': new_book.user_rating,
            'cant_pages': new_book.cant_pages,
            'date_added': new_book.date_added.isoformat(),
            'finished_date': new_book.finished_date.isoformat() if new_book.finished_date else None,
            'author_name': new_book.author_name,
            'shelf': new_book.shelf_id
        }

    except:
        return jsonify({'message': 'Book could not be created'}), 400

#update book details
@app.route("/users/<user_id>/shelves/<shelf_id>/<book_id>", methods=['PUT'])
def update_book(user_id, shelf_id, book_id):
    try:
        book = Book.query.get(book_id)
        if not book:
            return jsonify({'message': 'Book could not be found'}), 404
        data = request.json
        book.cover = data.get('cover')
        book.isbn = data.get('isbn')
        book.title = data.get('title')
        book.user_rating = data.get('user_rating')
        book.cant_pages = data.get('cant_pages')
        book.date_added = data.get('date_added').isoformat()
        book.finished_date = data.get('finished_date').isoformat() if new_book.finished_date else None,
        book.author_name = data.get('author_name')
        book.shelf_id = data.get('shelf_id')
        db.session.commit()
        return jsonify({'message': 'Book updated successfully'}), 200
    except:
        return jsonify({'message': 'Book could not be updated'}), 400

#delete book
@app.route("/users/<user_id>/shelves/<shelf_id>/<book_id>", methods=['DELETE'])
def delete_book(iser_id, shelf_id, book_id):
    try:
        book = Book.query.get(book_id)
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message':'Book deleted successfully'}), 200
    except:
        return jsonify({'message':'Book could not be deleted'}), 400

#move book between shelves
@app.route("/users/<user_id>/shelves/<shelf_id>/<book_id>/move", methods=['PUT'])
def move_book(user_id, shelf_id, book_id):
    try:
        book = Book.query.get(book_id)
        if not book:
            return jsonify({'message': 'Book could not be found'}), 404
        data = request.json
        book.shelf_id = data.get('shelf_id')
        db.session.commit()    
        return jsonify({'message': 'Book moved successfully'}), 200
    except:
        return jsonify({'message': 'Book could not be moved'}), 400

