import pathlib

from flask import send_from_directory
from flask import url_for


def loader(app):
    stream_thumbnail_path = pathlib.Path(pathlib.Path(app.root_path) / "uploads" / "streams")
    news_thumbnail_path = pathlib.Path(pathlib.Path(app.root_path) / "uploads" / "news")

    @app.context_processor
    def news_cdn_processor():
        def news_cdn(news_id, filename):
            if filename is None or news_id is None:
                return url_for("theme.static", filename="img/no-thumbnail.png")

            this_path = news_thumbnail_path / str(news_id) / filename
            if not this_path.exists():
                return url_for("theme.static", filename="img/no-thumbnail.png")

            return url_for("news_cdn", news_id=news_id, filename=filename)

        return dict(news_cdn=news_cdn)

    @app.context_processor
    def stream_cdn_processor():
        def stream_cdn(stream_id, filename):
            if filename is None or stream_id is None:
                return url_for("theme.static", filename="img/no-thumbnail.png")

            this_path = stream_thumbnail_path / str(stream_id) / filename

            if not this_path.exists():
                return url_for("theme.static", filename="img/no-thumbnail.png")

            return url_for("stream_cdn", stream_id=stream_id, filename=filename)

        return dict(stream_cdn=stream_cdn)

    @app.route("/cdn/streams/<stream_id>/<filename>")
    def stream_cdn(stream_id, filename):
        full_path = stream_thumbnail_path / str(stream_id)
        return send_from_directory(directory=full_path, path=filename)

    @app.route("/cdn/news/<news_id>/<filename>")
    def news_cdn(news_id, filename: str):
        full_path = news_thumbnail_path / str(news_id)
        return send_from_directory(directory=full_path, path=filename)
