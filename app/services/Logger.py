
import string
from app import db
from app.main.models import Base
from enum import Enum
from app.services.UserService import UserService
from datetime import datetime
from flask_login import current_user

class EventType(Enum):
    EVENT = "EVENT"
    ERROR = "ERROR"

class Event(Base): 
    
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(128), nullable=False)
    message = db.Column(db.String(256), nullable=False)
    time_stamp = db.Column(db.DateTime, default=datetime.now)
    user_email = db.Column(db.String(256), nullable=True)
    ip_address = db.Column(db.String(128), nullable=False)
class Logger:
    @classmethod
    def logEvent(cls, message: string, type: EventType):
        ip_address = UserService.get_user_ip_address()
        user_email = UserService.get_current_user_email() if current_user else None

        event = Event(
            event_type=type.value, 
            message=message, 
            ip_address=ip_address, 
            user_email=user_email
        )

        db.session.add(event)
        db.session.commit()

    @classmethod
    def get_logs_for_user(cls, email):
        logs = Event.query.filter_by(user_email=email).order_by(Event.time_stamp.desc())
        return logs