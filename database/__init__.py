from database.models import DataBase

db = DataBase(DATABASE_URL="postgresql://admin:admin@db:5432/database")


"""
This module initializes the DataBase class, which is used for creating the database 
tables and inserting data instances. 

By initializing DataBase in the __init__.py file, we make it easier to import and use the class 
from other modules within this package. 

Usage:
    from database import db

    db.create_tables()
"""