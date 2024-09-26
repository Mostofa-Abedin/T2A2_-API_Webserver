# Import standard library modules
from datetime import datetime  # For timestamping

# Import third-party modules
from flask import Blueprint, jsonify, request  # Flask functions
from flask_jwt_extended import jwt_required, get_jwt_identity  # JWT authentication
from marshmallow import ValidationError  # For input validation errors

# Import local modules
from init import db  # Database instance
from models.listing import Listing, ListingSchema  # Listing model and schema
from models.user import User  # User model
from models.car import Car  # Car model

# Create a Blueprint for listing routes
listings_bp = Blueprint('listings', __name__)

# Route to get all listings
@listings_bp.route('/listings', methods=['GET'])
def get_listings():
    try:
        # Retrieve all listings from the database
        listings = Listing.query.all()

        # Serialize the listings using the ListingSchema
        data = ListingSchema(many=True).dump(listings)

        # Return the serialized data as JSON
        return jsonify(data), 200
    except Exception:
        # Return a generic error message to the client
        return jsonify({'error': 'An internal server error occurred.'}), 500

# Route to get a specific listing by ID
@listings_bp.route('/listings/<int:id>', methods=['GET'])
def get_listing(id):
    try:
        # Retrieve the listing by ID
        listing = Listing.query.get(id)

        # Check if the listing exists
        if not listing:
            return jsonify({'error': 'Listing not found.'}), 404

        # Serialize the listing using the ListingSchema
        data = ListingSchema().dump(listing)

        # Return the serialized data as JSON
        return jsonify(data), 200
    except Exception:
        # Return a generic error message to the client
        return jsonify({'error': 'An internal server error occurred.'}), 500

# Route to create a new listing
@listings_bp.route('/listings', methods=['POST'])
@jwt_required()
def create_listing():
    # Get the current user's ID from the JWT token
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    # Check if the user exists
    if not user:
        return jsonify({'error': 'User not found.'}), 404

    try:
        # Load and validate input data using the ListingSchema
        data = ListingSchema().load(request.get_json())

        # Retrieve the car by 'car_id'
        car = Car.query.get(data['car_id'])
        if not car:
            return jsonify({'error': 'Invalid car ID provided.'}), 400

        # Check if the car is already listed
        existing_listing = Listing.query.filter_by(car_id=data['car_id']).first()
        if existing_listing:
            return jsonify({'error': 'This car is already listed.'}), 400

        # Create a new Listing instance
        new_listing = Listing(
            car_id=data['car_id'],
            user_id=current_user_id
            # 'date_posted' and 'listing_status' are set by default
        )

        # Add and commit the new listing to the database
        db.session.add(new_listing)
        db.session.commit()

        # Return the new listing as JSON
        return ListingSchema().dump(new_listing), 201
    except ValidationError as ve:
        # Return validation errors to the client
        return jsonify({'errors': ve.messages}), 400
    except Exception:
        # Return a generic error message to the client
        return jsonify({'error': 'An internal server error occurred.'}), 500

# Route to update an existing listing
@listings_bp.route('/listings/<int:id>', methods=['PUT'])
@jwt_required()
def update_listing(id):
    # Get the current user's ID from the JWT token
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    # Check if the user exists
    if not current_user:
        return jsonify({'error': 'User not found.'}), 404

    try:
        # Retrieve the listing by ID
        listing = Listing.query.get(id)

        # Check if the listing exists
        if not listing:
            return jsonify({'error': 'Listing not found.'}), 404

        # Check if the current user is the owner or an admin
        if listing.user_id != current_user_id and not current_user.is_admin:
            return jsonify({'error': 'You do not have permission to update this listing.'}), 403

        # Load input data
        data = request.get_json()

        # Only allow updating the 'listing_status' field
        if 'listing_status' in data:
            # Validate the new status
            if data['listing_status'] not in ['available', 'sold']:
                return jsonify({'error': 'Invalid listing status provided.'}), 400
            listing.listing_status = data['listing_status']

        # Commit changes to the database
        db.session.commit()

        # Return the updated listing as JSON
        return ListingSchema().dump(listing), 200
    except Exception:
        # Return a generic error message to the client
        return jsonify({'error': 'An internal server error occurred.'}), 500

# Route to delete a listing
@listings_bp.route('/listings/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_listing(id):
    # Get the current user's ID from the JWT token
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    # Check if the user exists
    if not current_user:
        return jsonify({'error': 'User not found.'}), 404

    try:
        # Retrieve the listing by ID
        listing = Listing.query.get(id)

        # Check if the listing exists
        if not listing:
            return jsonify({'error': 'Listing not found.'}), 404

        # Check if the current user is the owner or an admin
        if listing.user_id != current_user_id and not current_user.is_admin:
            return jsonify({'error': 'You do not have permission to delete this listing.'}), 403

        # Delete the listing from the database
        db.session.delete(listing)
        db.session.commit()

        # Return a success message
        return jsonify({'message': 'Listing deleted successfully.'}), 200
    except Exception:
        # Return a generic error message to the client
        return jsonify({'error': 'An internal server error occurred.'}), 500
