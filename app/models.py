from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ireporter.db'
db = SQLAlchemy(app)

class User(db.model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))

class Course(db.model):
    __tablename__ = 'courses'
