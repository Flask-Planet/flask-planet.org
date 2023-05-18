def loader(app):
    @app.context_processor
    def utility_processor():
        from app.model_connectors.user import User

        def author_link_from_user(user_id):
            return User.get_by_id(user_id).author_link or ""

        return dict(author_link_from_user=author_link_from_user)


