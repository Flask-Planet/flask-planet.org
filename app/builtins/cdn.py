import pathlib

from flask import send_from_directory


def loader(app):
    stream_thumbnail_path = pathlib.Path(pathlib.Path(app.root_path) / "uploads" / "streams")
    news_thumbnail_path = pathlib.Path(pathlib.Path(app.root_path) / "uploads" / "news")
    no_thumbnail_path = pathlib.Path(pathlib.Path(app.root_path) / "theme" / "static" / "img")

    @app.route("/cdn/streams/<stream_id>/<filename>")
    def stream_cdn(stream_id, filename):
        if filename is None or stream_id is None:
            return send_from_directory(directory=no_thumbnail_path, path="no-thumbnail.png")

        file_path = stream_thumbnail_path / str(stream_id) / str(filename)
        folder_path = stream_thumbnail_path / str(stream_id)

        if not file_path.exists():
            return send_from_directory(directory=no_thumbnail_path, path="no-thumbnail.png")

        return send_from_directory(directory=folder_path, path=filename)

    @app.route("/cdn/news/<news_id>/<filename>")
    def news_cdn(news_id, filename: str):
        if filename is None or news_id is None:
            return send_from_directory(directory=no_thumbnail_path, path="no-thumbnail.png")

        file_path = news_thumbnail_path / str(news_id) / str(filename)
        folder_path = news_thumbnail_path / str(news_id)

        if not file_path.exists():
            return send_from_directory(directory=no_thumbnail_path, path="no-thumbnail.png")

        return send_from_directory(directory=folder_path, path=filename)
