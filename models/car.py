from init import db, ma  # Import the SQLAlchemy database instance (db) and Marshmallow (ma) for serialization
from marshmallow import fields, validate  # Import fields from Marshmallow for schema definitions
from models.makemodelyear import MakeModelYear  # Import MakeModelYear before referencing it
# Define the Car model, representing the 'cars' table in the database
class Car(db.Model):
    __tablename__ = "cars"  # Explicitly specify the table name as 'cars'
    
    # Attributes (columns) of the table
    car_id = db.Column(db.Integer, primary_key=True)  # Primary key, unique identifier for each car
    mileage = db.Column(db.Integer, nullable=False)  # Mileage of the car, stored as an integer, must not be null
    price = db.Column(db.Float, nullable=False)  # Price of the car, stored as a floating-point number, must not be null
    condition = db.Column(db.Enum('new', 'used', 'certified', name='car_condition_enum'), nullable=False)  # Enum to specify the condition of the car
    description = db.Column(db.String(1000))  # Optional description of the car, maximum length of 1000 characters
    image_url = db.Column(db.String(100))  # URL to the car's image, max length of 100 characters
    
    # Foreign key to reference the MakeModelYear table.
    make_model_year_id = db.Column(db.Integer, db.ForeignKey('makemodelyear.make_model_year_id'), nullable=False)  # Foreign key referencing 'make_model_year_id' in the 'makemodelyear' table
    
    # Relationships with other tables
    # Establish a one-to-many relationship with the 'Listing' model; a car can be listed multiple times
    listings = db.relationship("Listing", back_populates="car", cascade="all, delete-orphan")  
    # Establish a one-to-many relationship with the 'CarTransaction' model; a car can have multiple transactions
    car_transactions = db.relationship("CarTransaction", back_populates="car")
    # Establish a many-to-one relationship with the 'MakeModelYear' model; a car references a specific make, model, and year
    make_model_year = db.relationship("MakeModelYear", back_populates="cars")  

    # String representation of the Car object for debugging purposes.
    def __repr__(self):
        return f"<Car {self.car_id}, Price: {self.price}>"

# Define the CarSchema using Marshmallow for serialization and deserialization.
class CarSchema(ma.Schema):
    # Nested schemas for serializing relationships
    listings = fields.List(fields.Nested('ListingSchema', exclude=["car"]))  # Use 'ListingSchema' to represent associated listings, excluding the 'car' field to prevent circular reference
    make_model_year = fields.Nested('MakeModelYearSchema', exclude=["cars"], dump_only=True)  # Use 'MakeModelYearSchema' to represent the make, model, and year, excluding 'cars' to prevent circular reference
    car_transactions = fields.List(fields.Nested('CarTransactionSchema', exclude=["car"]))
    class Meta:
        # Fields to include in the serialized output; defines how the data will be structured when the car is converted to JSON
        fields = ("car_id", "mileage", "price", "condition", "description", "image_url", "make_model_year_id", "make_model_year")

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