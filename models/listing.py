from init import db, ma  # Import the SQLAlchemy database instance (db) and Marshmallow (ma) for serialization
from marshmallow import fields  # Import fields from Marshmallow for schema definitions
from datetime import datetime  # Import datetime for timestamping

# Define the Listing model, representing the 'listings' table in the database
class Listing(db.Model):
    __tablename__ = "listings"  # Explicitly specify the table name as 'listings'
    
    # Attributes (columns) of the table
    listing_id = db.Column(db.Integer, primary_key=True)  # Primary key, unique identifier for each listing
    # Enum for listing status to ensure it can only be 'available' or 'sold'
    listing_status = db.Column(
        db.Enum('available', 'sold', name='listing_status_enum'),
        nullable=False,
        default='available'
    )
    # Date the listing was posted; must not be null, using 'DateTime' data type
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Foreign keys to create relationships with other tables
    car_id = db.Column(
        db.Integer,
        db.ForeignKey("cars.car_id", ondelete="CASCADE"),
        nullable=False
    )  # Foreign key referencing the 'car_id' in the 'cars' table
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False
    )  # Foreign key referencing the 'user_id' in the 'users' table

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
    user = fields.Nested(
        'UserSchema',
        exclude=["listings"],
        many=False,
        dump_only=True
    )  # Use 'UserSchema' to represent the user, exclude 'listings' to prevent circular reference
    car = fields.Nested(
        'CarSchema',
        many=False,
        dump_only=True
    )  # Use 'CarSchema' to represent the car, exclude 'listings' to prevent circular reference

    listing_id = ma.auto_field(dump_only=True)
    date_posted = ma.auto_field(dump_only=True)
    listing_status = ma.auto_field(dump_only=True)
    user_id = ma.auto_field(dump_only=True)
    
    # 'car_id' is required from the client
    car_id = fields.Integer(required=True)
    
    class Meta:
        model = Listing  # Link this schema to the Listing model
        
        
        # Fields to include in the serialized output
        fields = ("listing_id", "car_id", "user_id", "listing_status", "date_posted", "user", "car")
