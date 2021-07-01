import os 

#database initialization
if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:root@localhost:5432/schedule_db"
else:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL").replace("postgres://", "postgresql://", 1)

SQLALCHEMY_TRACK_MODIFICATIONS = False