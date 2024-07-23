import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'postgresql://postgreuser:Vj00aMGsv4lhXMqUcWpM13nbIbDTTb9D@dpg-cqfqa31u0jms7386iqs0-a.singapore-postgres.render.com/postgredatabase_6cyp'