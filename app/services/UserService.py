from app.auth.models import User
from flask import request
from flask_login import current_user, login_required

class UserService:

    # @login_required
    @classmethod
    def get_current_user_email(cls):
        if current_user.get_id() is not None:
            user = User.query.filter_by(id=current_user.get_id()).first()
            if user:
                return user.email

    @classmethod
    def get_user_ip_address(cls):
        return request.remote_addr