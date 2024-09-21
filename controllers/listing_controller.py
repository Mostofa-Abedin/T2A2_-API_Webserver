from flask import Blueprint, jsonify
from models.listing import Listing, ListingSchema
from init import db

# Create a Blueprint for listings
listings_bp = Blueprint('listings', __name__)

# Route to get all listings
@listings_bp.route('/listings', methods=['GET'])
def get_listings():
  
    try:
        # Query all Listing entries from the database
        listings = Listing.query.all()

        # Serialize the data using the ListingSchema
        listing_schema = ListingSchema(many=True)
        data = listing_schema.dump(listings)

        # Return the serialized data as JSON with a 200 OK status
        return jsonify(data), 200
    except Exception as e:
        # If an error occurs, return an error message with a 500 Internal Server Error status
        return jsonify({'error': str(e)}), 500

# Route to get a specific listing by ID
@listings_bp.route('/listings/<int:id>', methods=['GET'])
def get_listing(id):
    
    try:
        # Query the Listing entry by ID from the database.
        listing = Listing.query.get(id)

        # Check if the listing exists
        if not listing:
            return jsonify({'error': 'Listing not found.'}), 404

        # Serialize the data using the ListingSchema
        listing_schema = ListingSchema()
        data = listing_schema.dump(listing)

        # Return the serialized data as JSON with a 200 OK status
        return jsonify(data), 200
    except Exception as e:
        # If an error occurs, return an error message with a 500 Internal Server Error status
        return jsonify({'error': str(e)}), 500

# Route to create a new listing
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.listing import Listing, ListingSchema
from models.user import User
from models.car import Car
from init import db
from datetime import datetime
from marshmallow import ValidationError

# Create a Blueprint for listings
listings_bp = Blueprint('listings', __name__)

# Existing routes...

# Route to create a new listing
@listings_bp.route('/listings', methods=['POST'])
@jwt_required()
def create_listing():
    """
    Create a new listing entry.

    Requires:
        - Authenticated user.

    Returns:
        - The newly created listing as JSON.
        - Appropriate error messages and status codes if the operation fails.
    """
    # Get current user ID from the JWT token
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    # Check if user exists
    if not user:
        return jsonify({'error': 'User not found.'}), 404

    try:
        # Load and validate input data
        data = ListingSchema().load(request.get_json())

        # Check if the car exists
        car = Car.query.get(data['car_id'])
        if not car:
            return jsonify({'error': 'Invalid car_id.'}), 400

        # Check if the car is already listed
        existing_listing = Listing.query.filter_by(car_id=data['car_id']).first()
        if existing_listing:
            return jsonify({'error': 'This car is already listed.'}), 400

        # Create a new Listing instance
        new_listing = Listing(
            date_created=datetime.utcnow(),
            status='available',
            car_id=data['car_id'],
            user_id=current_user_id
        )

        # Add and commit the new listing to the database
        db.session.add(new_listing)
        db.session.commit()

        # Return the new listing as JSON with a 201 Created status
        return ListingSchema().dump(new_listing), 201
    except ValidationError as ve:
        # Return validation errors with a 400 Bad Request status
        return jsonify({'errors': ve.messages}), 400
    except Exception as e:
        # Handle any other exceptions
        return jsonify({'error': str(e)}), 500


# Route to update a listing
@listings_bp.route('/listings/<int:id>', methods=['PUT'])
def update_listing(id):
    pass  # Placeholder for updating a listing

# Route to delete a listing
@listings_bp.route('/listings/<int:id>', methods=['DELETE'])
def delete_listing(id):
    pass  # Placeholder for deleting a listing