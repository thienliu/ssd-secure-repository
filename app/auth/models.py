from app import db
from app.main.models import Base
from flask_login import UserMixin, current_user

# Define a User model
class User(Base, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(192), nullable=False)

    # Authorization Data: role & status
    # role:
    # 1: admin
    # 2: internal
    # 3: external
    role = db.Column(db.SmallInteger, nullable=False)

    # status:
    # 1: created
    # 2: active
    # 3: inactive
    status = db.Column(db.SmallInteger, nullable=False)

    def __init__(self, name, email, password, role, status):
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.status = status

    # def update_status(self, new_status):
    #     self.status = new_status

    # def get_email(self):
    #     return self.email

    @property
    def isAdmin(self):
        if current_user.get_id() is not None:
            current_logged_in_user = User.query.filter_by(
            id=current_user.get_id()).first()
            return current_logged_in_user.role == 1
        else:
            return False

    def __repr__(self):
        return '<User %r>' % (self.name)       