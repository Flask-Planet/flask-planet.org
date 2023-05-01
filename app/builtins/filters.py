def loader(app):
    @app.template_filter("datetime")
    def datetime_filter(value, format_="%Y-%m-%d"):
        if value is None:
            return ""
        return value.strftime(format_)

    @app.template_filter("datetime_local")
    def datetime_local_filter(value, format_="%Y-%m-%dT%H:%M"):
        if value is None:
            return ""
        return value.strftime(format_)

    @app.template_filter("stream_date")
    def stream_date_filter(value, format_="%A %d %B %Y"):
        if value is None:
            return ""
        return value.strftime(format_)

    @app.template_filter("stream_time")
    def stream_date_filter(value, format_="%H:%M"):
        if value is None:
            return ""
        return value.strftime(format_)
