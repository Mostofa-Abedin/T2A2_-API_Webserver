# Import the SQLAlchemy database instance (db) and Marshmallow (ma) for serialization
from init import db, ma

# Import fields and validation utilities from Marshmallow
from marshmallow import fields, validate

# Import the MakeModelYear model for relationships
from models.makemodelyear import MakeModelYear

# Define the Car model representing the 'cars' table in the database
class Car(db.Model):
    __tablename__ = "cars"  # Specify the table name

    # Primary key, unique identifier for each car
    car_id = db.Column(db.Integer, primary_key=True)
    # Mileage of the car, required
    mileage = db.Column(db.Integer, nullable=False)
    # Price of the car, required
    price = db.Column(db.Float, nullable=False)
    # Condition of the car: 'new', 'used', or 'certified'
    condition = db.Column(
        db.Enum('new', 'used', 'certified', name='car_condition_enum'),
        nullable=False
    )
    # Optional description of the car
    description = db.Column(db.String(1000))
    # URL to the car's image
    image_url = db.Column(db.String(100))

    # Foreign key referencing 'make_model_year_id' in the 'makemodelyear' table
    make_model_year_id = db.Column(
        db.Integer,
        db.ForeignKey('makemodelyear.make_model_year_id'),
        nullable=False
    )

    # Relationship to the Listing model
    listings = db.relationship(
        "Listing",
        back_populates="car",
        cascade="all, delete-orphan"
    )
    # Relationship to the CarTransaction model
    car_transactions = db.relationship(
        "CarTransaction",
        back_populates="car"
    )
    # Relationship to the MakeModelYear model
    make_model_year = db.relationship(
        "MakeModelYear",
        back_populates="cars"
    )

    def __repr__(self):
        # String representation for debugging purposes
        return f"<Car {self.car_id}, Price: {self.price}>"

# Define the CarSchema using Marshmallow for serialization and deserialization
class CarSchema(ma.Schema):
    # Nested schema for related listings, excluding 'car' to prevent recursion
    listings = fields.List(
        fields.Nested('ListingSchema', exclude=["car"])
    )
    # Nested schema for related make_model_year, excluding 'cars' to prevent recursion
    make_model_year = fields.Nested(
        'MakeModelYearSchema',
        exclude=["cars"],
        dump_only=True
    )
    # Nested schema for related car_transactions, excluding 'car' to prevent recursion
    car_transactions = fields.List(
        fields.Nested('CarTransactionSchema', exclude=["car"])
    )

    # Fields with validation
    mileage = fields.Integer(required=True)
    price = fields.Float(required=True)
    condition = fields.String(
        required=True,
        validate=validate.OneOf(['new', 'used', 'certified'])
    )
    description = fields.String()
    image_url = fields.String()
    make_model_year_id = fields.Integer(required=True)

    class Meta:
        # Fields to include in the serialized output
        fields = (
            "car_id", "mileage", "price", "condition",
            "description", "image_url", "make_model_year_id",
            "make_model_year", "listings", "car_transactions"
        )

# Schema instances for serializing Car objects
car_schema = CarSchema()
cars_schema = CarSchema(many=True)
