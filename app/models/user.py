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
    disabled = schema.Column(db.Boolean, default=False)
    permissions = schema.Column(types.JSON, nullable=True, default={})

    # Tracking
    created = schema.Column(types.DateTime, default=pytz_datetime())

    # Author
    author = schema.Column(types.String(128), nullable=True)
    author_link = schema.Column(types.String(1024), nullable=True)

    # Relationships
    rel_resource = relationship("Resource", back_populates="rel_user")

    def save(self):
        return self.__session__.commit()

    def set_new_password(self, new_password):
        new_salt = Auth.generate_salt()
        self.salt = new_salt
        self.password = Auth.sha_password(new_password, new_salt)
        return self.save()

    @classmethod
    def get_by_id(cls, user_id):
        return cls.read(fields={'user_id': user_id}, _auto_output=False).first()

    @classmethod
    def get_by_username(cls, username):
        return cls.read(fields={'username': username}, _auto_output=False).first()

    @classmethod
    def check_login(cls, username, password):
        user = cls.get_by_username(username)
        if user:
            if Auth.auth_password(
                    password,
                    user.password,
                    user.salt
            ):
                return user

        return None

    @classmethod
    def add_new_user(
            cls,
            username,
            password,
            author,
            author_link,
    ):
        salt = Auth.generate_salt()
        password = Auth.sha_password(password, salt)
        return cls.create(values={
            'username': username,
            'password': password,
            'salt': salt,
            'private_key': Auth.generate_private_key(salt),
            'author': author,
            'author_link': author_link,
            'created': pytz_datetime()
        })
