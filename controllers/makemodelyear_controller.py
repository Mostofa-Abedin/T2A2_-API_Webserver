from flask import Blueprint

# Create a Blueprint for make, model, and year combinations
makemodelyear_bp = Blueprint('makemodelyear', __name__)

# Route to get all make, model, and year combinations
@makemodelyear_bp.route('/makemodelyear', methods=['GET'])
def get_makemodelyears():
    pass  # Placeholder for getting all make/model/years

# Route to get a specific make, model, and year by ID
@makemodelyear_bp.route('/makemodelyear/<int:id>', methods=['GET'])
def get_makemodelyear(id):
    pass  # Placeholder for getting a make/model/year by ID

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
