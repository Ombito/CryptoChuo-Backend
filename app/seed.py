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
    ]

    for user_info in users_data:
        new_user = User(**user_info)
        db.session.add(new_user)


    db.session.commit()

    
    courses_data = [
        {'title': 'Blockchain Fundamentals', 'user_id': 1, 'description': 'Learn the basic concepts and principles of blockchain technology.', 'image': 'new image', 'category': 'Technology', 'price': 19.99, 'rating': 4.5, 'duration': '1 week', 'level': 'Beginner'},
        {'title': 'Smart Contracts Development', 'user_id': 2, 'description': 'Hands-on experience in developing smart contracts on various blockchain platforms.', 'image': 'new image', 'category': 'Programming', 'price': 29.99, 'rating': 4.8, 'duration': '12 hours', 'level': 'Intermediate'},
        {'title': 'Decentralized Finance (DeFi)', 'user_id': 5, 'description': 'Explore decentralized financial systems and applications.', 'image': 'new image', 'category': 'Finance', 'price': 49.99, 'rating': 4.7, 'duration': '35 hours', 'level': 'Advanced'},
        {'title': 'Cryptocurrency Trading Strategies', 'user_id': 3, 'description': 'Explore effective trading strategies for cryptocurrencies and market analysis..', 'image': 'new image', 'category': 'Finance', 'price': 69.99, 'rating': 4.5, 'duration': '48 hours', 'level': 'Intermediate'},
        {'title': 'Decentralized Applications (DApps) Development', 'user_id': 5, 'description': 'Hands-on experience in developing decentralized applications on blockchain platforms.', 'image': 'new image', 'category': 'Programming', 'price': 99.99, 'rating': 4.9, 'duration': '4 months', 'level': 'Advanced'},
        {'title': 'Blockchain and Cybersecurity', 'user_id': 1, 'description': 'Explore the intersection of blockchain technology and cybersecurity.', 'image': 'new image', 'category': 'Technology', 'price': 59.99, 'rating': 4.7, 'duration': '48 hours', 'level': 'Intermediate'},
        {'title': 'Initial Coin Offerings (ICOs) Explained', 'user_id': 2, 'description': 'Understand the concept of Initial Coin Offerings and their implications.', 'image': 'new image', 'category': 'Finance', 'price': 39.99, 'rating': 4.4, 'duration': '12 hours', 'level': 'Beginner'},
        {'title': 'Blockchain and Supply Chain Management', 'user_id': 3, 'description': 'Learn how blockchain is revolutionizing supply chain management.', 'image': 'new image', 'category': 'Business', 'price': 79.99, 'rating': 4.6, 'duration': '30 hours', 'level': 'Intermediate'},
        {'title': 'Ethereum Smart Contracts Security', 'user_id': 4, 'description': 'Security considerations in the development of smart contracts on the Ethereum platform.', 'image': 'new image', 'category': 'Programming', 'price': 89.99, 'rating': 4.8, 'duration': '72 hours', 'level': 'Advanced'},
        {'title': 'Blockchain and Digital Identity', 'user_id': 5, 'description': 'Explore the use of blockchain in securing digital identities.', 'image': 'new image', 'category': 'Technology', 'price': 19.99, 'rating': 4.7, 'duration': '12 hours', 'level': 'Intermediate'},

    ]

    for course_info in courses_data:
        new_course = Course(**course_info)
        db.session.add(new_course)

    db.session.commit()

   

   
db.session.commit()


print('Database seeded successfully.')
