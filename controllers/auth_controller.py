from flask import Blueprint, request
from models.user import User, user_schema, UserSchema
from init import bcrypt, db
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from flask_jwt_extended import create_access_token
from datetime import timedelta

# Create a Blueprint for authentication and user management
auth_bp = Blueprint('auth', __name__)

# Route to register a new user

@auth_bp.route("/register", methods=["POST"])
def register_user():
    try:
        # Get the data from the body of the request using UserSchema for validation
        body_data = UserSchema().load(request.get_json())
        
        # Create an instance of the User model
        user = User(
            name=body_data.get("name"),
            email=body_data.get("email"),
            phone_number=body_data.get("phone_number"),
            address=body_data.get("address")
        )
        
        # Hash the password and store it in the 'password_hash' field
        password = body_data.get("password")
        if password:
            user.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        
        # Add and commit to the DB
        db.session.add(user)
        db.session.commit()
        
        # Return acknowledgement
        return user_schema.dump(user), 201

    # Handle database integrity errors
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The column {err.orig.diag.column_name} is required"}, 400
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Email address must be unique"}, 400
    except Exception as e:
        return {"error": str(e)}, 500

# # Route to login a user
@auth_bp.route("/login", methods=["POST"])
def login_user():
    try:
        # Get the data from the request
        body_data = request.get_json()
        
        # Find the user in the database using the provided email
        stmt = db.select(User).filter_by(email=body_data.get("email"))
        user = db.session.scalar(stmt)
        
        # Check if the user exists and the provided password is correct
        if user and bcrypt.check_password_hash(user.password_hash, body_data.get("password")):
            # Create a JWT token with an expiration of 1 day
            token = create_access_token(identity=str(user.user_id), expires_delta=timedelta(days=1))
            
            # Return user info and the token
            return {
                "email": user.email,
                "is_admin": user.is_admin,
                "token": token
            }, 200
        
        # If credentials are invalid, return an error message
        else:
            return {"error": "Invalid email or password"}, 400
    
    except Exception as e:
        return {"error": str(e)}, 500
    
# # Route to get all users (Admin-only)
# @auth_bp.route('/auth/users', methods=['GET'])
# def get_users():
#     pass  # Placeholder for getting all users

# # Route to get a specific user by ID (Admin or self)
# @auth_bp.route('/auth/users/<int:id>', methods=['GET'])
# def get_user(id):
#     pass  # Placeholder for getting a user by ID

# # Route to update user information (Admin or self)
# @auth_bp.route('/auth/users/<int:id>', methods=['PUT'])
# def update_user(id):
#     pass  # Placeholder for updating user information

# # Route to delete a user (Admin-only)
# @auth_bp.route('/auth/users/<int:id>', methods=['DELETE'])
# def delete_user(id):
#     pass  # Placeholder for deleting a user
