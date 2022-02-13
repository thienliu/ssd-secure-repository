from sqlalchemy import true
from app import db
from app.main.models import Base
from flask_login import UserMixin, current_user
from flask_authorize import RestrictionsMixin, AllowancesMixin


#mapping tables
UserGroup = db.Table(
    'user_group', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'))
)

UserRole = db.Table(
    'user_role', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
)

class Group(db.Model, RestrictionsMixin):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)


# Authorization Data: role & status
# role:
# 1: admin
# 2: internal
# 3: external
class Role(db.Model, AllowancesMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

# Define a User model
class User(Base, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(192), nullable=False)

    # `roles` and `groups` are reserved words that *must* be defined
    # on the `User` model to use group- or role-based authorization.
    roles = db.relationship('Role', secondary=UserRole)
    groups = db.relationship('Group', secondary=UserGroup)

    # status:
    # 1: created
    # 2: active
    # 3: inactive
    status = db.Column(db.SmallInteger, nullable=False)

    def __init__(self, name, email, password, roles, groups, status):
        self.name = name
        self.email = email
        self.password = password
        self.roles = roles
        self.groups = groups
        self.status = status

    @property
    def isAdmin(self):
        if current_user.get_id() is not None:
            current_logged_in_user = User.query.filter_by(id=current_user.get_id()).first()
            return 'admin' in map(lambda r: r.name, current_logged_in_user.roles)

        else:
            return False

    @property
    def hasAdminRole(self):
        return 'admin' in map(lambda r: r.name, self.roles)

    def __repr__(self):
        return '<User %r>' % (self.name)       