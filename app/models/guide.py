from app.models import *


class Guide(db.Model):
    # PriKey
    guide_id = schema.Column(types.Integer, primary_key=True)

    # ForKey
    fk_account_id = schema.Column(types.Integer, schema.ForeignKey("account.account_id"), nullable=False)

    # Data
    slug = schema.Column(types.String(128), nullable=False)
    html = schema.Column(types.BLOB, nullable=False)
    tags = schema.Column(types.JSON, nullable=True, default={})

    # Tracking
    created = schema.Column(types.DateTime, default=pytz_datetime())

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
