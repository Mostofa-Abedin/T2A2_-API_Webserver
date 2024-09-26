# Import the SQLAlchemy database instance (db) and Marshmallow (ma) for serialization
from init import db, ma

# Import fields from Marshmallow for schema definitions
from marshmallow import fields


# Define the MakeModelYear model representing the 'makemodelyear' table
class MakeModelYear(db.Model):
    __tablename__ = "makemodelyear"  # Specify the table name

    # Define the columns/attributes
    make_model_year_id = db.Column(
        db.Integer, primary_key=True
    )  # Primary key for each make, model, and year combination
    make = db.Column(
        db.String(100), nullable=False
    )  # Car make (e.g., Toyota), required
    model = db.Column(
        db.String(100), nullable=False
    )  # Car model (e.g., Corolla), required
    year = db.Column(
        db.Integer, nullable=False
    )  # Year of the car's make, required

    # Relationship with the Car model
    cars = db.relationship(
        "Car",
        back_populates="make_model_year"
    )  # A make-model-year can have multiple cars

    def __repr__(self):
        # String representation for debugging
        return f"<MakeModelYear {self.make} {self.model}, Year: {self.year}>"

# Define the MakeModelYearSchema for serialization/deserialization
class MakeModelYearSchema(ma.Schema):
    # Nested field for related cars
    cars = fields.List(
        fields.Nested('CarSchema', exclude=["make_model_year"])
    )  # Exclude 'make_model_year' to prevent recursion

    class Meta:
        # Fields to include in the serialized output
        fields = (
            "make_model_year_id", "make", "model", "year", "cars"
        )
