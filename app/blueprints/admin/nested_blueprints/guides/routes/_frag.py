from app import bigapp
from .. import bp


@bp.post("/frag/tags-datalist")
def frag_tags_datalist():
    q_tags = bigapp.model("GuideTag").get_all()
    return "OK"
