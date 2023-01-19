from flask import Flask


def loader(app: Flask):
    pass

    # @app.template_filter('example__hello_world')
    # def example__filter_(value: str) -> str:
    #     from markupsafe import Markup
    #
    #     """
    #     Usage
    #
    #     {{ "World" | example__hello_world }} => Hello World, again!
    #     """
    #     return Markup(f"Hello {value}, again!")
