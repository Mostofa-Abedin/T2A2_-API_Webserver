# Import standard library modules
from datetime import datetime  # For timestamping

# Import third-party modules
from flask import Blueprint, jsonify, request  # Flask functions
from flask_jwt_extended import jwt_required, get_jwt_identity  # JWT authentication
from marshmallow import ValidationError  # For input validation errors

# Import local modules
from init import db  # Database instance
from models.car_transaction import CarTransaction, CarTransactionSchema  # CarTransaction model and schema
from models.user import User  # User model
from models.car import Car  # Car model
from models.listing import Listing  # Listing model

# Create a Blueprint for car transaction routes
car_transactions_bp = Blueprint('car_transactions', __name__)

# Route to get all car transactions
@car_transactions_bp.route('/car-transactions', methods=['GET'])
@jwt_required()
def get_car_transactions():
    # Get current user ID from the JWT token
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    # Check if the user exists
    if not user:
        return jsonify({'error': 'User not found.'}), 404

    try:
        # Retrieve all car transactions from the database
        transactions = CarTransaction.query.all()

        # Serialize the transactions using the CarTransactionSchema
        data = CarTransactionSchema(many=True).dump(transactions)

        # Return the serialized data as JSON
        return jsonify(data), 200
    except Exception:
        # Return a generic error message to the client
        return jsonify({'error': 'An internal server error occurred.'}), 500

# Route to get a specific car transaction by ID
@car_transactions_bp.route('/car-transactions/<int:id>', methods=['GET'])
@jwt_required()
def get_car_transaction(id):
    # Get current user ID from the JWT token
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    # Check if the user exists
    if not user:
        return jsonify({'error': 'User not found.'}), 404

    try:
        # Retrieve the car transaction by ID
        transaction = CarTransaction.query.get(id)

        # Check if the transaction exists
        if not transaction:
            return jsonify({'error': 'Car transaction not found.'}), 404

        # Serialize the transaction using the CarTransactionSchema
        data = CarTransactionSchema().dump(transaction)

        # Return the serialized data as JSON
        return jsonify(data), 200
    except Exception:
        # Return a generic error message to the client
        return jsonify({'error': 'An internal server error occurred.'}), 500

# Route to create a new car transaction
@car_transactions_bp.route('/car-transactions', methods=['POST'])
@jwt_required()
def create_car_transaction():
    # Get current user ID from the JWT token
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    # Check if the user exists
    if not user:
        return jsonify({'error': 'User not found.'}), 404

    try:
        # Load input data from the request
        data = request.get_json()

        # Validate required fields
        required_fields = ['car_id', 'amount']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f"'{field}' is a required field."}), 400

        # Check if the car exists
        car = Car.query.get(data['car_id'])
        if not car:
            return jsonify({'error': 'Invalid car ID provided.'}), 400

        # Retrieve the listing associated with the car where the listing status is 'available'
        listing = Listing.query.filter_by(
            car_id=car.car_id,
            listing_status='available'
        ).first()
        if not listing:
            return jsonify({'error': 'Car is not available for purchase.'}), 400

        # Check if the amount matches the car's price
        try:
            amount = float(data['amount'])
        except ValueError:
            return jsonify({'error': 'Amount must be a number.'}), 400

        if amount != car.price:
            return jsonify({'error': 'Amount does not match the car price.'}), 400

        # Create a new CarTransaction instance
        new_transaction = CarTransaction(
            transaction_date=datetime.utcnow(),
            amount=amount,
            car_id=data['car_id'],
            buyer_id=current_user_id
        )

        # Update the listing status to 'sold'
        listing.listing_status = 'sold'

        # Add and commit the new transaction to the database
        db.session.add(new_transaction)
        db.session.commit()

        # Return the new transaction as JSON
        return CarTransactionSchema().dump(new_transaction), 201
    except Exception:
        # Return a generic error message to the client
        return jsonify({'error': 'An internal server error occurred.'}), 500
