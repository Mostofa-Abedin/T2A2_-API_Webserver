# Import standard library modules
from datetime import timedelta

# Import third-party modules
from flask import Blueprint, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from psycopg2 import errorcodes
from sqlalchemy.exc import IntegrityError

# Import local modules
from init import bcrypt, db
from models.user import User, UserSchema, user_schema

# Create a Blueprint for authentication and user management
auth_bp = Blueprint('auth', __name__)

# Route to register a new user
@auth_bp.route("/register", methods=["POST"])
def register_user():
    try:
        # Load and validate data from the request body
        body_data = UserSchema().load(request.get_json())

        # Extract password and ensure it is provided
        password = body_data.get("password")
        if not password:
            return {"error": "Password is required."}, 400

        # Create a new User instance
        user = User(
            name=body_data.get("name"),
            email=body_data.get("email"),
            phone_number=body_data.get("phone_number"),
            address=body_data.get("address"),
            password=bcrypt.generate_password_hash(password).decode("utf-8")
        )

        # Add and commit the new user to the database
        db.session.add(user)
        db.session.commit()

        # Return the new user data
        return user_schema.dump(user), 201

    # Handle database integrity errors
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The field '{err.orig.diag.column_name}' is required."}, 400
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "An account with this email already exists."}, 400
        return {"error": "A database integrity error occurred."}, 500
    except Exception:
        # Return a generic error message
        return {"error": "An internal server error occurred."}, 500

# Route to login a user
@auth_bp.route("/login", methods=["POST"])
def login_user():
    try:
        # Get data from the request
        body_data = request.get_json()

        # Find the user by email
        user = User.query.filter_by(email=body_data.get("email")).first()

        # Check if the user exists and the password is correct
        if user and bcrypt.check_password_hash(user.password, body_data.get("password")):
            # Create a JWT token with an expiration time
            token = create_access_token(identity=str(user.user_id), expires_delta=timedelta(days=1))

            # Return user info and the token
            return {
                "email": user.email,
                "is_admin": user.is_admin,
                "token": token
            }, 200
        else:
            # Invalid credentials
            return {"error": "Invalid email or password."}, 400
    except Exception:
        # Return a generic error message
        return {"error": "An internal server error occurred."}, 500

# Route to update user information (Admin or self)
@auth_bp.route("/users/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_user(id):
    # Get the current user ID from the JWT
    current_user_id = get_jwt_identity()

    # Fetch the current user (the one making the request)
    current_user = User.query.get(current_user_id)

    # Fetch the user to be updated
    user = User.query.get(id)

    # Check if the user exists
    if not user:
        return {"error": "User not found."}, 404

    # Check if the current user is an admin or the user themselves
    if current_user_id != id and not current_user.is_admin:
        return {"error": "You do not have permission to update this user's information."}, 403

    try:
        # Load and validate data (partial updates allowed)
        body_data = UserSchema().load(request.get_json(), partial=True)

        # Update fields if provided
        if 'name' in body_data:
            user.name = body_data['name']
        if 'email' in body_data:
            user.email = body_data['email']
        if 'phone_number' in body_data:
            user.phone_number = body_data['phone_number']
        if 'address' in body_data:
            user.address = body_data['address']
        if 'password' in body_data:
            user.password = bcrypt.generate_password_hash(body_data['password']).decode("utf-8")

        # Commit changes to the database
        db.session.commit()

        # Return the updated user data
        return user_schema.dump(user), 200
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "An account with this email already exists."}, 400
        return {"error": "A database integrity error occurred."}, 500
    except Exception:
        # Return a generic error message
        return {"error": "An internal server error occurred."}, 500

# Route to delete a user (Admin-only)
@auth_bp.route("/users/<int:id>", methods=['DELETE'])
@jwt_required()
def delete_user(id):
    # Get the current user ID from the JWT
    current_user_id = get_jwt_identity()

    # Fetch the current user
    current_user = User.query.get(current_user_id)

    # Check if the current user is an admin
    if not current_user.is_admin:
        return {"error": "You do not have permission to delete this user."}, 403

    # Fetch the user to be deleted
    user = User.query.get(id)

    # Check if the user exists
    if not user:
        return {"error": "User not found."}, 404

    try:
        # Delete the user
        db.session.delete(user)
        db.session.commit()

        # Return success message
        return {"message": "User deleted successfully."}, 200
    except Exception:
        # Return a generic error message
        return {"error": "An internal server error occurred."}, 500
