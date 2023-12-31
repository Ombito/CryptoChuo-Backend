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
        {'title': 'Blockchain Fundamentals', 'user_id': 1, 'description': 'Learn the basic concepts and principles of blockchain technology.', 'image': 'new image', 'category': 'Technology', 'price': 19.99, 'rating': 4.5, 'duration': '1 week', 'level': 'Beginner', 'is_trending': 'true'},
        {'title': 'Smart Contracts Development', 'user_id': 2, 'description': 'Hands-on experience in developing smart contracts on various blockchain platforms.', 'image': 'new image', 'category': 'Programming', 'price': 29.99, 'rating': 4.8, 'duration': '12 hours', 'level': 'Intermediate', 'is_trending': 'true'},
        {'title': 'Decentralized Finance (DeFi)', 'user_id': 5, 'description': 'Explore decentralized financial systems and applications.', 'image': 'new image', 'category': 'Finance', 'price': 49.99, 'rating': 4.7, 'duration': '35 hours', 'level': 'Advanced', 'is_trending': 'true'},
        {'title': 'Cryptocurrency Trading Strategies', 'user_id': 3, 'description': 'Explore effective trading strategies for cryptocurrencies and market analysis..', 'image': 'new image', 'category': 'Finance', 'price': 69.99, 'rating': 4.5, 'duration': '48 hours', 'level': 'Intermediate'},
        {'title': 'Decentralized Applications (DApps) Development', 'user_id': 5, 'description': 'Hands-on experience in developing decentralized applications on blockchain platforms.', 'image': 'new image', 'category': 'Programming', 'price': 99.99, 'rating': 4.9, 'duration': '4 months', 'level': 'Advanced'},
        {'title': 'Blockchain and Cybersecurity', 'user_id': 1, 'description': 'Explore the intersection of blockchain technology and cybersecurity.', 'image': 'new image', 'category': 'Technology', 'price': 59.99, 'rating': 4.7, 'duration': '48 hours', 'level': 'Intermediate'},
        {'title': 'Initial Coin Offerings (ICOs) Explained', 'user_id': 2, 'description': 'Understand the concept of Initial Coin Offerings and their implications.', 'image': 'new image', 'category': 'Finance', 'price': 39.99, 'rating': 4.4, 'duration': '12 hours', 'level': 'Beginner'},
        {'title': 'Blockchain and Healthcare', 'user_id': 3, 'description': 'Applications of blockchain technology in the healthcare industry.', 'image': 'new image', 'category': 'Health', 'price': 79.99, 'rating': 4.6, 'duration': '30 hours', 'level': 'Intermediate'},
        {'title': 'Ethereum Smart Contracts Security', 'user_id': 4, 'description': 'Security considerations in the development of smart contracts on the Ethereum platform.', 'image': 'new image', 'category': 'Programming', 'price': 89.99, 'rating': 4.8, 'duration': '72 hours', 'level': 'Advanced', 'is_trending': 'true'},
        {'title': 'Blockchain and Digital Identity', 'user_id': 5, 'description': 'Explore the use of blockchain in securing digital identities.', 'image': 'new image', 'category': 'Technology', 'price': 19.99, 'rating': 4.7, 'duration': '2 hours', 'level': 'Intermediate'},
        {'title': 'Cryptocurrency Investment Strategies', 'user_id': 2, 'description': 'Learn effective strategies for investing in cryptocurrencies.', 'image': 'new image', 'category': 'Finance', 'price': 29.99, 'rating': 4.9, 'duration': '6 hours', 'level': 'Intermediate'},
        {'title': 'Hyperledger Fabric Development', 'user_id': 3, 'description': 'Hands-on experience in developing applications using Hyperledger Fabric.', 'image': 'new image', 'category': 'Programming', 'price': 99.99, 'rating': 4.8, 'duration': '4 weeks', 'level': 'Advanced'},
        {'title': 'Ripple and XRP Explained', 'user_id': 4, 'description': 'An in-depth look at Ripple and its native cryptocurrency XRP.', 'image': 'new image', 'category': 'Technology', 'price': 29.99, 'rating': 4.5, 'duration': '8 hours', 'level': 'Beginner', 'is_trending': 'true'},
        {'title': 'NFTs and Digital Art', 'user_id': 2, 'description': 'Understanding Non-Fungible Tokens (NFTs) and their impact on the art world.', 'image': 'new image', 'category': 'Art', 'price': 29.99, 'rating': 4.4, 'duration': '6 hours', 'level': 'Beginner', 'is_trending': 'true'},
        {'title': 'Introduction to Solidity Programming', 'user_id': 1, 'description': 'Learn the basics of programming smart contracts using Solidity.', 'image': 'new image', 'category': 'Programming', 'price': 49.99, 'rating': 4.4, 'duration': '30 hours', 'level': 'Beginner', 'is_trending': 'true'},
        {'title': 'Blockchain and Social Impact', 'user_id': 5, 'description': 'Explore how blockchain technology can be leveraged for positive social impact.', 'image': 'new image', 'category': 'Social Impact', 'price': 39.99, 'rating': 4.7, 'duration': '24 hours', 'level': 'Advanced'},
        {'title': 'Cardano (ADA) Explained', 'user_id': 3, 'description': 'An overview of the Cardano blockchain and its native cryptocurrency ADA.', 'image': 'new image', 'category': 'Technology', 'price': 29.99, 'rating': 4.6, 'duration': '12 hours', 'level': 'Intermediate'},
        {'title': 'Blockchain and Legal Implications', 'user_id': 4, 'description': 'Understand the legal implications and challenges of blockchain technology', 'image': 'new image', 'category': 'Business', 'price': 49.99, 'rating': 4.6, 'duration': '8 hours', 'level': 'Intermediate', 'is_trending': 'true'},
        {'title': 'Blockchain and Supply Chain Management', 'user_id': 2, 'description': 'Learn how blockchain is revolutionizing supply chain management.', 'image': 'new image', 'category': 'Business', 'price': 39.99, 'rating': 4.6, 'duration': '12 hours', 'level': 'Intermediate'},
        {'title': 'Blockchain and Environmental Sustainability', 'user_id': 4, 'description': 'Explore the role of blockchain in promoting environmental sustainability.', 'image': 'new image', 'category': 'Technology', 'price': 29.99, 'rating': 4.7, 'duration': '12 hours', 'level': 'Intermediate'},
    ]

    for course_info in courses_data:
        new_course = Course(**course_info)
        db.session.add(new_course)

    db.session.commit()


    merchandise_data = [
        {'name': 'Blockchain T-Shirt', 'description': 'High-quality cotton T-shirt with a blockchain-themed design.', 'image': 'new image', 'price': 19.99, 'rating': 4.5},
        {'name': 'Cryptocurrency Mug', 'description': 'Ceramic mug featuring popular cryptocurrency logos.', 'image': 'new image', 'price': 12.99, 'rating': 4.8},
        {'name': 'Crypto Backpack', 'description': 'Spacious backpack with a modern blockchain-inspired pattern.', 'image': 'new image', 'price': 39.99, 'rating': 4.2},
        {'name': 'Blockchain Stickers Set', 'description': 'Set of high-quality vinyl stickers featuring blockchain symbols..', 'image': 'new image', 'price': 8.99, 'rating': 4.4},
        {'name': 'Bitcoin Hoodie', 'description': 'Warm hoodie with a Bitcoin logo for crypto enthusiasts.', 'image': 'new image', 'price': 29.99, 'rating': 4.5},
        {'name': 'Ethereum Mousepad', 'description': 'Large mousepad featuring the Ethereum logo and blockchain graphics.', 'image': 'new image', 'price': 14.99, 'rating': 4.0},
        {'name': 'Litecoin Keychain', 'description': 'Durable keychain with a Litecoin symbol for your keys.', 'image': 'new image', 'price': 9.99, 'rating': 4.4},
        {'name': 'Crypto Art Poster', 'description': 'Artistic poster depicting the beauty of blockchain and cryptocurrency.', 'image': 'new image', 'price': 24.99, 'rating': 4.7},
        {'name': 'Ripple Water Bottle', 'description': 'Stainless steel water bottle featuring the Ripple logo.', 'image': 'new image', 'price': 19.99, 'rating': 4.0},
        {'name': 'Smart Contracts Notebook', 'description': 'Elegant notebook with smart contract diagrams for jotting down your ideas.', 'image': 'new image', 'price': 11.99, 'rating': 4.5},
        {'name': 'NFT Art Canvas', 'description': 'Canvas print featuring exclusive NFT artwork from a renowned crypto artist.', 'image': 'new image', 'price': 49.99, 'rating': 4.8},
        {'name': 'Cardano Cap', 'description': 'Adjustable cap with the Cardano logo for sun protection.', 'image': 'new image', 'price': 21.99, 'rating': 3.8},
        {'name': 'Crypto Puzzle Set', 'description': 'Challenging puzzle set with cryptocurrency-themed pieces.', 'image': 'new image', 'price': 21.99, 'rating': 3.9},
        {'name': 'Tron USB Drive', 'description': 'High-speed USB drive with the Tron logo for secure data storage.', 'image': 'new image', 'price': 18.99, 'rating': 4.8},
        {'name': 'Monero Socks', 'description': 'Comfortable socks with Monero symbols for a touch of crypto style.', 'image': 'new image', 'price': 8.99, 'rating': 4.1},
        {'name': 'Blockchain Watch', 'description': 'Elegant wristwatch with blockchain-inspired design and features.', 'image': 'new image', 'price': 69.99, 'rating': 4.5},
        {'name': 'Stellar Lumens Phone Case', 'description': 'Durable phone case with Stellar Lumens logo for various phone models.', 'image': 'new image', 'price': 15.99, 'rating': 3.9},
        {'name': 'Blockchain Puzzle Book', 'description': 'Interactive puzzle book filled with blockchain-related challenges.', 'image': 'new image', 'price': 14.99, 'rating': 4.5},
        {'name': 'Tezos Tea Set', 'description': 'Fine porcelain tea set with Tezos blockchain motifs for tea enthusiasts.', 'image': 'new image', 'price': 34.99, 'rating': 4.0},
        {'name': 'EOS Sunglasses', 'description': 'Stylish sunglasses with the EOS logo for protection under the sun.', 'image': 'new image', 'price': 25.99, 'rating': 4.8},
    ]

    for merchandise_info in merchandise_data:
        new_merchandise = Merchandise(**merchandise_info)
        db.session.add(new_merchandise)

    db.session.commit()


   
db.session.commit()


print('Database seeded successfully.')
