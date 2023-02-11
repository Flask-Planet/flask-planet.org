from app.models import *
from app.models.__mixins__ import CRUDMixin


class Tracking(db.Model, CRUDMixin):
    # PriKey
    tracking_id = schema.Column(types.Integer, primary_key=True)

    # Data
    ip = schema.Column(types.String(128), nullable=False)
    url = schema.Column(types.String(512), nullable=False)
