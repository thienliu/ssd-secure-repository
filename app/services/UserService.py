from distutils.log import Log
from app.auth.models import User
from flask import request
from flask_login import current_user, login_required
from app import db
from app.errors.authErrors import UserDeletionError
class UserService:

    @classmethod
    def get_current_user_email(cls):
        if current_user.get_id() is not None:
            user = User.query.filter_by(id=current_user.get_id()).first()
            if user:
                return user.email

    @classmethod
    def get_user_ip_address(cls):
        return request.remote_addr

    @classmethod
    def get_user_by_email(cls, email):
        return User.query.filter_by(email=email).first()

    @classmethod
    @login_required
    def delete_user(cls, user: User):
        try:
            db.session.delete(user)
        except Exception as e:
            raise UserDeletionError(user_id=user.id)

        db.session.commit()
