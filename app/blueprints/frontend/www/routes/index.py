from flask import render_template

from app.models.news import News
from app.models.resource import Resource
from app.models.stream import Stream
from .. import bp


@bp.route("/", methods=["GET"])
def index():
    news_ = News.all_newest_first_pages(
        page=1,
        per_page=3,
    )

    streaming_today = Stream.streaming_today()

    resources_ = Resource.all_newest_first_pages(
        page=1,
        per_page=3,
    )

    return render_template(
        bp.tmpl("index.html"),
        news=news_,
        streaming_today=streaming_today,
        resources=resources_,
    )
