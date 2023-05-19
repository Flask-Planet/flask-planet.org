from app.models import *


class System(db.Model, CrudMixin):
    __id_field__ = 'system_id'
    __session__ = db.session

    # PriKey
    system_id = schema.Column(types.Integer, primary_key=True)

    # Data
    terms_and_conditions_markdown = schema.Column(types.NVARCHAR, nullable=False)
    terms_and_conditions_markup = schema.Column(types.NVARCHAR, nullable=False)
    privacy_policy_markdown = schema.Column(types.NVARCHAR, nullable=False)
    privacy_policy_markup = schema.Column(types.NVARCHAR, nullable=False)

    @classmethod
    def get_first(cls):
        query = select(cls).order_by(cls.system_id.asc()).limit(1)
        return cls.__session__.scalars(query).first()
