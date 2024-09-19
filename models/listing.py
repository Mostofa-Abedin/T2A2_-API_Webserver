from init import db, ma  # Import the SQLAlchemy database instance (db) and Marshmallow (ma) for serialization
from marshmallow import fields  # Import fields from Marshmallow for schema definitions

# Define the Listing model, representing the 'listings' table in the database
class Listing(db.Model):
    __tablename__ = "listings"  # Explicitly specify the table name as 'listings'
    
    # Attributes (columns) of the table
    listing_id = db.Column(db.Integer, primary_key=True)  # Primary key, unique identifier for each listing
    # Enum for listing status to ensure it can only be 'available' or 'sold'
    listing_status = db.Column(db.Enum('available', 'sold', name='listing_status_enum'), nullable=False)
    # Date the listing was posted; must not be null, using 'Date' data type
    date_posted = db.Column(db.Date, nullable=False)  
    
    # Foreign keys to create relationships with other tables
    car_id = db.Column(db.Integer, db.ForeignKey("cars.car_id"), nullable=False)  # Foreign key referencing the 'car_id' in the 'cars' table
    seller_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)  # Foreign key referencing the 'user_id' in the 'users' table

    # Relationships with other tables
    # Establish a many-to-one relationship with the 'User' model; a user can have multiple listings
    user = db.relationship("User", back_populates="listings")  
    # Establish a many-to-one relationship with the 'Car' model; a car can have multiple listings
    car = db.relationship("Car", back_populates="listings")  

    # String representation of the Listing object for debugging purposes
    def __repr__(self):
        return f"<Listing {self.listing_id}, Status: {self.listing_status}>"

# Define the ListingSchema using Marshmallow for serialization and deserialization
class ListingSchema(ma.SQLAlchemyAutoSchema):
    # Nested schemas for serializing relationships with the 'User' and 'Car' models
    user = fields.Nested('UserSchema', exclude=["listings"], many=False)  # Use 'UserSchema' to represent the user, exclude the 'listings' field to prevent circular reference
    car = fields.Nested('CarSchema', exclude=["listings"], many=False)  # Use 'CarSchema' to represent the car, exclude the 'listings' field to prevent circular reference

    class Meta:
        model = Listing  # Link this schema to the Listing model
        load_instance = True  # Allow deserialization to model instances
        # Fields to include in the serialized output
        fields = ("listing_id", "car_id", "seller_id", "listing_status", "date_posted", "user", "car")

