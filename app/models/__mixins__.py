from app import db


class CRUDMixin:
    """Mixin that adds convenience methods for CRUD (create, read, update, delete)"""

    @classmethod
    def create(
            cls,
            commit: bool = True,
            return_instance: bool = False,
            **kwargs
    ) -> any:

        instance = cls()
        for attr, value in kwargs.items():
            if hasattr(instance, attr):
                setattr(instance, attr, value)

        db.session.add(instance)

        if commit:
            db.session.commit()

        if return_instance:
            db.session.flush()
            return instance

    @classmethod
    def get_by_field(
            cls,
            field: str,
            value: any
    ) -> any:
        """Get by a specified field. Returns None if value not found."""

        return db.session.query(cls).filter_by(**{field: value}).first()

    @classmethod
    def update_by_id(
            cls,
            id_field: str,
            id_value: int,
            commit: bool = True,
            **kwargs
    ) -> None:
        """Update a database entry using the specified id field."""

        instance = cls.get_by_field(id_field, id_value)

        if not instance:
            return

        for attr, value in kwargs.items():
            if hasattr(instance, attr):
                setattr(instance, attr, value)

        if commit:
            db.session.commit()

    @classmethod
    def delete_by_id(
            cls,
            id_field: str,
            id_value: int,
            commit: bool = True
    ) -> None:
        """Delete a database entry using the specified id field"""

        instance = cls.get_by_field(id_field, id_value)

        db.session.delete(instance)

        if commit:
            db.session.commit()
