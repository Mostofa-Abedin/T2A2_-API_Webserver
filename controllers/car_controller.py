from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.car import Car, CarSchema
from models.user import User
from models.makemodelyear import MakeModelYear
from init import db

# Create a Blueprint for car management
cars_bp = Blueprint('cars', __name__)

# Route to get all cars
@cars_bp.route('/cars', methods=['GET'])
def get_cars():
    try:
        # Query all Car entries from the database.
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
    
    try:
        # Query the Car entry by ID from the database
        car = Car.query.get(id)

        # Check if the car exists
        if not car:
            return jsonify({'error': 'Car not found.'}), 404

        # Serialize the data using the CarSchema
        car_schema = CarSchema()
        data = car_schema.dump(car)

        # Return the serialized data as JSON with a 200 OK status
        return jsonify(data), 200
    except Exception as e:
        # If an error occurs, return an error message with a 500 Internal Server Error status
        return jsonify({'error': str(e)}), 500

# Route to create a new car
@cars_bp.route('/cars', methods=['POST'])
@jwt_required()
def create_car():
   
    # Get current user ID from the JWT token
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    # Check if user exists and is an admin
    if not user or not user.is_admin:
        return jsonify({'error': 'You do not have permission to perform this action.'}), 403

    try:
        # Load and validate input data
        data = CarSchema().load(request.get_json())

        # Check if the make_model_year_id exists
        make_model_year = MakeModelYear.query.get(data['make_model_year_id'])
        if not make_model_year:
            return jsonify({'error': 'Invalid make_model_year_id.'}), 400

        # Create a new Car instance
        new_car = Car(
            mileage=data['mileage'],
            price=data['price'],
            condition=data['condition'],
            description=data.get('description'),
            image_url=data.get('image_url'),
            make_model_year_id=data['make_model_year_id']
        )

        # Add and commit the new entry to the database
        db.session.add(new_car)
        db.session.commit()

        # Return the new car as JSON with a 201 Created status
        return CarSchema().dump(new_car), 201
    except Exception as e:
        # Handle any exceptions and return an error message
        return jsonify({'error': str(e)}), 500

# Route to update a car
@cars_bp.route('/cars/<int:id>', methods=['PUT'])
@jwt_required()
def update_car(id):
    
    # Get current user ID from the JWT token
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    # Check if user exists and is an admin
    if not user or not user.is_admin:
        return jsonify({'error': 'You do not have permission to perform this action.'}), 403

    try:
        # Fetch the existing car by ID
        car = Car.query.get(id)

        # Check if the car exists
        if not car:
            return jsonify({'error': 'Car not found.'}), 404

        # Load and validate input data (partial updates allowed)
        data = CarSchema().load(request.get_json(), partial=True)

        # Update fields if they are provided in the request
        if 'mileage' in data:
            car.mileage = data['mileage']
        if 'price' in data:
            car.price = data['price']
        if 'condition' in data:
            car.condition = data['condition']
        if 'description' in data:
            car.description = data['description']
        if 'image_url' in data:
            car.image_url = data['image_url']
        if 'make_model_year_id' in data:
            # Check if the new make_model_year_id exists
            make_model_year = MakeModelYear.query.get(data['make_model_year_id'])
            if not make_model_year:
                return jsonify({'error': 'Invalid make_model_year_id.'}), 400
            car.make_model_year_id = data['make_model_year_id']

        # Commit the changes to the database
        db.session.commit()

        # Return the updated car as JSON with a 200 OK status
        return CarSchema().dump(car), 200
    except ValidationError as ve:
        # Return validation errors with a 400 Bad Request status
        return jsonify({'errors': ve.messages}), 400
    except Exception as e:
        # Handle any other exceptions
        return jsonify({'error': str(e)}), 500

# Route to delete a car
@cars_bp.route('/cars/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_car(id):
    
    # Get current user ID from the JWT token
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    # Check if user exists and is an admin
    if not user or not user.is_admin:
        return jsonify({'error': 'You do not have permission to perform this action.'}), 403

    try:
        # Fetch the existing car by ID
        car = Car.query.get(id)

        # Check if the car exists
        if not car:
            return jsonify({'error': 'Car not found.'}), 404

        # Check for associated CarTransactions
        if car.car_transactions:
            return jsonify({
                'error': 'Cannot delete car with associated transactions. Delete or reassign associated transactions first.'
            }), 400

        # Proceed to delete the car
        db.session.delete(car)
        db.session.commit()

        # Return a success message.
        return jsonify({'message': 'Car deleted successfully.'}), 200
    except Exception as e:
        # Handle any exceptions and return an error message
        return jsonify({'error': str(e)}), 500