from init import db, ma  # Import the SQLAlchemy database instance (db) and Marshmallow (ma) for serialization
from marshmallow import fields  # Import fields from Marshmallow for schema definitions

# Define the Transaction model, representing the 'transactions' table in the database
class Transaction(db.Model):
    __tablename__ = "transactions"  # Explicitly specify the table name as 'transactions'
    
    # Attributes (columns) of the table
    transaction_id = db.Column(db.Integer, primary_key=True)  # Primary key, unique identifier for each transaction
    transaction_date = db.Column(db.Date, nullable=False)  # Date of the transaction, using 'Date' type, must not be null
    amount = db.Column(db.Float, nullable=False)  # Transaction amount, stored as a floating-point number, must not be null

    # Foreign keys to create relationships with other tables
    car_id = db.Column(db.Integer, db.ForeignKey("cars.car_id"), nullable=False)  # Foreign key referencing 'car_id' in the 'cars' table
    buyer_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)  # Foreign key referencing 'user_id' in the 'users' table

    # Relationships with other tables
    # Establish a many-to-one relationship with the 'User' model; a user can be involved in multiple transactions
    user = db.relationship("User", back_populates="transactions")  
    # Establish a many-to-one relationship with the 'Car' model; a car can be involved in multiple transactions
    car = db.relationship("Car", back_populates="transactions")  

    # String representation of the Transaction object for debugging purposes
    def __repr__(self):
        return f"<Transaction {self.transaction_id}, Amount: {self.amount}>"

# Define the TransactionSchema using Marshmallow for serialization and deserialization
class TransactionSchema(ma.Schema):
    # Nested schemas for serializing relationships with the 'User' and 'Car' models
    user = fields.Nested('UserSchema', exclude=["transactions"])  # Use 'UserSchema' to represent the buyer, exclude the 'transactions' field to prevent circular reference
    car = fields.Nested('CarSchema', exclude=["transactions"])  # Use 'CarSchema' to represent the car, exclude the 'transactions' field to prevent circular reference

    class Meta:
        # Fields to include in the serialized output; defines how the data will be structured when the transaction is converted to JSON
        fields = ("transaction_id", "car_id", "buyer_id", "transaction_date", "amount")
