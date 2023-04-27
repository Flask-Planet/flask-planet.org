from flask_bigapp import Auth

from app.models import *


class User(db.Model, CrudMixin):
    __id_field__ = 'user_id'
    __session__ = db.session

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

    # Relationships
    rel_resource = relationship("Resource", back_populates="rel_user")

    @classmethod
    def get_by_id(cls, user_id):
        return cls.get_by_field('user_id', user_id)

    @classmethod
    def get_by_username(cls, username):
        return cls.get_by_field('username', username)

    @classmethod
    def add_new_user(cls, username, password, display_name):
        salt = Auth.generate_salt()
        password = Auth.sha_password(password, salt)
        return cls.create(values={
            'username': username,
            'password': password,
            'salt': salt,
            'private_key': Auth.generate_private_key(salt),
            'display_name': display_name,
            'created': pytz_datetime()
        })
