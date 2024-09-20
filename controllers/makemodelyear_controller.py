from flask import Blueprint, jsonify
from init import db
from models.makemodelyear import MakeModelYear, MakeModelYearSchema

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
def create_makemodelyear():
    pass  # Placeholder for creating a new make/model/year

# Route to update a make, model, and year
@makemodelyear_bp.route('/makemodelyear/<int:id>', methods=['PUT'])
def update_makemodelyear(id):
    pass  # Placeholder for updating a make/model/year

# Route to delete a make, model, and year
@makemodelyear_bp.route('/makemodelyear/<int:id>', methods=['DELETE'])
def delete_makemodelyear(id):
    pass  # Placeholder for deleting a make/model/year
