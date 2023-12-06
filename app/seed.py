from app import db, app
from models import User, Course, OrderRecord, Merchandise, Enrollment


app.app_context().push()
db.create_all()

with app.app_context():
    user1 = User(full_name='John Doe', email='john.doe@example.com', username='john_doe')
    user1.password_hash = 'hashed_password'
    db.session.add(user1)

    user2 = User(full_name='Jane Doe', email='jane.doe@example.com', username='jane_doe')
    user2.password_hash = 'hashed_password'
    db.session.add(user2)

    
    course1 = Course(course_name='Introduction to Python', description='Learn Python programming', price=49.99, user_id=user1.id)
    db.session.add(course1)
    course2 = Course(course_name='Web Development Basics', description='Introduction to web development', price=59.99, user_id=user2.id)
    db.session.add(course2)

    
    merchandise1 = Merchandise(name='T-Shirt', description='Comfortable cotton T-Shirt', price=19.99, image='tshirt.jpg')
    db.session.add(merchandise1)
    merchandise2 = Merchandise(name='Mug', description='Coffee mug with a cool design', price=9.99, image='mug.jpg')
    db.session.add(merchandise2)

    
    enrollment1 = Enrollment(course_id=course1.id, user_id=user1.id)
    db.session.add(enrollment1)
    enrollment2 = Enrollment(course_id=course2.id, user_id=user2.id)
    db.session.add(enrollment2)

    
    order1 = OrderRecord(item='Laptop', description='Gaming laptop', quantity=1, user_id=user1.id, merchandise_id=merchandise1.id)
    db.session.add(order1)
    order2 = OrderRecord(item='Book', description='Python Programming Guide', quantity=2, user_id=user2.id, merchandise_id=merchandise2.id)
    db.session.add(order2)

    
    db.session.commit()

    print('Database seeded successfully.')
