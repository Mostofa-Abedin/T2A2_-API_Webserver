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
        # Query the Listing entry by ID from the database
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
def create_listing():
    pass  # Placeholder for creating a new listing

# Route to update a listing
@listings_bp.route('/listings/<int:id>', methods=['PUT'])
def update_listing(id):
    pass  # Placeholder for updating a listing

# Route to delete a listing
@listings_bp.route('/listings/<int:id>', methods=['DELETE'])
def delete_listing(id):
    pass  # Placeholder for deleting a listing