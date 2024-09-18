from init import db, ma  # Import the SQLAlchemy database instance (db) and Marshmallow (ma) for serialization
from marshmallow import fields  # Import fields from Marshmallow for schema definitions

# Define the MakeModelYear model, representing the 'makemodelyear' table in the database
class MakeModelYear(db.Model):
    __tablename__ = "makemodelyear"  # Explicitly specify the table name as 'makemodelyear'
    
    # Attributes (columns) of the table
    make_model_year_id = db.Column(db.Integer, primary_key=True)  # Primary key, unique identifier for each make, model, and year combination
    make = db.Column(db.String(100), nullable=False)  # Car make (e.g., Toyota), must not be null, max length 100 characters
    model = db.Column(db.String(100), nullable=False)  # Car model (e.g., Corolla), must not be null, max length 100 characters
    year = db.Column(db.Integer, nullable=False)  # Year of the car's make, must not be null
    
    # Relationships with other tables
    # Establish a one-to-many relationship with the 'Car' model; a make, model, and year can be associated with multiple cars
    cars = db.relationship("Car", back_populates="make_model_year")  

    # String representation of the MakeModelYear object for debugging purposes
    def __repr__(self):
        return f"<MakeModelYear {self.make} {self.model}, Year: {self.year}>"

# Define the MakeModelYearSchema using Marshmallow for serialization and deserialization
class MakeModelYearSchema(ma.Schema):
    # Nested schema for serializing relationships with the 'Car' model
    cars = fields.List(fields.Nested('CarSchema', exclude=["make_model_year"]))  # Use 'CarSchema' to represent associated cars, excluding 'make_model_year' to prevent circular reference
    
    class Meta:
        # Fields to include in the serialized output; defines how the data will be structured when the make, model, year is converted to JSON
        fields = ("make_model_year_id", "make", "model", "year", "cars")
