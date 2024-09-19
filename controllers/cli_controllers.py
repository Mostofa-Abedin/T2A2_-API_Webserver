import json
import click
from flask import Blueprint
from flask.cli import with_appcontext
from init import db, bcrypt  # Import bcrypt for password hashing
from models.user import User  # Import models for database operations
from models.car import Car
from models.listing import Listing
from models.car_transaction import CarTransaction  # Updated import
from models.makemodelyear import MakeModelYear
from sqlalchemy import text

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
            # Drop all tables with cascade
            db.session.execute(text('DROP TABLE IF EXISTS users, makemodelyear, cars, listings, car_transactions CASCADE'))
            db.session.commit()
            click.echo("All tables dropped successfully.")
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
            try:
                user_data['password'] = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
                user = User(**user_data)
                db.session.add(user)
                print(f"Adding user: {user.name}")  # Debugging line to check user addition
            except Exception as e:
                print(f"Error adding user: {e}")  # Print any errors that occur

        # Seed the MakeModelYear table with data from the 'makemodelyears' key in the JSON
        for mm_data in data['makemodelyears']:
            makemodelyear = MakeModelYear(**mm_data)
            db.session.add(makemodelyear)

        # Seed the Cars table with data from the 'cars' key in the JSON
        for car_data in data['cars']:
            car = Car(**car_data)
            db.session.add(car)

        # Seed the Listings table with data from the 'listings' key in the JSON
        for listing_data in data['listings']:
            listing = Listing(**listing_data)
            db.session.add(listing)

        # Seed the CarTransactions table with data from the 'car_transactions' key in the JSON
        for transaction_data in data['car_transactions']:  # Use the correct key here
            transaction = CarTransaction(**transaction_data)
            db.session.add(transaction)

        # Commit all the objects added to the session
        db.session.commit()
        click.echo("Database seeded with data from the JSON file.")

    except FileNotFoundError:
        click.echo(f"File '{file_path}' not found.")
    except json.JSONDecodeError:
        click.echo("Invalid JSON file format.")
    except Exception as e:
        click.echo(f"An error occurred: {e}")
