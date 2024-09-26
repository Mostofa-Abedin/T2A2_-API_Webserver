# Import standard library modules
import json

# Import third-party modules
import click
from flask import Blueprint
from flask.cli import with_appcontext
from sqlalchemy import text

# Import local modules
from init import db, bcrypt  # Database and bcrypt instances
from models.user import User
from models.car import Car
from models.listing import Listing
from models.car_transaction import CarTransaction
from models.makemodelyear import MakeModelYear

# Create a blueprint for CLI commands
db_commands = Blueprint('db_commands', __name__)

# Command to create all tables in the database based on the model definitions
@db_commands.cli.command("create_tables")
@with_appcontext
def create_tables():
    # Create all database tables defined by the SQLAlchemy models
    try:
        db.create_all()
        click.echo("All tables created successfully.")
    except Exception:
        click.echo("An error occurred while creating tables.")

# Command to drop all tables from the database
@db_commands.cli.command("drop_tables")
@with_appcontext
def drop_tables():
    # Drop all database tables. This will permanently remove all data in the tables.
    if click.confirm(
        'Are you sure you want to drop all tables? This action cannot be undone.',
        abort=True
    ):
        try:
            # Drop all tables with cascade
            db.session.execute(text(
                'DROP TABLE IF EXISTS users, makemodelyear, cars, listings, car_transactions CASCADE'
            ))
            db.session.commit()
            click.echo("All tables dropped successfully.")
        except Exception:
            click.echo("An error occurred while dropping tables.")

# Command to seed the database with initial data from a JSON file
@db_commands.cli.command("seed_tables")
@click.argument('file_path')
@with_appcontext
def seed_tables(file_path):
    # Seed the database with initial data from a specified JSON file
    try:
        # Open the JSON file and load its content
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Seed the Users table
        for user_data in data.get('users', []):
            try:
                # Hash the user's password
                user_data['password'] = bcrypt.generate_password_hash(
                    user_data['password']
                ).decode('utf-8')
                user = User(**user_data)
                db.session.add(user)
            except Exception:
                click.echo("An error occurred while adding a user.")

        # Seed the MakeModelYear table
        for mm_data in data.get('makemodelyears', []):
            makemodelyear = MakeModelYear(**mm_data)
            db.session.add(makemodelyear)

        # Seed the Cars table
        for car_data in data.get('cars', []):
            car = Car(**car_data)
            db.session.add(car)

        # Seed the Listings table
        for listing_data in data.get('listings', []):
            listing = Listing(**listing_data)
            db.session.add(listing)

        # Seed the CarTransactions table
        for transaction_data in data.get('car_transactions', []):
            transaction = CarTransaction(**transaction_data)
            db.session.add(transaction)

        # Commit all the changes to the database
        db.session.commit()
        click.echo("Database seeded successfully with data from the JSON file.")
    except FileNotFoundError:
        click.echo(f"File '{file_path}' not found.")
    except json.JSONDecodeError:
        click.echo("Invalid JSON file format.")
    except Exception:
        click.echo("An error occurred during database seeding.")
