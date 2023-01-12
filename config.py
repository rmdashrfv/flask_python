import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'abc123')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'postgresql://mlaw:cjiaang11@localhost/flask_python_development')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True