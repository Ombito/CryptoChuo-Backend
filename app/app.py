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
class LoginUser(Resource):
    def post(self):
        email  = request.get_json().get('email')
        password = request.get_json().get("password")
        user = User.query.filter(User.email == email).first()
        if user and user.authenticate(password):
            session['user_id']=user.id
            return user.to_dict(),201
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

     # signup resource
class SignupUser(Resource):
    def post(self):
        data = request.get_json()

        full_name = data.get('full_name')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        

        if full_name and username and email and password:
            new_user = User(full_name=full_name, username=username, email=email)
            new_user.password_hash = password
            db.session.add(new_user)
            db.session.commit()

            session['user_id']=new_user.id

            return new_user.to_dict(), 201
        return {"error": "user details must be added"}, 422

 #check session   
class CheckSession(Resource):
    def get(self):
        user = User.query.filter(User.id == session.get('user_id')).first()
        if user:
            return jsonify(user.to_dict()),200
        else:
            return {"error": "user not in session:please signin/login"},401

    #  all users route
class UserResource(Resource):
    def get(self):
        users = [user.to_dict() for user in User.query.all()]

        return make_response(jsonify(users),200) 
    
    # orders route
class OrderResource(Resource):

        # get all order records
    def get(self):
        
        all_orders = [order.to_dict() for  order in Order.query.all()]
        
        return make_response(jsonify(all_orders),200)

        # post order records
    def post(self):
        data = request.get_json()

        title=data.get('title')
        description=data.get('description')
        image = data.get('image')
        video = data.get('video')
        location = data.get('location')
        status = data.get('status')
        user_id=data.get('user_id')

        if image and video and location:
            new_order = Order(title=title, description=description, image=image, video=video, location=location, status=status, user_id=user_id)

            db.session.add(new_order)
            db.session.commit()
      
            return make_response(jsonify(new_order.to_dict(), 201))
        
        return {"error": "Order details must be added"}, 422


if __name__ == '__main__':
    app.run(port=5555, debug=True)