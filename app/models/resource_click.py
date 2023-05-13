from app.models import *


class ResourceClick(db.Model, CrudMixin):
    __id_field__ = 'resource_click_id'
    __session__ = db.session

    # PriKey
    resource_click_id = schema.Column(types.Integer, primary_key=True)

    # ForKey
    fk_resource_id = schema.Column(types.Integer, schema.ForeignKey("resource.resource_id"), nullable=False)

    # Tracking
    created = schema.Column(types.DateTime, default=pytz_datetime())

    @classmethod
    def add_resource_click(cls, resource_id: int):
        return cls.create(values={
            'fk_resource_id': resource_id,
            'created': pytz_datetime()
        })

    @classmethod
    def delete_by_resource_id(cls, resource_id: int):
        return cls.delete(fields={
            'fk_resource_id': resource_id,
        })
