from flask import Blueprint, jsonify, request  # Import necessary Flask functions
from flask_jwt_extended import jwt_required, get_jwt_identity  # Import JWT functions for authentication
from models.listing import Listing, ListingSchema  # Import the Listing model and schema
from models.user import User  # Import the User model
from models.car import Car  # Import the Car model
from init import db  # Import the database instance
from datetime import datetime  # Import datetime for timestamping
from marshmallow import ValidationError  # Import ValidationError for error handling

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
@listings_bp.route('/listings', methods=['POST'])
@jwt_required()
def create_listing():
 
    # Get current user ID from the JWT token
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    # Check if user exists
    if not user:
        return jsonify({'error': 'User not found.'}), 404

    try:
        # Load and validate input data
        data = ListingSchema().load(request.get_json())

        # Access 'car_id' using subscript notation
        car = Car.query.get(data['car_id'])
        if not car:
            return jsonify({'error': 'Invalid car_id.'}), 400

        # Check if the car is already listed
        existing_listing = Listing.query.filter_by(car_id=data['car_id']).first()
        if existing_listing:
            return jsonify({'error': 'This car is already listed.'}), 400

        # Create a new Listing instance
        new_listing = Listing(
            car_id=data['car_id'],
            user_id=current_user_id
            # 'date_posted' and 'listing_status' are set by default in the model
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
@jwt_required()
def update_listing(id):
   
    # Get current user ID from the JWT token
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    try:
        # Retrieve the listing by ID
        listing = Listing.query.get(id)

        # Check if the listing exists
        if not listing:
            return jsonify({'error': 'Listing not found.'}), 404

        # Check if the current user is the owner or an admin
        if listing.user_id != current_user_id and not current_user.is_admin:
            return jsonify({'error': 'Unauthorized access.'}), 403

        # Load and validate input data
        data = request.get_json()
        # Only allow updating certain fields (e.g., listing_status)
        if 'listing_status' in data:
            # Validate the new status
            if data['listing_status'] not in ['available', 'sold', 'pending']:
                return jsonify({'error': 'Invalid listing status.'}), 400
            listing.listing_status = data['listing_status']

        # Commit changes to the database
        db.session.commit()

        # Return the updated listing as JSON
        return ListingSchema().dump(listing), 200

    except Exception as e:
        # Handle any other exceptions
        return jsonify({'error': str(e)}), 500

# Route to delete a listing
@listings_bp.route('/listings/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_listing(id):
   
    # Get current user ID from the JWT token
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    try:
        # Retrieve the listing by ID
        listing = Listing.query.get(id)

        # Check if the listing exists
        if not listing:
            return jsonify({'error': 'Listing not found.'}), 404

        # Check if the current user is the owner or an admin
        if listing.user_id != current_user_id and not current_user.is_admin:
            return jsonify({'error': 'Unauthorized access.'}), 403

        # Delete the listing from the database
        db.session.delete(listing)
        db.session.commit()

        # Return a success message.
        return jsonify({'message': 'Listing deleted successfully.'}), 200

    except Exception as e:
        # Handle any other exceptions
        return jsonify({'error': str(e)}), 500