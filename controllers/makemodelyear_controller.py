# Import necessary modules and functions
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.makemodelyear import MakeModelYear, MakeModelYearSchema
from models.user import User

# Create a Blueprint for make, model, and year endpoints
makemodelyear_bp = Blueprint('makemodelyear', __name__)

# Route to get all make, model, and year combinations
@makemodelyear_bp.route('/makemodelyear', methods=['GET'])
def get_makemodelyears():
    try:
        # Query all MakeModelYear entries from the database
        makemodelyears = MakeModelYear.query.all()

        # Serialize the data using the MakeModelYearSchema
        data = MakeModelYearSchema(many=True).dump(makemodelyears)

        # Return the serialized data as JSON with a 200 OK status
        return jsonify(data), 200
    except Exception:
        # Return a generic error message with a 500 Internal Server Error status
        return jsonify({'error': 'An internal server error occurred.'}), 500

# Route to get a specific make, model, and year by ID
@makemodelyear_bp.route('/makemodelyear/<int:id>', methods=['GET'])
def get_makemodelyear(id):
    try:
        # Query the MakeModelYear entry with the given ID
        makemodelyear = MakeModelYear.query.get(id)

        # Check if the entry exists
        if makemodelyear is None:
            # Return a 404 Not Found error if the entry doesn't exist
            return jsonify({'error': 'Make, model, and year combination not found.'}), 404

        # Serialize the data using the MakeModelYearSchema
        data = MakeModelYearSchema().dump(makemodelyear)

        # Return the serialized data as JSON with a 200 OK status
        return jsonify(data), 200
    except Exception:
        # Return a generic error message with a 500 Internal Server Error status
        return jsonify({'error': 'An internal server error occurred.'}), 500

# Route to create a new make, model, and year combination
@makemodelyear_bp.route('/makemodelyear', methods=['POST'])
@jwt_required()
def create_makemodelyear():
    # Get current user ID from the JWT token
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    # Check if the user exists and is an admin
    if not user or not user.is_admin:
        return jsonify({'error': 'You do not have permission to perform this action.'}), 403

    try:
        # Load input data from the request
        data = request.get_json()

        # Check if all required fields are provided
        if not data.get('make') or not data.get('model') or not data.get('year'):
            return jsonify({'error': 'Make, model, and year are required fields.'}), 400

        # Validate that make and model are strings
        if not isinstance(data['make'], str) or not isinstance(data['model'], str):
            return jsonify({'error': 'Make and model must be strings.'}), 400

        # Validate that year is an integer
        if not isinstance(data['year'], int):
            return jsonify({'error': 'Year must be an integer.'}), 400

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
    except Exception:
        # Return a generic error message with a 500 Internal Server Error status
        return jsonify({'error': 'An internal server error occurred.'}), 500

# Route to update an existing make, model, and year combination
@makemodelyear_bp.route('/makemodelyear/<int:id>', methods=['PUT'])
@jwt_required()
def update_makemodelyear(id):
    # Get current user ID from the JWT token
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    # Check if the user exists and is an admin
    if not user or not user.is_admin:
        return jsonify({'error': 'You do not have permission to perform this action.'}), 403

    try:
        # Fetch the existing MakeModelYear entry by ID
        makemodelyear = MakeModelYear.query.get(id)

        # Check if the entry exists
        if not makemodelyear:
            return jsonify({'error': 'Make, model, and year combination not found.'}), 404

        # Load input data (partial updates allowed)
        data = request.get_json()

        # Update fields if they are provided in the request
        if 'make' in data:
            if not isinstance(data['make'], str):
                return jsonify({'error': 'Make must be a string.'}), 400
            makemodelyear.make = data['make']
        if 'model' in data:
            if not isinstance(data['model'], str):
                return jsonify({'error': 'Model must be a string.'}), 400
            makemodelyear.model = data['model']
        if 'year' in data:
            if not isinstance(data['year'], int):
                return jsonify({'error': 'Year must be an integer.'}), 400
            makemodelyear.year = data['year']

        # Commit the changes to the database
        db.session.commit()

        # Return the updated entry as JSON with a 200 OK status
        return MakeModelYearSchema().dump(makemodelyear), 200
    except Exception:
        # Return a generic error message with a 500 Internal Server Error status
        return jsonify({'error': 'An internal server error occurred.'}), 500

# Route to delete a make, model, and year combination
@makemodelyear_bp.route('/makemodelyear/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_makemodelyear(id):
    # Get current user ID from the JWT token
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    # Check if the user exists and is an admin
    if not user or not user.is_admin:
        return jsonify({'error': 'You do not have permission to perform this action.'}), 403

    try:
        # Fetch the existing MakeModelYear entry by ID
        makemodelyear = MakeModelYear.query.get(id)

        # Check if the entry exists
        if not makemodelyear:
            return jsonify({'error': 'Make, model, and year combination not found.'}), 404

        # Check if any cars are associated with this MakeModelYear
        if makemodelyear.cars:
            return jsonify({'error': 'Cannot delete. Please remove associated cars first.'}), 400

        # Proceed to delete the MakeModelYear entry
        db.session.delete(makemodelyear)
        db.session.commit()

        # Return a success message with a 200 OK status
        return jsonify({'message': 'Make, model, and year combination deleted successfully.'}), 200
    except Exception:
        # Return a generic error message with a 500 Internal Server Error status
        return jsonify({'error': 'An internal server error occurred.'}), 500
