from database.models import DataBase

db = DataBase(DATABASE_URL="postgresql://admin:admin@db:5432/database")