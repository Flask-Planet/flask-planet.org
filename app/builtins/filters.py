def loader(app):
    @app.template_filter("datetime")
    def datetime_filter(value, format="%Y-%m-%d"):
        return value.strftime(format)
