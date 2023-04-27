from flask_sqlalchemy.pagination import Pagination

from app.models import *
from app.models.resource_tag import ResourceTag
from app.models.resource_tag_membership import ResourceTagMembership


class Resource(db.Model, CrudMixin):
    __id_field__ = 'resource_id'
    __session__ = db.session

    # PriKey
    resource_id = schema.Column(types.Integer, primary_key=True)

    # ForKey
    fk_user_id = schema.Column(types.Integer, schema.ForeignKey("user.user_id"), nullable=False)

    # Data
    slug = schema.Column(types.String(128), nullable=False, unique=True)
    title = schema.Column(types.String(128), nullable=False)
    summary = schema.Column(types.String(500), nullable=True)

    # Viewable
    viewable = schema.Column(types.Boolean, default=False)
    auto_viewable = schema.Column(types.Boolean, default=False)
    go_viewable_on = schema.Column(types.DateTime, nullable=True)

    # Tracking
    created = schema.Column(types.DateTime, default=pytz_datetime())

    # Relationships
    rel_user = relationship("User", back_populates="rel_resource")

    rel_resource_tag_membership = relationship(
        "ResourceTagMembership",
        primaryjoin="Resource.resource_id==ResourceTagMembership.fk_resource_id",
        cascade="all, delete"
    )

    rel_resource_pages = relationship(
        "ResourcePage",
        primaryjoin="Resource.resource_id==ResourcePage.fk_resource_id",
        order_by="ResourcePage.order",
        cascade="all, delete"
    )

    rel_resource_clicks = relationship(
        "ResourceClick",
        primaryjoin="Resource.resource_id==ResourceClick.fk_resource_id",
        cascade="all, delete"
    )

    def add_click(self):
        from .resource_click import ResourceClick
        ResourceClick.add_resource_click(self.resource_id)

    @classmethod
    def get_by_id(cls, resource_id):
        return cls.read(id_=resource_id)

    @classmethod
    def get_by_slug(cls, slug):
        return cls.read(fields={'slug': slug}, _auto_output=False).first()

    @classmethod
    def get_tags_by_id(cls, resource_id):
        from .resource_tag_membership import ResourceTagMembership
        result = ResourceTagMembership.read(fields={'fk_resource_id': resource_id})
        if result:
            return [tag.rel_resource_tag.tag for tag in result]
        return []

    @classmethod
    def search_by_title(cls, title):
        query = select(cls).order_by(desc(cls.created)).where(cls.title.ilike(f"%{title}%"))  # type: ignore
        return cls.__session__.execute(query).scalars().all()

    @classmethod
    def search_by_title_pages(cls, title, page: int = 1, per_page: int = 20, tag: str = None):
        if tag:
            query = select(cls).order_by(desc(cls.created)).where(cls.rel_resource_tag_membership.any(  # type: ignore
                ResourceTagMembership.fk_resource_tag_id == ResourceTag.get_by_tag(tag).resource_tag_id
            )).where(cls.title.ilike(f"%{title}%"))  # type: ignore
            return db.paginate(query, page=page, per_page=per_page)
        query = select(cls).order_by(desc(cls.created)).where(cls.title.ilike(f"%{title}%"))  # type: ignore
        return db.paginate(query, page=page, per_page=per_page)

    @classmethod
    def all_newest_first(cls):
        logger.debug("Getting all resources newest first...")
        return cls.read(all_rows=True, order_by="created", order_desc=True)

    @classmethod
    def all_newest_first_pages(cls, page: int = 1, per_page: int = 20, tag: str = None) -> Pagination:
        if tag:
            query = select(cls).order_by(desc(cls.created)).where(cls.rel_resource_tag_membership.any(  # type: ignore
                ResourceTagMembership.fk_resource_tag_id == ResourceTag.get_by_tag(tag).resource_tag_id
            ))
            logger.debug(f"Getting all resources newest first with tag {tag}...")
            return db.paginate(query, page=page, per_page=per_page)
        query = select(cls).order_by(desc(cls.created))  # type: ignore
        logger.debug("Getting all resources newest first...")
        return db.paginate(query, page=page, per_page=per_page)

    @classmethod
    def all_oldest_first(cls):
        return cls.read(all_rows=True, order_by="created")

    @classmethod
    def add_new_resource(cls, **kwargs):
        logger.debug("Adding new resource...")
        return cls.create(values=kwargs, wash_attributes=True)

    @classmethod
    def get_clicks(cls, resource_id):
        return len(cls.get_by_id(resource_id).rel_resource_clicks)
