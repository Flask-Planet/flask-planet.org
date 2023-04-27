from app import bigapp
from .. import bp
from app.models.resource_tag import ResourceTag

@bp.post("/frag/tags-datalist")
def frag_tags_datalist():
    q_tags = ResourceTag.get_all()
    return "OK"
