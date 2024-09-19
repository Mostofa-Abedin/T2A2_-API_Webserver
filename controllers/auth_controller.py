from flask import Blueprint, request
from models.user import User, user_schema, UserSchema
from init import bcrypt, db
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
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
        
        # Hash the password and store it in the 'password' field
        password = body_data.get("password")
        if password:
            user.password = bcrypt.generate_password_hash(password).decode("utf-8")

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

# Route to login a user
@auth_bp.route("/login", methods=["POST"])
def login_user():
    try:
        # Get the data from the request
        body_data = request.get_json()
        
        # Find the user in the database using the provided email
        stmt = db.select(User).filter_by(email=body_data.get("email"))
        user = db.session.scalar(stmt)
        
        # Check if the user exists and the provided password is correct
        if user and bcrypt.check_password_hash(user.password, body_data.get("password")):
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

# Route to update user information (Admin or self)
@auth_bp.route("/users/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_user(id):
    # Get the current user ID from the JWT
    current_user_id = get_jwt_identity()

    # Fetch the current user (the one making the request)
    stmt_current_user = db.select(User).filter_by(user_id=current_user_id)
    current_user = db.session.scalar(stmt_current_user)
    
    # Fetch the user from the database to be updated
    stmt = db.select(User).filter_by(user_id=id)
    user = db.session.scalar(stmt)
    
    # Check if the user exists
    if not user:
        return {"error": "User does not exist."}, 404
    
    # Check if the current user is an admin or the user themselves
    if current_user_id != id and not current_user.is_admin:
        return {"error": "You do not have permission to update this user's information."}, 403
    
    # Get the fields from the body of the request
    body_data = UserSchema().load(request.get_json(), partial=True)
    
    # Update the fields as required
    user.name = body_data.get("name") or user.name
    user.email = body_data.get("email") or user.email
    user.phone_number = body_data.get("phone_number") or user.phone_number
    user.address = body_data.get("address") or user.address
    password = body_data.get("password")
    if password:
        user.password = bcrypt.generate_password_hash(password).decode("utf-8")

    # Commit the changes to the database
    db.session.commit()
    
    # Return the updated user data
    return user_schema.dump(user), 200

# Route to delete a user (Admin-only)
@auth_bp.route("/users/<int:id>", methods=['DELETE'])
@jwt_required()
def delete_user(id):
    # Get the current user ID from the JWT
    current_user_id = get_jwt_identity()

    # Fetch the current user (the one making the request)
    stmt_current_user = db.select(User).filter_by(user_id=current_user_id)
    current_user = db.session.scalar(stmt_current_user)
    
    # Check if the current user is an admin
    if not current_user.is_admin:
        return {"error": "You do not have permission to delete this user."}, 403
    
    # Fetch the user to be deleted
    stmt = db.select(User).filter_by(user_id=id)
    user = db.session.scalar(stmt)

    # Check if the user exists
    if not user:
        return {"error": "User does not exist."}, 404

    # Delete the user
    db.session.delete(user)
    db.session.commit()

    # Return success message
    return {"message": "User deleted successfully."}, 200
