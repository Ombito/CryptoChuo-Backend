from sqlalchemy_serializer import SerializerMixin
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.ext.hybrid import hybrid_property

db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(50), unique=True)
    _password_hash = db.Column(db.String(100), nullable=False)

    courses = db.relationship('Course', backref='user')
    orders = db.relationship('OrderRecord', backref='user')
    serialize_rules = ('-courses.user', '-orders.user',)

    @hybrid_property
    def password_hash(self):
        raise AttributeError("Not allowed")

    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode("utf-8"))


class Course(db.Model, SerializerMixin):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    image = db.Column(db.String(100))
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    level = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    enrollment_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    is_trending = db.Column(db.String)
    
    serialize_rules = ('-user.courses',)


class OrderRecord(db.Model, SerializerMixin):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String, nullable=False)
    image = db.Column(db.String(100))
    description = db.Column(db.String, nullable=False)
    order_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    quantity = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    serialize_rules = ('-user.orders',)


class Merchandise(db.Model, SerializerMixin):
    __tablename__ = 'merchandise_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100))
    price = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float, nullable=False)



