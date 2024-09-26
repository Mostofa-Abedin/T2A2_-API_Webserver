# Import the SQLAlchemy database instance (db) and Marshmallow (ma) for serialization
from init import db, ma

# Import fields from Marshmallow for schema definitions
from marshmallow import fields

# Import datetime for timestamping
from datetime import datetime

# Define the Listing model representing the 'listings' table
class Listing(db.Model):
    __tablename__ = "listings"  # Specify the table name

    # Primary key, unique identifier for each listing
    listing_id = db.Column(db.Integer, primary_key=True)

    # Enum for listing status; can be 'available' or 'sold'
    listing_status = db.Column(
        db.Enum('available', 'sold', name='listing_status_enum'),
        nullable=False,
        default='available'
    )

    # Date when the listing was posted
    date_posted = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    # Foreign key referencing 'car_id' in the 'cars' table
    car_id = db.Column(
        db.Integer,
        db.ForeignKey("cars.car_id", ondelete="CASCADE"),
        nullable=False
    )

    # Foreign key referencing 'user_id' in the 'users' table
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False
    )

    # Relationship to the User model
    user = db.relationship(
        "User",
        back_populates="listings"
    )

    # Relationship to the Car model
    car = db.relationship(
        "Car",
        back_populates="listings"
    )

    def __repr__(self):
        # String representation for debugging
        return f"<Listing {self.listing_id}, Status: {self.listing_status}>"

# Define the ListingSchema for serialization/deserialization
class ListingSchema(ma.SQLAlchemyAutoSchema):
    # Nested field for the related user
    user = fields.Nested(
        'UserSchema',
        exclude=["listings"],
        many=False,
        dump_only=True
    )

    # Nested field for the related car
    car = fields.Nested(
        'CarSchema',
        many=False,
        dump_only=True
    )

    # Fields set as dump_only to prevent client from supplying them
    listing_id = ma.auto_field(dump_only=True)
    date_posted = ma.auto_field(dump_only=True)
    listing_status = ma.auto_field(dump_only=True)
    user_id = ma.auto_field(dump_only=True)

    # 'car_id' is required input from the client when creating a listing
    car_id = fields.Integer(required=True)

    class Meta:
        # Link this schema to the Listing model
        model = Listing

        # Fields to include in the serialized output
        fields = (
            "listing_id", "car_id", "user_id",
            "listing_status", "date_posted",
            "user", "car"
        )

