from app.models import *


class ResourceTag(db.Model, CrudMixin):
    __id_field__ = 'resource_tag_id'
    __session__ = db.session

    # PriKey
    resource_tag_id = schema.Column(types.Integer, primary_key=True)

    # Data
    tag = schema.Column(types.String(128), nullable=False)

    # Relationships
    rel_resource_tag_membership = relationship(
        "ResourceTagMembership",
        primaryjoin="ResourceTag.resource_tag_id==ResourceTagMembership.fk_resource_tag_id",
        cascade="all, delete"
    )

    @classmethod
    def get_all_tags(cls):
        return [tag.tag for tag in cls.read(all_rows=True)]

    @classmethod
    def get_by_list_of_tags(cls, tags: list):
        return db.session.execute(
            select(cls).where(cls.tag.in_(tags))
        ).all()

    @classmethod
    def get_by_tag(cls, tag):
        return cls.read(fields={'tag': tag}, _auto_output=False).first()

    @classmethod
    def add_tag(cls, tag: str):
        return cls.create(values={'tag': tag})
