from init import db, ma  # Importing the SQLAlchemy database instance (db) and Marshmallow (ma) for serialization
from marshmallow import fields, validate  # Import fields and validation utilities from Marshmallow
from marshmallow.validate import Regexp  # Import Regexp for regular expression validation

# Define the User model, representing the 'users' table in the database
class User(db.Model):
    __tablename__ = "users"  # Explicitly specify the table name as 'users'
    
    # Attributes (columns) of the table
    user_id = db.Column(db.Integer, primary_key=True)  # Primary key, unique identifier for each user
    name = db.Column(db.String(100), nullable=False)  # Name of the user, must not be null, max length 100 characters
    email = db.Column(db.String(50), nullable=False, unique=True)  # Email, must not be null and must be unique
    password = db.Column(db.String(200), nullable=False)  # Password, stored as a hashed string, must not be null
    phone_number = db.Column(db.String(15))  # Phone number, can include symbols like '+' and has a max length of 15 characters
    address = db.Column(db.String(255))  # Address of the user, max length 255 characters
    is_admin = db.Column(db.Boolean, default=False)  # Boolean to indicate if the user is an admin, defaults to False

    # Relationships with other tables
    listings = db.relationship("Listing", back_populates="user")  # One-to-many relationship with 'Listing', referenced by 'user' in the Listing model
    transactions = db.relationship("Transaction", back_populates="user")  # One-to-many relationship with 'Transaction', referenced by 'user' in the Transaction model

    # String representation of the User object, useful for debugging
    def __repr__(self):
        return f"<User {self.email}>"  # Returns a string representing the User instance by its email

# Define the UserSchema using Marshmallow for serialization and deserialization
class UserSchema(ma.Schema):
    # Nested schemas for serializing relationships (listings and transactions)
    listings = fields.List(fields.Nested('ListingSchema', exclude=["user"]))  # List of related 'ListingSchema' objects, excluding the 'user' field to prevent circular reference
    transactions = fields.List(fields.Nested('TransactionSchema', exclude=["user"]))  # List of related 'TransactionSchema' objects, excluding the 'user' field to prevent circular reference
    
    # Email field with validation for a correct email format using a regular expression
    email = fields.String(required=True, validate=Regexp(r"^\S+@\S+\.\S+$", error="Invalid Email Format."))  # Ensures the email is in a valid format
    
    class Meta:
        # Fields to include in the serialized output
        fields = ("user_id", "name", "email", "password", "phone_number", "address", "is_admin", "listings", "transactions")

# Schema instance for serializing a single user object, excluding the password field for security
user_schema = UserSchema(exclude=["password"])

# Schema instance for serializing a list of user objects, excluding the password field for security
users_schema = UserSchema(many=True, exclude=["password"])
