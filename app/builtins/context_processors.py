def loader(app):
    @app.context_processor
    def utility_processor():
        def format_price(amount, currency="€"):
            return f"{amount:.2f}{currency}"

        return dict(format_price=format_price)
