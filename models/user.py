# Import SQLAlchemy and Marshmallow instances
from init import db, ma

# Import fields and Regexp for validation from Marshmallow
from marshmallow import fields
from marshmallow.validate import Regexp

# Import the CarTransaction model for relationships
from models.car_transaction import CarTransaction

# Define the User model representing the 'users' table
class User(db.Model):
    __tablename__ = "users"  # Specify the table name

    # Define the columns/attributes
    user_id = db.Column(db.Integer, primary_key=True)  # Primary key
    name = db.Column(db.String(100), nullable=False)  # User's name, required
    email = db.Column(db.String(50), nullable=False, unique=True)  # User's email, unique and required
    password = db.Column(db.String(200), nullable=False)  # User's hashed password, required
    phone_number = db.Column(db.String(15))  # User's phone number
    address = db.Column(db.String(255))  # User's address
    is_admin = db.Column(db.Boolean, default=False)  # Flag to indicate admin users

    # Relationship to the Listing model
    listings = db.relationship(
        "Listing",
        back_populates="user",
        cascade="all, delete-orphan"
    )  # User's listings with cascade delete

    # Relationship to the CarTransaction model
    car_transactions = db.relationship(
        "CarTransaction",
        back_populates="user"
    )  # User's car transactions

    def __repr__(self):
        # String representation of the User object
        return f"<User {self.email}>"

# Define the UserSchema for serialization/deserialization
class UserSchema(ma.Schema):
    # Nested field for user's listings
    listings = fields.List(
        fields.Nested('ListingSchema', exclude=["user", "car"])
    )  # Exclude 'user' and 'car' to prevent recursion

    # Nested field for user's car transactions
    car_transactions = fields.List(
        fields.Nested('CarTransactionSchema', exclude=["user", "car"])
    )  # Exclude 'user' and 'car' to prevent recursion

    # Email field with regex validation
    email = fields.String(
        required=True,
        validate=Regexp(
            r"^\S+@\S+\.\S+$",
            error="Invalid email format."
        )
    )  # Validate email format

    # Password field, load_only to avoid exposing it
    password = fields.String(required=True, load_only=True)  # Required but not included in output

    class Meta:
        # Fields to include in the serialized output
        fields = (
            "user_id", "name", "email", "password",
            "phone_number", "address", "is_admin",
            "listings", "car_transactions"
        )

# Schema instances for serializing User objects
user_schema = UserSchema()  # For a single user
users_schema = UserSchema(many=True)  # For multiple users
