# Step-by-Step Guide for Setting up an API Project with Flask

## Step 1: Project Setup

1. **Create Project Directory**:
   - Create a new folder for your project (e.g., `trello_clone`).
2. **Create Virtual Environment**:
   - Open your terminal and navigate to the project folder.
   - Run the command to create a virtual environment:
     ```bash
     python3 -m venv .venv
     ```
   - Activate the virtual environment:
     - On MacOS/Linux:
       ```bash
       source .venv/bin/activate
       ```
     - On Windows:
       ```bash
       .venv\Scripts\activate
       ```

## Step 2: Install Necessary Packages

1. Install the following Flask-related libraries:

   ```bash
   pip install Flask SQLAlchemy flask-marshmallow Flask-Bcrypt Flask-JWT-Extended python-dotenv psycopg2-binary
   ```

2. **Create `requirements.txt`**:
   - After installing the packages, create a `requirements.txt` file to track dependencies:
     ```bash
     pip freeze > requirements.txt
     ```

## Step 3: Create Configuration Files

1. **`.env` File**:

   - Create a `.env` file for sensitive information like the database URL and JWT secret key:
     ```bash
     DATABASE_URL = "postgresql+psycopg2://trello_dev:123456@localhost:5432/trello_db"
     JWT_SECRET_KEY = "secret"
     ```

2. **`.env.example`**:

   - Create an example `.env` file without sensitive data, which other users can use to set up their environment:
     ```bash
     DATABASE_URL =
     JWT_SECRET_KEY =
     ```

3. **`.flaskenv` File**:

   - Create a `.flaskenv` file to configure the Flask app:
     ```bash
     FLASK_APP=main
     FLASK_DEBUG=1
     FLASK_RUN_PORT=8080
     ```

4. **`.gitignore` File**:
   - Create a `.gitignore` file to exclude unnecessary or sensitive files:
     ```bash
     __pycache__
     .venv
     .env
     ```

## Step 4: Initialize the App

1. **Create `init.py`**:

   - Create a file called `init.py` to initialize the libraries needed for the app:

     ```python
     from flask_sqlalchemy import SQLAlchemy
     from flask_marshmallow import Marshmallow
     from flask_bcrypt import Bcrypt
     from flask_jwt_extended import JWTManager

     db = SQLAlchemy()
     ma = Marshmallow()
     bcrypt = Bcrypt()
     jwt = JWTManager()
     ```

2. **Create `main.py`**:

   - Create a `main.py` file to set up the Flask app and link it to the database and JWT:

     ```python
     import os
     from flask import Flask
     from init import db, ma, bcrypt, jwt

     def create_app():
         app = Flask(__name__)
         app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
         app.config["JWT_SECRET"] = os.environ.get("JWT_SECRET_KEY")

         db.init_app(app)
         ma.init_app(app)
         bcrypt.init_app(app)
         jwt.init_app(app)

         return app
     ```

## Step 5: Set Up the Database

1. **PostgreSQL Setup**:
   - Create a PostgreSQL database for the project.
     ```bash
     sudo -u postgres psql
     ```
   - Inside the PostgreSQL console, run the following commands:
     ```sql
     CREATE DATABASE trello_db;
     CREATE USER trello_dev WITH PASSWORD '123456';
     GRANT ALL PRIVILEGES ON DATABASE trello_db TO trello_dev;
     ```

## Step 6: Run the App

1. **Run the Flask App**:
   - After setting everything up, run the app using the following command:
     ```bash
     flask run
     ```

This is the initial setup for building an API from scratch, including environment configurations, database setup, and project structure. We’ll expand this guide with more models, views, and controllers as we progress through the lectures.

## Step 7: Adding Blueprints and CLI Commands

1. **Create Controllers Folder and CLI Commands**

```python
from flask import Blueprint
from init import db
from models.user import User

db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_tables():
    db.create_all()
    print("Tables created!")

@db_commands.cli.command('drop')
def drop_tables():
    db.drop_all()
    print("Tables dropped!")

@db_commands.cli.command('seed')
def seed_tables():
    users = [
        User(email="admin@test.com", password=bcrypt.generate_password_hash("123456").decode('utf-8'), is_admin=True),
        User(email="user@test.com", password=bcrypt.generate_password_hash("123456").decode('utf-8'), is_admin=False)
    ]
    db.session.add_all(users)
    db.session.commit()
    print("Tables seeded!")
```

2. **Register Blueprints in main.py**

Add this to your main.py file to register the blueprint:

```python
from controllers.cli_controllers import db_commands

app = Flask(__name__)
# Blueprint registration
app.register_blueprint(db_commands)
```

3. **Run CLI Commands**
   After registering the blueprints, you can now run the following CLI commands in your terminal:

```bash
flask db create   # Creates all tables
flask db drop     # Drops all tables
flask db seed     # Seeds the tables with initial data
```

### Step 8: User Model and Authentication

1. **Create User Model**

In your models folder, create a user.py file with the following content:

```python
from init import db, ma

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
```

2. **Authentication Routes**

In your controllers folder, create a new file called auth_controller.py and add the following routes for user registration and login:

```python
from flask import Blueprint, request
from init import db, bcrypt
from models.user import User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = User(
        email=data['email'],
        password=bcrypt.generate_password_hash(data['password']).decode('utf-8')
    )
    db.session.add(user)
    db.session.commit()
    return {'message': 'User registered successfully!'}
```

### Step 9: Creating the Card Model

1. **Create card.py in the models folder:**

```python

from init import db, ma

class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    status = db.Column(db.String, nullable=False)
    priority = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='cards')

class CardSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Card
        load_instance = True

    id = ma.auto_field()
    title = ma.auto_field()
    description = ma.auto_field()
    status = ma.auto_field()
    priority = ma.auto_field()
    date = ma.auto_field()
    user = ma.Nested('UserSchema', only=('id', 'name', 'email'))
```

2. **Back-populating in user.py:**

Update the user.py model by adding a relationship with the Card model.

```python
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    cards = db.relationship('Card', back_populates='user')

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

    id = ma.auto_field()
    name = ma.auto_field()
    email = ma.auto_field()
    cards = ma.Nested('CardSchema', many=True, exclude=('user',))
```

### Step 10: Seeding the Database with Card Data

In cli_controllers.py, update the seed_tables command to seed both the User and Card data.

```python
@db_commands.cli.command('seed')
def seed_tables():
    users = [
        User(name="Admin", email="admin@test.com", password=bcrypt.generate_password_hash("123456").decode('utf-8'), is_admin=True),
        User(name="User", email="user@test.com", password=bcrypt.generate_password_hash("123456").decode('utf-8'), is_admin=False)
    ]
    db.session.add_all(users)
    db.session.commit()

    cards = [
        Card(title="GitHub Operations", description="Perform GitHub operations", status="to-do", priority="high", date=date.today(), user=users[0]),
        Card(title="Initialize Modules", description="Set up necessary modules", status="ongoing", priority="high", date=date.today(), user=users[0]),
        Card(title="Add Comments", description="Add meaningful comments to the code", status="to-do", priority="low", date=date.today(), user=users[1])
    ]
    db.session.add_all(cards)
    db.session.commit()
    print("Tables seeded!")
```

### Section 11: Fetching Data from Database

To verify that the User and Card models are correctly related, use the following query in your auth_controller.py or an appropriate route controller:

```python
@auth.route('/users/<int:id>/cards', methods=['GET'])
def get_user_cards(id):
    user = User.query.get(id)
    if not user:
        return {"error": "User not found"}, 404

    cards_schema = CardSchema(many=True)
    return cards_schema.dump(user.cards), 200
```

### Section 12: Relationships and Back-Population

The key to the Card and User relationship is the back_populates attribute in both models. This ensures that fetching a user includes their cards and vice versa.

For example:

When you fetch a User, the cards field will list all the associated Card objects.
When you fetch a Card, the user field will include the associated User object.

### Section 13: Creating Comment Model

Create comment.py in the models folder:

```python
from init import db, ma

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id'), nullable=False)

    card = db.relationship('Card', back_populates='comments')

class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comment
        load_instance = True

    id = ma.auto_field()
    content = ma.auto_field()
    date = ma.auto_field()
    card = ma.Nested('CardSchema', only=('id', 'title'))
```

2. Back-populating in card.py:
   Update the card.py model to establish the relationship between Card and Comment:

```python
class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    status = db.Column(db.String, nullable=False)
    priority = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='cards')
    comments = db.relationship('Comment', back_populates='card')

class CardSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Card
        load_instance = True

    id = ma.auto_field()
    title = ma.auto_field()
    description = ma.auto_field()
    status = ma.auto_field()
    priority = ma.auto_field()
    date = ma.auto_field()
    user = ma.Nested('UserSchema', only=('id', 'name', 'email'))
    comments = ma.Nested('CommentSchema', many=True)
```

### Section 14: Seeding the Database with Comment Data

In cli_controllers.py, update the seed_tables command to include comment data.

```python
@db_commands.cli.command('seed')
def seed_tables():
    users = [
        User(name="Admin", email="admin@test.com", password=bcrypt.generate_password_hash("123456").decode('utf-8'), is_admin=True),
        User(name="User", email="user@test.com", password=bcrypt.generate_password_hash("123456").decode('utf-8'), is_admin=False)
    ]
    db.session.add_all(users)
    db.session.commit()

    cards = [
        Card(title="GitHub Operations", description="Perform GitHub operations", status="to-do", priority="high", date=date.today(), user=users[0]),
        Card(title="Initialize Modules", description="Set up necessary modules", status="ongoing", priority="high", date=date.today(), user=users[0])
    ]
    db.session.add_all(cards)
    db.session.commit()

    comments = [
        Comment(content="This is a test comment", date=date.today(), card=cards[0]),
        Comment(content="Another test comment", date=date.today(), card=cards[1])
    ]
    db.session.add_all(comments)
    db.session.commit()

    print("Tables seeded!")
```

### Section 15: Comment Controller

Create comment_controller.py in the controllers folder:

```python
from flask import Blueprint, request
from init import db
from models.comment import Comment, CommentSchema
from models.card import Card
from flask_jwt_extended import jwt_required, get_jwt_identity

comments_bp = Blueprint('comments', __name__, url_prefix='/comments')

@comments_bp.route('/', methods=['POST'])
@jwt_required()
def create_comment():
    data = request.get_json()
    card = Card.query.get(data['card_id'])

    if not card:
        return {"error": "Card not found"}, 404

    comment = Comment(
        content=data['content'],
        date=date.today(),
        card=card
    )

    db.session.add(comment)
    db.session.commit()

    return CommentSchema().dump(comment), 201

@comments_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_comment(id):
    comment = Comment.query.get(id)

    if not comment:
        return {"error": "Comment not found"}, 404

    db.session.delete(comment)
    db.session.commit()

    return {"message": "Comment deleted"}, 200
```

### Section 16: Registering the Comment Blueprint

In main.py, register the comment blueprint:

```python
from controllers.comment_controller import comments_bp

app = Flask(__name__)
app.register_blueprint(comments_bp)
```

### Section 17: Testing in Insomnia

You can now create and delete comments in Insomnia:

1. POST Request to create a comment:
   Endpoint: /comments/
   Body:

```json
{
  "content": "Great job on the feature!",
  "card_id": 1
}
```

Example response:

```json
{
  "id": 1,
  "content": "Great job on the feature!",
  "date": "2024-09-13",
  "card": {
    "id": 1,
    "title": "GitHub Operations"
  }
}
```

2. DELETE Request to delete a comment:

Endpoint: /comments/<comment_id>

Example response

```json
{
  "message": "Comment deleted"
}
```

### Section 18: Setting up the Comment Controller

1. Import Dependencies in comment_controller.py:

```python
from flask import Blueprint, request
from init import db
from models.comment import Comment, CommentSchema
from models.card import Card
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date
```

2. Define the Blueprint for Comments:

```python
comments_bp = Blueprint('comments', __name__, url_prefix='/cards/<int:card_id>/comments')
```

### Section 19: Creating Routes for Comments

1. Create Comment Route
   This route will allow users to create a comment on a specific card:

```python
@comments_bp.route('/', methods=['POST'])
@jwt_required()
def create_comment(card_id):
    body_data = request.get_json()
    card = Card.query.get(card_id)
    if not card:
        return {"error": "Card not found"}, 404

    comment = Comment(
        content=body_data['content'],
        date=date.today(),
        user_id=get_jwt_identity(),
        card=card
    )
    db.session.add(comment)
    db.session.commit()
    return CommentSchema().dump(comment), 201
```

2. Delete Comment Route

This route allows deleting a specific comment by its comment_id:

```python
@comments_bp.route('/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(card_id, comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        return {"error": "Comment not found"}, 404

    db.session.delete(comment)
    db.session.commit()
    return {"message": f"Comment '{comment.content}' deleted successfully"}, 200
```

3. Update Comment Route

This route allows updating a specific comment's content:

```python
@comments_bp.route('/<int:comment_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_comment(card_id, comment_id):
    body_data = request.get_json()
    comment = Comment.query.get(comment_id)
    if not comment:
        return {"error": "Comment not found"}, 404

    if 'content' in body_data:
        comment.content = body_data['content']

    db.session.commit()
    return CommentSchema().dump(comment), 200
```

### Section 20: Registering the Blueprint

In card_controller.py, update it to register the comments blueprint:

```python
from controllers.comment_controller import comments_bp

card_bp = Blueprint('cards', __name__, url_prefix='/cards')

# Registering the comments blueprint within the card blueprint
card_bp.register_blueprint(comments_bp)
```

### Section 21: Testing Comments in Insomnia

1. POST Request to Create a Comment

- URL: /cards/<card_id>/comments/
- Body:

```json
{
  "content": "This is a new comment"
}
```

2. DELETE Request to Delete a Comment

- URL: /cards/<card_id>/comments/<comment_id>

3. PUT/PATCH Request to Update a Comment

- URL: /cards/<card_id>/comments/<comment_id>
- Body

```json
{
  "content": "Updated comment content"
}
```

```mermaid
erDiagram
    Users {
        int id PK
        string name
        string email UNIQUE
        string password_hash
        string phone_number
        string "address"
    }

    Cars {
        int id PK
        string make
        string model
        int year
        int mileage
        float price
        string fuel_type
        string condition
        string description
        string image_url
        int seller_id FK
        timestamp date_added
    }

    Listings {
        int id PK
        int car_id FK
        int seller_id FK
        string listing_status
        timestamp date_posted
    }

    Transactions {
        int id PK
        int buyer_id FK
        int car_id FK
        timestamp transaction_date
        float amount
        string status
    }

    Users ||--o{ Cars : "lists"
    Users ||--o{ Listings : "creates"
    Users ||--o{ Transactions : "makes"

    Cars ||--|| Listings : "is listed in"
    Cars ||--|| Transactions : "is sold in"

```

How do you account for the following scenarios in your database?

1. A user can be both a buyer and a seller. Therefore something about role needs to be changed?

Other things, I do not like and it might be simpler to get rid of these things for the sake of simplicity.

1. I don't think an expiry date is necessary as it creates additional hassle. Therefore, we also don't need "One-to-Many with Listings: A car can be listed multiple times if it remains unsold, but each listing corresponds to one car. This relationship is established through the car_id foreign key in the Listings table."

Other questions?

1. Are there any junction tables needed?
2. Can you think of any edge case that might not have been taken into account?
