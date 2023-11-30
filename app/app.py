from flask_cors import CORS, cross_origin
from flask import Flask, jsonify, request, session, make_response
from flask_restful import Api, Resource, reqparse
from models import User, db
from flask_migrate import Migrate
import os


app = Flask(__name__)
CORS(app,support_credentials=True)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key='qwwerrtyyu123'
db.init_app(app)
api = Api(app)
migrate = Migrate(app, db)

    # home route
class Index(Resource):
    def get(self):
        response_body = '<h1>Hello World</h1>'
        status = 200
        headers = {}
        return make_response(response_body,status,headers)
    
    # login route
class Login(Resource):
    def get(self):

    #logout resource
class Logout(Resource):

    # signup resource
class Signup(Resource):
    def post(self):
