from app.models import *


class ResourceTagMembership(db.Model, CrudMixin):
    __id_field__ = 'resource_tag_membership_id'
    __session__ = db.session

    # PriKey
    resource_tag_membership_id = schema.Column(types.Integer, primary_key=True)

    # ForKey
    fk_resource_id = schema.Column(types.Integer, schema.ForeignKey("resource.resource_id"), nullable=False)
    fk_resource_tag_id = schema.Column(types.Integer, schema.ForeignKey("resource_tag.resource_tag_id"), nullable=False)

    # Relationships
    rel_resource = relationship(
        "Resource", back_populates="rel_resource_tag_membership"
    )
    rel_resource_tag = relationship(
        "ResourceTag",
        primaryjoin="ResourceTagMembership.fk_resource_tag_id==ResourceTag.resource_tag_id",
        back_populates="rel_resource_tag_membership"
    )

    @classmethod
    def process_tag_list(cls, resource_id: int, tags: list):
        from .resource_tag import ResourceTag

        for tag in tags:
            if tag == "" or tag is None or tag == " ":
                continue

            logger.debug(f"Tag: {tag}")
            this_tag = ResourceTag.get_by_tag(tag)

            if not this_tag:
                logger.debug("Tag not found, adding tag...")
                this_tag = ResourceTag.add_tag(tag)

            logger.debug(f"Adding tag membership... {this_tag.tag} - {this_tag.resource_tag_id} to {resource_id}")

            cls.add_resource_tag_membership(resource_id, this_tag.resource_tag_id)

    @classmethod
    def add_resource_tag_membership(cls, resource_id: int, resource_tag_id: int):
        return cls.create(values={
            'fk_resource_id': resource_id,
            'fk_resource_tag_id': resource_tag_id
        })

    @classmethod
    def delete_by_resource_id(cls, resource_id: int):
        cls.delete(field=('fk_resource_id', resource_id))
        return
