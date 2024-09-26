# Import the SQLAlchemy database instance (db) and Marshmallow (ma)
from init import db, ma

# Import fields from Marshmallow for schema definitions
from marshmallow import fields

# Define the CarTransaction model representing the 'car_transactions' table
class CarTransaction(db.Model):
    __tablename__ = "car_transactions"  # Specify the table name

    # Primary key, unique identifier for each transaction
    transaction_id = db.Column(db.Integer, primary_key=True)
    # Date of the transaction, required
    transaction_date = db.Column(db.Date, nullable=False)
    # Transaction amount, required
    amount = db.Column(db.Float, nullable=False)

    # Foreign key referencing 'car_id' in the 'cars' table
    car_id = db.Column(
        db.Integer,
        db.ForeignKey("cars.car_id"),
        nullable=False
    )
    # Foreign key referencing 'user_id' in the 'users' table
    buyer_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id"),
        nullable=False
    )

    # Relationship to the User model (buyer)
    user = db.relationship(
        "User",
        back_populates="car_transactions"
    )
    # Relationship to the Car model
    car = db.relationship(
        "Car",
        back_populates="car_transactions"
    )

    def __repr__(self):
        # String representation for debugging
        return f"<CarTransaction {self.transaction_id}, Amount: {self.amount}>"

# Define the CarTransactionSchema for serialization/deserialization
class CarTransactionSchema(ma.Schema):
    # Nested field for the related user (buyer)
    user = fields.Nested(
        'UserSchema',
        exclude=["car_transactions", "listings"]
    )
    # Nested field for the related car
    car = fields.Nested(
        'CarSchema',
        exclude=["car_transactions", "listings"]
    )

    class Meta:
        # Fields to include in the serialized output
        fields = (
            "transaction_id", "car_id", "buyer_id",
            "transaction_date", "amount", "user", "car"
        )
