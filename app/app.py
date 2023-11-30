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
class LoginAdmin(Resource):
    def post(self):
        username  = request.get_json().get('username')
        password = request.get_json().get("password")

        admin = Admin.query.filter(Admin.username == username).first()
        if admin and admin.authenticate(password):
            session['admin_id']=admin.id
            return make_response(jsonify(admin.to_dict()),201)
        else:
            return {"error":"username or password is incorrect"},401

    #logout resource
class Logout(Resource):
    def delete(self):
        if session.get('user_id'):
            session['user_id']=None
            return {"message": "User logged out successfully"}
        else:
            return {"error":"User must be logged in to logout"}

#     # signup resource
# class Signup(Resource):
#     def post(self):


if __name__ == '__main__':
    app.run(port=5555, debug=True)