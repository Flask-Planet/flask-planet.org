import pathlib

from flask import current_app

from app.models import *


class ResourcePage(db.Model, CrudMixin):
    __id_field__ = 'resource_page_id'
    __session__ = db.session

    # PriKey
    resource_page_id = schema.Column(types.Integer, primary_key=True)

    # ForKey
    fk_resource_id = schema.Column(types.Integer, schema.ForeignKey("resource.resource_id"), nullable=False)

    # Data
    order = schema.Column(types.Integer, nullable=False)
    markup = schema.Column(types.NVARCHAR, nullable=False)
    markdown = schema.Column(types.NVARCHAR, nullable=False)
    markdown_og_filename = schema.Column(types.String(512), default=True)
    markdown_safe_filename = schema.Column(types.String(512), default=True)

    # Tracking
    created = schema.Column(types.DateTime, default=pytz_datetime())

    @classmethod
    def delete_by_og_filename(cls, og_filename: str, fk_resource_id: int):
        cls.delete(
            fields={
                'fk_resource_id': fk_resource_id,
                'markdown_og_filename': og_filename
            }
        )

    @classmethod
    def delete_by_id(cls, resource_page_id: int):
        resource_page = cls.get_by_id(resource_page_id)

        upload_location = pathlib.Path(
            pathlib.Path(current_app.root_path) / "uploads" / "resources" / resource_page.fk_resource_id)
        file_location = upload_location / resource_page.markdown_safe_filename
        file_location.unlink(missing_ok=True)

        cls.delete(id_=resource_page_id)

    @classmethod
    def delete_by_resource_id(cls, resource_id: int):
        resource_pages = cls.read(fields={'fk_resource_id': resource_id})

        for resource_page in resource_pages:
            upload_location = pathlib.Path(
                pathlib.Path(current_app.root_path) / "uploads" / "resources" / str(resource_page.fk_resource_id))
            file_location = upload_location / resource_page.markdown_safe_filename
            file_location.unlink(missing_ok=True)

        return cls.delete(fields={
            'fk_resource_id': resource_id,
        })

    @classmethod
    def update_order(cls, resource_page_id, order):
        cls.update(
            values={
                "order": order
            },
            id_=resource_page_id
        )

    @classmethod
    def get_by_resource_id(cls, fk_resource_id: str):
        return cls.read(
            order_by="order",
            fields={'fk_resource_id': fk_resource_id},
            _auto_output=False
        ).first()

    @classmethod
    def get_by_og_filename(cls, og_filename: str):
        return cls.read(
            fields={'markdown_og_filename': og_filename},
            _auto_output=False
        ).first()

    @classmethod
    def count_by_resource_id(cls, fk_resource_id: int):
        query = select(func.count()).where(cls.fk_resource_id == fk_resource_id)
        return cls.__session__.execute(query).scalar() or 0
