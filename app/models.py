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
    title = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100))
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    enrollment_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    enrollments = db.relationship('Enrollment', back_populates='course')
    categories = db.relationship('CourseCategory', back_populates='course')
    durations = db.relationship('CourseDurationAssociation', back_populates='course')
    levels = db.relationship('CourseLevel', back_populates='course')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='courses')

    duration_associations = db.relationship('CourseDurationAssociation', back_populates='course', overlaps="durations")

    serialize_rules = ('-enrollments.course', '-user.courses', '-categories.course', '-durations.course', '-levels.course',)


class Category(db.Model, SerializerMixin):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    courses = db.relationship('CourseCategory', back_populates='category')


class CourseCategory(db.Model, SerializerMixin):
    __tablename__ = 'course_categories'

    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), primary_key=True)

    course = db.relationship('Course', back_populates='categories')
    category = db.relationship('Category', back_populates='courses')


class CourseDuration(db.Model, SerializerMixin):
    __tablename__ = 'course_durations'

    id = db.Column(db.Integer, primary_key=True)
    duration = db.Column(db.String(20), unique=True, nullable=False)

    courses = db.relationship('CourseDurationAssociation', back_populates='duration')

class CourseDurationAssociation(db.Model, SerializerMixin):
    __tablename__ = 'course_duration_association'

    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), primary_key=True)
    duration_id = db.Column(db.Integer, db.ForeignKey('course_durations.id'), primary_key=True)

    course = db.relationship('Course', back_populates='duration_associations')
    duration = db.relationship('CourseDuration', back_populates='courses')


class Level(db.Model, SerializerMixin):
    __tablename__ = 'levels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    courses = db.relationship('CourseLevel', back_populates='level')


class CourseLevel(db.Model, SerializerMixin):
    __tablename__ = 'course_levels'

    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), primary_key=True)
    level_id = db.Column(db.Integer, db.ForeignKey('levels.id'), primary_key=True)

    course = db.relationship('Course', back_populates='levels')
    level = db.relationship('Level', back_populates='courses')


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
    rating = db.Column(db.Float, nullable=False)

    orders = db.relationship('OrderRecord', back_populates='merchandise')

    serialize_rules = ('-orders.merchandise',)


class Enrollment(db.Model, SerializerMixin):
    __tablename__ = 'enrollments'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    course = db.relationship('Course', back_populates='enrollments')
    user = db.relationship('User', back_populates='enrollments')
