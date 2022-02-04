import email
from app import db, bcrypt
from app.auth.models import User
import sys

def main():
    password = "Qwerty@123"
    hashed_password = bcrypt.generate_password_hash(password)
    user1 = User(
        name = "Thien",
        email = "thien@awesomerepo.com", 
        password = hashed_password,
        role = 1, 
        status = 2
    )
    user2 = User(
        name = "Neelam",
        email = "neelam@awesomerepo.com", 
        password = hashed_password,
        role = 1, 
        status = 2
    )
    user3 = User(
        name = "Created Internal Staff",
        email = "internal_created@awesomerepo.com", 
        password = hashed_password,
        role = 2, 
        status = 1
    )
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.commit()

if __name__ == '__main__':
    sys.exit(main())
