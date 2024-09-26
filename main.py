# Main application module for initializing and configuring the Flask app
import os
from flask import Flask
from init import db, ma, bcrypt, jwt

# Import the Blueprint
from controllers.cli_controllers import db_commands  
from controllers.auth_controller import auth_bp
from controllers.car_controller import cars_bp
from controllers.listing_controller import listings_bp
from controllers.car_transaction_controller import car_transactions_bp
from controllers.makemodelyear_controller import makemodelyear_bp

def create_app():
    # Create the Flask application instance
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

    # Initialize Flask extensions
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register blueprints to organize the app's routes and functionalities
    app.register_blueprint(db_commands)
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(cars_bp, url_prefix='/api')
    app.register_blueprint(listings_bp, url_prefix='/api')
    app.register_blueprint(car_transactions_bp, url_prefix='/api')
    app.register_blueprint(makemodelyear_bp, url_prefix='/api')

    return app
