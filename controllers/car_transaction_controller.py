from flask import Blueprint, jsonify, request  # Import necessary Flask functions
from flask_jwt_extended import jwt_required, get_jwt_identity  # Import JWT functions for authentication
from models.car_transaction import CarTransaction, CarTransactionSchema  # Import the CarTransaction model and schema
from models.user import User  # Import the User model
from models.car import Car  # Import the Car model
from init import db  # Import the database instance
from datetime import datetime  # Import datetime for timestamping
from marshmallow import ValidationError  # Import ValidationError for error handling
from models.listing import Listing

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
@jwt_required()
def get_car_transaction(id):
    
    try:
        # Query the CarTransaction entry by ID from the database
        transaction = CarTransaction.query.get(id)

        # Check if the transaction exists
        if not transaction:
            return jsonify({'error': 'Car transaction not found.'}), 404

        # Serialize the data using the CarTransactionSchema
        transaction_schema = CarTransactionSchema()
        data = transaction_schema.dump(transaction)

        # Return the serialized data as JSON with a 200 OK status
        return jsonify(data), 200
    except Exception as e:
        # Handle any exceptions
        return jsonify({'error': str(e)}), 500
    
# Route to create a new car transaction
@car_transactions_bp.route('/car-transactions', methods=['POST'])
@jwt_required()
def create_car_transaction():
    
    # Get current user ID from the JWT token
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    # Check if user exists
    if not user:
        return jsonify({'error': 'User not found.'}), 404

    try:
        # Load and validate input data
        data = request.get_json()

        # Validate required fields
        required_fields = ['car_id', 'amount']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f"'{field}' is required."}), 400

        # Check if the car exists
        car = Car.query.get(data['car_id'])
        if not car:
            return jsonify({'error': 'Invalid car_id.'}), 400

        # Query the listing associated with the car where the listing status is 'available'
        listing = Listing.query.filter_by(car_id=car.car_id, listing_status='available').first()
        if not listing:
            return jsonify({'error': 'Car is not available for purchase.'}), 400

        # Check if the amount matches the car's price
        if data['amount'] != car.price:
            return jsonify({'error': 'Amount does not match car price.'}), 400

        # Create a new CarTransaction instance
        new_transaction = CarTransaction(
            transaction_date=datetime.utcnow(),
            amount=data['amount'],
            car_id=data['car_id'],
            buyer_id=current_user_id
        )

        # Update listing status to 'sold'
        listing.listing_status = 'sold'

        # Add and commit the new transaction to the database
        db.session.add(new_transaction)
        db.session.commit()

        # Return the new transaction as JSON with a 201 Created status
        return CarTransactionSchema().dump(new_transaction), 201
    except ValidationError as ve:
        # Return validation errors with a 400 Bad Request status
        return jsonify({'errors': ve.messages}), 400
    except Exception as e:
        # Handle any other exceptions
        return jsonify({'error': str(e)}), 500
