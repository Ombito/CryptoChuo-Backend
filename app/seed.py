from app import app
from models import User, db, Course, OrderRecord, Merchandise
import datetime
import random

app.app_context().push()
db.drop_all()
db.create_all()

with app.app_context():
   
    users_data = [
        {'full_name': 'User1', 'email': 'user1@example.com', 'username': 'user1', '_password_hash': 'password1'},
        {'full_name': 'User2', 'email': 'user2@example.com', 'username': 'user2', '_password_hash': 'password2'},
        # Add more users as needed
    ]

    for user_info in users_data:
        new_user = User(**user_info)
        db.session.add(new_user)

    # Commit users to the database
    db.session.commit()

    # Create courses
    courses_data = [
        {'title': 'Course1', 'user_id': 1, 'description': 'Description for Course1', 'image': 'new image', 'category': 'beginner', 'price': 19.99, 'rating': 4.5, 'duration': '1 week', 'level': 'beginner'},
        {'title': 'Course2', 'user_id': 2, 'description': 'Description for Course1', 'image': 'new image', 'category': 'beginner', 'price': 19.99, 'rating': 4.5, 'duration': '1 week', 'level': 'beginner'},
        # Add more courses as needed
    ]

    for course_info in courses_data:
        new_course = Course(**course_info)
        db.session.add(new_course)

    db.session.commit()

   

   
db.session.commit()


print('Database seeded successfully.')
