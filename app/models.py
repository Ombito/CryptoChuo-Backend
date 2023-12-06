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
    _password_hash = db.Column(db.String(100))

    courses = db.relationship('Course', back_populates='user')
    orders = db.relationship('OrderRecord', back_populates='user')
    enrollments = db.relationship('Enrollment', back_populates='user')

    serialize_rules = ('-courses.user', '-orders.user', '-enrollments.user',)

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
    course_name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100))
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    enrollment_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    enrollments = db.relationship('Enrollment', back_populates='course')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='courses')

    serialize_rules = ('-enrollments.course', '-user.courses',)


class OrderRecord(db.Model, SerializerMixin):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String, nullable=False)
    image = db.Column(db.String(100))
    description = db.Column(db.String, nullable=False)
    order_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    quantity = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='orders')

    merchandise_id = db.Column(db.Integer, db.ForeignKey('merchandises.id'))
    merchandise = db.relationship('Merchandise', back_populates='orders')

    serialize_rules = ('-user.all_orders',)


class Merchandise(db.Model, SerializerMixin):
    __tablename__ = 'merchandises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100))
    price = db.Column(db.Float, nullable=False)

    orders = db.relationship('OrderRecord', back_populates='merchandise')

    serialize_rules = ('-orders.merchandise',)


class Enrollment(db.Model, SerializerMixin):
    __tablename__ = 'enrollments'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    course = db.relationship('Course', back_populates='enrollments')
    user = db.relationship('User', back_populates='enrollments')
