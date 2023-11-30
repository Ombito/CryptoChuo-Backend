from sqlalchemy_serializer import SerializerMixin
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.ext.hybrid import hybrid_property

db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model,SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(50), unique=True)
    _password_hash = db.Column(db.String(100))
    

    student_courses = db.relationship('Courses', backref='user')
    all_orders = db.relationship('Orders', backref='user')

    serialize_rules=('-student_courses','-all_orders',)

    @hybrid_property
    def password_hash(self):
        raise AttributeError ("Not allowed")
    

    @password_hash.setter
    def password_hash (self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        
    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash,password.encode("utf-8"))


class Course(db.model,SerializerMixin):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.String(100))
    email = db.Column(db.String(100))
    username = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    serialize_rules=('-user.student_courses',)

class OrderRecord(db.Model,SerializerMixin):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    item=db.Column(db.String)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    description=db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    serialize_rules=('-user.all_orders',)