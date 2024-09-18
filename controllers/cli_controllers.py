from flask import Blueprint
from init import db
from models.user import User

db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_tables():
    db.create_all()
    print("Tables created!")

@db_commands.cli.command('drop')
def drop_tables():
    db.drop_all()
    print("Tables dropped!")

@db_commands.cli.command('seed')
def seed_tables():
    users = [
        # Add user data later
        User(email="admin@test.com", password=bcrypt.generate_password_hash("123456").decode('utf-8'), is_admin=True),
        User(email="user@test.com", password=bcrypt.generate_password_hash("123456").decode('utf-8'), is_admin=False)
    ]
    db.session.add_all(users)
    db.session.commit()
    print("Tables seeded!")