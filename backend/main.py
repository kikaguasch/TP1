from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, User, Book, Shelf_Type
from datetime import datetime
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
    <h1>Welcome to our library API!</h1>
    </body>
    </html>  
    """
#get users
@app.route("/users/", methods=['GET'])
def users():
    try:
        users = User.query.all()
        users_data = []
        for user in users:
            user_data = {
                'id': user.id,
                'name': user.name,
                'age': user.age,
            }
            users_data.append(user_data)
        return jsonify(users_data)
    except:
        return jsonify({'message': 'No current readers'}), 404

#create users    
@app.route("/users/create", methods=['POST'])
def new_user():
    try:
        data = request.json
        print(f"Received data: {data}")
        if not data:
            return jsonify({'message': 'No input data provided'}), 400
        name = data.get('name')
        age = data.get('age')
        if not name or not age:
            return jsonify({'message': 'Name and age are required'}), 400

        user = User(name=name, age=age)
        # new_shelf = User(name=user.name, age=user.age)
        db.session.add(user)
        db.session.commit()

        return jsonify({'success': True, 'id': user.id}), 201
        # return jsonify({'message': 'User created', 'user_id': user.id}), 201 #creado

    except Exception as error:
        print(f"Error: {error}")
        # return jsonify({'message': 'Could not create user', 'error': str(error)}), 400
        return jsonify({'success': False, 'message': str(error)}), 400

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
        }
        return jsonify(user_data)
    except:
        return jsonify({'message': 'User does not exist'}), 404

#get shelves from each user by id
@app.route("/users/<user_id>/shelves/<shelf_id>", methods=['GET'])
def user_specific_shelves(user_id, shelf_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User could not be found'}), 404
        
        shelf_type = Shelf_Type.query.get(shelf_id)
        if not shelf_type:
            return jsonify({'message': 'Shelf could not be found'}), 404
        
        shelf_data = {
            'id': shelf_type.id,
            'type': shelf_type.type,
            'books': []
        }
        books = Book.query.filter_by(user_id=user_id, shelf_id=shelf_type.id).all()
        for book in books: 
            book_data = {
                'id': book.id,
                'title': book.title,
                'author_name': book.author_name,
                'amnt_pages': book.amnt_pages,
                'date_added': book.date_added.isoformat(),
                'cover_url': book.cover_url
            }
            shelf_data['books'].append(book_data)
        return jsonify(shelf_data)
    except:
        return jsonify({'message': 'No shelves available'}), 404   

#create new book
@app.route("/users/<user_id>/shelves/<shelf_id>/books", methods=['POST'])
def new_book(user_id, shelf_id):
    try:
        data = request.json
        print(f"Received data: {data}")
        shelf_type = Shelf_Type.query.get(shelf_id)
        if not shelf_type:
            return jsonify({'message': 'Shelf could not be found'}), 404
        new_book = Book(
            title=data.get('title'), 
            amnt_pages=data.get('amnt_pages'), 
            date_added=datetime.now(), 
            author_name=data.get('author_name'), 
            shelf_id=shelf_type.id,
            user_id=user_id,
            cover_url=data.get('cover_url')
        )  
        db.session.add(new_book)
        db.session.commit()

        # return jsonify({'message': 'Book created successfully'}), 201
        return jsonify({'success': True, 'title': new_book.title }), 201
    except Exception as error:
        print(f"Error: {error}")
        # return jsonify({'message': 'Book could not be created'}), 400
        return jsonify({'success': False, 'message': str(error)}), 400


#update book details
@app.route("/users/<user_id>/shelves/<shelf_id>/<book_id>", methods=['PUT'])
def update_book(user_id, shelf_id, book_id):
    try:
        book = Book.query.get(book_id)
        if not book:
            return jsonify({'message': 'Book could not be found'}), 404
        data = request.json
        book.title = data.get('title')
        book.amnt_pages = data.get('amnt_pages')
        book.date_added = datetime.fromisoformat(data.get('date_added'))
        book.author_name = data.get('author_name')
        book.shelf_id = data.get('shelf_id')
        book.user_id = data.get('user_id')
        book.cover_url = data.get('cover_url')
        db.session.commit()

        book_data = {
            'id': book.id,
            'title': book.title,
            'author_name': book.author_name,
            'amnt_pages': book.amnt_pages,
            'date_added': book.date_added.isoformat(),
            'cover_url': book.cover_url
        }
        return jsonify({'message': 'Book updated successfully'}), 200
    except:
        return jsonify({'message': 'Book could not be updated'}), 400

#delete book
@app.route("/users/<user_id>/shelves/<shelf_id>/<book_id>", methods=['DELETE'])
def delete_book(user_id, shelf_id, book_id):
    try:
        book = Book.query.get(book_id)
        if not book:
            return jsonify({'message': 'Book could not be found'}), 404
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
        book.shelf = data.get('shelf')
        db.session.commit()    
        return jsonify({'message': 'Book moved successfully'}), 200
    except:
        return jsonify({'message': 'Book could not be moved'}), 400

if __name__ == '__main__':
    print('Staring server...')
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)
    print('Stopping server...!')