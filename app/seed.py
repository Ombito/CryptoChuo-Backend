from app import app
from models import User, db, Course, Category, CourseCategory, CourseDuration, CourseDurationAssociation, Level, CourseLevel, OrderRecord, Merchandise, Enrollment
import datetime
import random

app.app_context().push()
db.drop_all()
db.create_all()

with app.app_context():
    # Create users
    for i in range(10):
        user = User(
            full_name=f'User{i}',
            email=f'user{i}@example.com',
            username=f'user{i}',
            _password_hash='hashed_password'
        )
        db.session.add(user)
    db.session.commit()

    # Create categories, durations, and levels (same as before)
    categories_data = ['Programming', 'Mathematics', 'Science', 'Art', 'History', 'Music', 'Languages', 'Fitness', 'Cooking', 'Business']

    for category_name in categories_data:
        category = Category(name=category_name)
        db.session.add(category)

    # Create durations
    durations_data = ['1 Week', '2 Weeks', '1 Month', '2 Months', '3 Months', '6 Months', '1 Year', '2 Years', 'Lifetime', 'Flexible']

    for duration_name in durations_data:
        duration = CourseDuration(duration=duration_name)
        db.session.add(duration)

    # Create levels
    levels_data = ['Beginner', 'Intermediate', 'Advanced', 'Expert', 'All Levels', 'Introductory', 'Intermediate-Advanced', 'Masterclass', 'Professional', 'Custom']

    for level_name in levels_data:
        level = Level(name=level_name)
        db.session.add(level)

    db.session.commit()

    # Create courses
    for i in range(10):
        # user = db.session.query(User).get(random.randint(1, 10))
        user=User.query.order_by(db.func.random()).first()
        course = Course(
            title=f'Course {i}',
            description=f'This is course number {i}.',
            price=19.99 + i,
            rating=random.uniform(3.0, 5.0),
            enrollment_date=datetime.datetime.now(),
            user=user
        )
        db.session.add(course)
        db.session.commit()

        # Add categories, durations, and levels to the course
        # category = db.session.query(Category).get(1)
        # duration = db.session.query(CourseDuration).get(1)
        # level = db.session.query(Level).get(1)

        # if category:
        #     course_category = CourseCategory(course_id=course.id, category_id=category.id)
        #     db.session.add(course_category)

        # if duration:
        #     course_duration = CourseDurationAssociation(course_id=course.id, duration_id=duration.id)
        #     db.session.add(course_duration)

        # if level:
        #     course_level = CourseLevel(course_id=course.id, level_id=level.id)
        #     db.session.add(course_level)

    

        merchandise1 = Merchandise(name='Merchandise1', description="Newyork tshirt", price=10.99, rating=4)
        merchandise2 = Merchandise(name='Merchandise2', description="Newyork trouser", price=20.99, rating=4)
        db.session.add_all([merchandise1, merchandise2])
        db.session.commit()

        order1 = OrderRecord(
            item='Item1',
            image='item1.jpg',
            description='Description for Item1',
            quantity=2,
            user=User.query.order_by(db.func.random()).first(),
            merchandise=merchandise1,
            location="Nairobi"
        )

        order2 = OrderRecord(
            item='Item2',
            image='item2.jpg',
            description='Description for Item2',
            quantity=1,
            user=User.query.order_by(db.func.random()).first(),
            merchandise=merchandise2,
            location="Eldoret"
        )

        db.session.add_all([order1, order2])
        db.session.commit()
    # Create enrollments, merchandises, orders (same as before)
    db.session.commit()

    print('Database seeded successfully.')
