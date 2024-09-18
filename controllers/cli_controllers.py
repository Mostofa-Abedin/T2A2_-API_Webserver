import json
import click
from flask import Blueprint
from flask.cli import with_appcontext
from init import db  # Import the SQLAlchemy database instance
from models.user import User  # Import models for database operations
from models.car import Car
from models.listing import Listing
from models.transaction import Transaction
from models.makemodelyear import MakeModelYear

# Create a blueprint for CLI commands
db_commands = Blueprint('db_commands', __name__)

# Command to create all tables in the database based on the model definitions
@db_commands.cli.command("create_tables")
@with_appcontext
def create_tables():
    """Create all database tables defined by the SQLAlchemy models."""
    try:
        db.create_all()  # Creates tables for all models that have been defined
        click.echo("All tables created successfully.")  # Provides feedback to the user
    except Exception as e:
        click.echo(f"An error occurred while creating tables: {e}")

# Command to drop all tables from the database
@db_commands.cli.command("drop_tables")
@with_appcontext
def drop_tables():
    """Drop all database tables. This will permanently remove all data in the tables."""
    # Confirmation prompt to prevent accidental data loss
    if click.confirm('Are you sure you want to drop all tables? This action cannot be undone.', abort=True):
        try:
            db.drop_all()  # Drops all tables from the database
            click.echo("All tables dropped successfully.")  # Provides feedback to the user
        except Exception as e:
            click.echo(f"An error occurred while dropping tables: {e}")

# Command to seed the database with initial data from a JSON file
@db_commands.cli.command("seed_tables")
@click.argument('file_path')  # Takes the path to the JSON file as a command-line argument
@with_appcontext
def seed_tables(file_path):
    """Seed the database with initial data from a specified JSON file."""
    try:
        # Open the JSON file and load its content into a dictionary
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Seed the Users table with data from the 'users' key in the JSON
        for user_data in data['users']:
            user = User(**user_data)  # Create a User object using unpacked JSON data
            db.session.add(user)  # Add the User object to the session

        # Seed the MakeModelYear table with data from the 'makemodelyears' key in the JSON
        for mm_data in data['makemodelyears']:
            makemodelyear = MakeModelYear(**mm_data)  # Create a MakeModelYear object
            db.session.add(makemodelyear)  # Add the MakeModelYear object to the session

        # Seed the Cars table with data from the 'cars' key in the JSON
        for car_data in data['cars']:
            car = Car(**car_data)  # Create a Car object
            db.session.add(car)  # Add the Car object to the session

        # Seed the Listings table with data from the 'listings' key in the JSON
        for listing_data in data['listings']:
            listing = Listing(**listing_data)  # Create a Listing object
            db.session.add(listing)  # Add the Listing object to the session

        # Seed the Transactions table with data from the 'transactions' key in the JSON
        for transaction_data in data['transactions']:
            transaction = Transaction(**transaction_data)  # Create a Transaction object
            db.session.add(transaction)  # Add the Transaction object to the session

        # Commit all the objects added to the session, saving them to the database
        db.session.commit()
        click.echo("Database seeded with data from the JSON file.")  # Provides feedback to the user

    except FileNotFoundError:
        # Handle the error if the specified JSON file does not exist
        click.echo(f"File '{file_path}' not found.")
    except json.JSONDecodeError:
        # Handle the error if the JSON file is not in a valid format
        click.echo("Invalid JSON file format.")
    except Exception as e:
        # Handle any other unexpected errors that occur during the seeding process
        click.echo(f"An error occurred: {e}")
