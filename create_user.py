from app import db, bcrypt
from app.auth.models import User, Role
import sys

def main():
    create_user()

# Pre-populates several accounts for testing
def create_user():
    default_password = "Qwerty@123"

    admin_role = Role(name='admin')
    staff_role = Role(name='staff')

    hashed_password = bcrypt.generate_password_hash(default_password)
    user1 = User(
        name = "Thien",
        email = "thien@awesomerepo.com", 
        password = hashed_password,
        roles = [admin_role], 
        groups = [],
        status = 2
    )
    user2 = User(
        name = "Neelam",
        email = "neelam@awesomerepo.com", 
        password = hashed_password,
        roles = [admin_role], 
        groups = [],
        status = 2
    )
    user3 = User(
        name = "Created Internal Staff",
        email = "internal_created@awesomerepo.com", 
        password = hashed_password,
        roles = [staff_role], 
        groups = [],
        status = 1
    )

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.commit()

if __name__ == '__main__':
    sys.exit(main())
