from flask import Blueprint, jsonify, request
from init import db
from models.makemodelyear import MakeModelYear, MakeModelYearSchema
from models.user import User

from flask_jwt_extended import jwt_required, get_jwt_identity

# Create a Blueprint for make, model, and year combinations
makemodelyear_bp = Blueprint('makemodelyear', __name__)

# Route to get all make, model, and year combinations
@makemodelyear_bp.route('/makemodelyear', methods=['GET'])
def get_makemodelyears():
    try:
        # Query all MakeModelYear entries from the database
        makemodelyears = MakeModelYear.query.all()
        
        # Serialize the data using the MakeModelYearSchema
        makemodelyear_schema = MakeModelYearSchema(many=True)
        data = makemodelyear_schema.dump(makemodelyears)
        
        # Return the serialized data as JSON with a 200 OK status
        return jsonify(data), 200
    except Exception as e:
        # If an error occurs, return an error message with a 500 Internal Server Error status
        return jsonify({'error': str(e)}), 500

# Route to get a specific make, model, and year by ID
@makemodelyear_bp.route('/makemodelyear/<int:id>', methods=['GET'])
def get_makemodelyear(id):
    try:
        # Query the MakeModelYear entry with the given ID
        makemodelyear = MakeModelYear.query.get(id)
        
        # Check if the entry exists
        if makemodelyear is None:
            # Return a 404 Not Found error if the entry doesn't exist
            return jsonify({'error': 'MakeModelYear not found.'}), 404
        
        # Serialize the data using the MakeModelYearSchema
        makemodelyear_schema = MakeModelYearSchema()
        data = makemodelyear_schema.dump(makemodelyear)
        
        # Return the serialized data as JSON with a 200 OK status
        return jsonify(data), 200
    except Exception as e:
        # If an error occurs, return an error message with a 500 Internal Server Error status
        return jsonify({'error': str(e)}), 500
    
# Route to create a new make, model, and year
@makemodelyear_bp.route('/makemodelyear', methods=['POST'])
@jwt_required()
def create_makemodelyear():
    
    # Get current user ID from the JWT token
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    # Check if user exists and is an admin
    if not user or not user.is_admin:
        return jsonify({'error': 'You do not have permission to perform this action.'}), 403

    try:
        # Load and validate input data
        data = MakeModelYearSchema().load(request.get_json())

        # Check if the combination already exists
        existing_entry = MakeModelYear.query.filter_by(
            make=data['make'],
            model=data['model'],
            year=data['year']
        ).first()
        if existing_entry:
            return jsonify({'error': 'This make, model, and year combination already exists.'}), 400

        # Create a new MakeModelYear instance
        new_makemodelyear = MakeModelYear(
            make=data['make'],
            model=data['model'],
            year=data['year']
        )

        # Add and commit the new entry to the database
        db.session.add(new_makemodelyear)
        db.session.commit()

        # Return the new entry as JSON with a 201 Created status
        return MakeModelYearSchema().dump(new_makemodelyear), 201
    except Exception as e:
        # Handle any exceptions and return an error message
        return jsonify({'error': str(e)}), 500

# Route to update a make, model, and year
@makemodelyear_bp.route('/makemodelyear/<int:id>', methods=['PUT'])
def update_makemodelyear(id):
    pass  # Placeholder for updating a make/model/year

# Route to delete a make, model, and year
@makemodelyear_bp.route('/makemodelyear/<int:id>', methods=['DELETE'])
def delete_makemodelyear(id):
    pass  # Placeholder for deleting a make/model/year
