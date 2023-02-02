from app.models import *


class User(db.Model):
    # PriKey
    user_id = schema.Column(types.Integer, primary_key=True)

    # Data
    username = schema.Column(types.String(256), nullable=False)
    password = schema.Column(types.String(512), nullable=False)
    salt = schema.Column(types.String(4), nullable=False)
    private_key = schema.Column(types.String(256), nullable=False)
    display_name = schema.Column(types.String(64), nullable=False)
    disabled = schema.Column(db.Boolean, default=False)
    permissions = schema.Column(types.JSON, nullable=True, default={})

    # Tracking
    created = schema.Column(types.DateTime, default=pytz_datetime())

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
