import pathlib


def loader(app):
    from flask import send_from_directory

    @app.route("/cdn/streams/<stream_id>/<filename>")
    def stream_cdn(stream_id, filename):
        stream_thumbnail_path = pathlib.Path(pathlib.Path(app.root_path) / "stream_thumbnails" / stream_id)
        return send_from_directory(stream_thumbnail_path, filename)
