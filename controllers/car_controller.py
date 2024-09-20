from flask import Blueprint, jsonify
from models.car import Car, CarSchema
from init import db

# Create a Blueprint for car management
cars_bp = Blueprint('cars', __name__)

# Route to get all cars
@cars_bp.route('/cars', methods=['GET'])
def get_cars():
    try:
        # Query all Car entries from the database
        cars = Car.query.all()

        # Serialize the data using the CarSchema
        car_schema = CarSchema(many=True)
        data = car_schema.dump(cars)

        # Return the serialized data as JSON with a 200 OK status
        return jsonify(data), 200
    except Exception as e:
        # If an error occurs, return an error message with a 500 Internal Server Error status
        return jsonify({'error': str(e)}), 500

# Route to get a specific car by ID
@cars_bp.route('/cars/<int:id>', methods=['GET'])
def get_car(id):
    pass  # Placeholder for getting a car by ID

# Route to create a new car
@cars_bp.route('/cars', methods=['POST'])
def create_car():
    pass  # Placeholder for creating a new car

# Route to update a car
@cars_bp.route('/cars/<int:id>', methods=['PUT'])
def update_car(id):
    pass  # Placeholder for updating a car

# Route to delete a car
@cars_bp.route('/cars/<int:id>', methods=['DELETE'])
def delete_car(id):
    pass  # Placeholder for deleting a car
