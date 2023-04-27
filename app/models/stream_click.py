from app.models import *


class StreamClick(db.Model, CrudMixin):
    __id_field__ = 'stream_click_id'
    __session__ = db.session

    # PriKey
    stream_click_id = schema.Column(types.Integer, primary_key=True)

    # ForKey
    fk_news_id = schema.Column(types.Integer, schema.ForeignKey("stream.stream_id"), nullable=False)

    # Tracking
    created = schema.Column(types.DateTime, default=pytz_datetime())

    @classmethod
    def add_stream_click(cls, stream_id: int):
        return cls.create(values={
            'fk_stream_id': stream_id,
            'created': pytz_datetime()
        })
