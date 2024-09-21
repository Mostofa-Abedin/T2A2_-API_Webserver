from flask import Blueprint, jsonify, request  # Import necessary Flask functions
from flask_jwt_extended import jwt_required, get_jwt_identity  # Import JWT functions for authentication
from models.car_transaction import CarTransaction, CarTransactionSchema  # Import the CarTransaction model and schema
from models.user import User  # Import the User model
from models.car import Car  # Import the Car model
from init import db  # Import the database instance
from datetime import datetime  # Import datetime for timestamping
from marshmallow import ValidationError  # Import ValidationError for error handling

# Create a Blueprint for car transactions
car_transactions_bp = Blueprint('car_transactions', __name__)

# Route to get all car transactions
@car_transactions_bp.route('/car-transactions', methods=['GET'])
@jwt_required()
def get_car_transactions():
    
    try:
        # Query all CarTransaction entries from the database
        transactions = CarTransaction.query.all()

        # Serialize the data using the CarTransactionSchema
        transaction_schema = CarTransactionSchema(many=True)
        data = transaction_schema.dump(transactions)

        # Return the serialized data as JSON with a 200 OK status
        return jsonify(data), 200
    except Exception as e:
        # Handle any exceptions
        return jsonify({'error': str(e)}), 500

# Route to get a specific car transaction by ID
@car_transactions_bp.route('/car-transactions/<int:id>', methods=['GET'])
def get_car_transaction(id):
    pass  # Placeholder for getting a car transaction by ID

# Route to create a new car transaction
@car_transactions_bp.route('/car-transactions', methods=['POST'])
def create_car_transaction():
    pass  # Placeholder for creating a new car transaction
