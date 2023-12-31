from flask_cors import CORS
from flask import Flask, jsonify, request, session, make_response
from flask_restful import Api, Resource
from models import User, db, Course, OrderRecord, Merchandise, Contact, Newsletter, bcrypt
from flask_migrate import Migrate
from werkzeug.exceptions import NotFound
import os
from datetime import timedelta
from flask_session import Session
import secrets


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, support_credentials=True)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = secrets.token_hex(16)
app.config['SESSION_TYPE'] = 'filesystem'
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_FILE_DIR'] = 'session_dir'
app.config['JSONIFY_PRETTYPRINT_REGULAR']= True


db.init_app(app)
api = Api(app)
migrate = Migrate(app, db)
Session(app)

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

        if user:
            if user.authenticate(password):
                session['user_id']=user.id
                return make_response(jsonify(user.to_dict()), 200)
                
            else:
                return make_response(jsonify({"error": "Username or password is incorrect"}), 401)
        else:
            return make_response(jsonify({"error": "User not Registered"}), 404)

        
     # signup resource
class SignupUser(Resource):
    def post(self):
        try:
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
                session['user_type'] = 'user'

                return make_response(jsonify(new_user.to_dict()),201)
            
            return make_response(jsonify({"error": "user details must be added"}),422)
    
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


    #logout resource
class Logout(Resource):
    def delete(self):
        if session.get('user_id'):
            session['user_id']=None
            return {"message": "User logged out successfully"}
        else:
            return {"error":"User must be logged in to logout"}


 #check session   
class CheckSession(Resource):
    def get(self):
        new_user = session.get('new_user')
        if new_user == 'user':
            user = User.query.filter(User.id == session.get('user_id')).first()
            if user:
                response= make_response(jsonify(user.to_dict()),200)
                response.content_type='application/json'
                return response
        
            else:
                return make_response(jsonify({"error": "user not in session: please signin/login"}), 401)
    

    #  all users route
class UserResource(Resource):
    def get(self):
        users = [user.to_dict() for user in User.query.all()]

        return make_response(jsonify(users),200) 


    # course route
class CourseResource(Resource):
    def get(self):
        all_courses = [course.to_dict() for course in Course.query.all()]
        
        return make_response(jsonify(all_courses),200)
   
        # post course records
    def post(self):
        data = request.get_json()

        title=data.get('title')
        description=data.get('description')
        image = data.get('image')
        price = data.get('price')
        duration = data.get('duration')
        rating = data.get('rating')
        enrollment_date = data.get('enrollment_date')
        user_id=data.get('user_id')
       
        if image and price and enrollment_date:
            new_course = Course( title=title, description= description, image=image, price=price, duration=duration, rating=rating, enrollment_date=enrollment_date, user_id=user_id)
            
            db.session.add(new_course)
            db.session.commit()

            return make_response(new_course.to_dict(), 201) 
        return {"error": "Course details must be added"}, 422
    

class CourseRecordById(Resource):
    #get course by id
    def get(self,id):
        pass
        course=Course.query.filter_by(id=id).first().to_dict()

        return make_response(jsonify(course),200)
    
        
class CourseRecordForUser(Resource):
        # post course record for a certain user
    def post(self, user_id):
        try:
            data = request.get_json()

            data['user_id'] = user_id

            my_course = Course(**data)
            db.session.add(my_course)
            db.session.commit()

            return make_response(jsonify(my_course.to_dict()), 201)

        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)
        

        # edit a course record    
    def patch(self,id):
        my_course = Course.query.filter_by(id=id).first()

        if my_course:
            for attr in request.get_json():
                setattr(my_course,attr, request.get_json()[attr])

            db.session.add(my_course)
            db.session.commit()
            
            return make_response(jsonify(my_course.to_dict(), 200))
        
        return {"error": "Course record not found"}, 404

        # delete a course record
    def delete(self,id):
        my_course=Course.query.get(id)

        if my_course:
            db.session.delete(my_course)
            db.session.commit()
            return {"message": "Course record deleted successfully"}, 200
        else:
            return {"error": "Course record not found"}, 404
    

    # orders route
class OrderResource(Resource):

        # get all order records
    def get(self):
        all_orders = [order.to_dict() for  order in OrderRecord.query.all()]
        
        return make_response(jsonify(all_orders),200)

        # post order records
    def post(self):
        data = request.get_json()

        description=data.get('description')
        image = data.get('image')
        video = data.get('video')
        location = data.get('location')
        status = data.get('status')
        user_id=data.get('user_id')

        if image and video and location:
            new_order = OrderRecord(description=description, image=image, video=video, location=location, status=status, user_id=user_id)

            db.session.add(new_order)
            db.session.commit()
      
            return make_response(jsonify(new_order.to_dict(), 201))
        
        return {"error": "Order details must be added"}, 422

class OrderRecordById(Resource):
    def get(self,id):
        record=OrderRecord.query.filter_by(id=id).first().to_dict()
        

        return make_response(jsonify(record),200)
    
        # edit an order record
    def patch(self, id):
        order = OrderRecord.query.filter_by(id=id).first()

        if order:
            for attr in request.get_json():
                setattr(order,attr,request.get_json()[attr])

                db.session.add(order)
                db.session.commit()
            return make_response(jsonify(order.to_dict(), 200)) 
        
        
        return {"error": "Order record not found"}, 404


        # delete an order record from the db
    def delete(self, id):
        order = OrderRecord.query.filter_by(id=id).first()

        if order:
            db.session.delete(order)
            db.session.commit()
            return {"message": "Order record deleted successfully"}, 200
        else:
            return {"error": "Order record not found"}, 404


    # merchandise route
class MerchandiseResource(Resource):
    def get(self):
        all_merchandises = [merchandise.to_dict() for merchandise in Merchandise.query.all()]
        
        return make_response(jsonify(all_merchandises),200)
   
        # post merchandise records
    def post(self):
        data = request.get_json()

        name=data.get('name')
        description=data.get('description')
        image = data.get('image')
        price = data.get('price')
        rating = data.get('rating')

       
        if image and name and price and description:
            new_merchandise = Merchandise( name=name, description= description, image=image, price=price, rating=rating, )
            
            db.session.add(new_merchandise)
            db.session.commit()

            return make_response(new_merchandise.to_dict(), 201) 
        return {"error": "Merchandise details must be added"}, 422
    

    # contact route
class ContactResource(Resource):
    def get(self):
        all_contacts = [contact.to_dict() for contact in Contact.query.all()]
        
        return make_response(jsonify(all_contacts),200)
   
        # post contact records
    def post(self):
        data = request.get_json()

        name=data.get('name')
        phone_number=data.get('phone_number')
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')
       
        if email and name and subject and phone_number:
            new_contact = Contact( name=name, phone_number= phone_number, email=email, subject=subject, message=message, )
            
            db.session.add(new_contact)
            db.session.commit()

            return make_response(new_contact.to_dict(), 201) 
        return {"error": "Contact details must be added"}, 422

    # newsletter route
class NewsletterResource(Resource):
    def get(self):
        all_newsletters = [newsletter.to_dict() for newsletter in Newsletter.query.all()]
        
        return make_response(jsonify(all_newsletters),200)
   
        # post newsletter records
    def post(self):
        data = request.get_json()
        email = data.get('email')
       
        if email:
            new_newsletter = Newsletter( email=email )
            
            db.session.add(new_newsletter)
            db.session.commit()

            return make_response(new_newsletter.to_dict(), 201) 
        return {"error": "Newsletter details must be added"}, 422
    
    # home resource
api.add_resource(Index,'/', endpoint='landing')

    # user resources
api.add_resource(UserResource, '/users', endpoint='users')
api.add_resource(CheckSession,'/session_user',endpoint='session_user' )
api.add_resource(SignupUser, '/signup_user', endpoint='signup')
api.add_resource(LoginUser, '/login_user', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')

    #course resources
api.add_resource(CourseResource, '/courses', endpoint='courses')
api.add_resource(CourseRecordForUser, '/courses/user/<int:user_id>', endpoint='courses_for_user')
api.add_resource(CourseRecordById, '/courses/<int:id>', endpoint='coursebyid')

    # order resources
api.add_resource(OrderResource,'/orders', endpoint='order')
api.add_resource(OrderRecordById, '/orders/<int:id>', endpoint='ordersbyid')

    # merchandise resource
api.add_resource(MerchandiseResource, '/merchandises', endpoint='merchandises')

    # contact resource
api.add_resource(ContactResource, '/contact', endpoint='contact')

    # newsletter resource
api.add_resource(NewsletterResource, '/newsletters', endpoint='newsletters')


@app.before_request
def before_request():
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Credentials': 'true',
            'Content-Type': 'application/json'
        }
        return make_response('', 200, headers)
    
    
@app.errorhandler(NotFound)
def handle_not_found(e):
    response = make_response(
        "Not Found:The requested endpoint(resource) does not exist",
        404
        )
    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)