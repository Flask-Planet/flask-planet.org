import typing as t

from flask import Markup


def loader(app):
    @app.context_processor
    def author_link_from_user_proc():
        from app.models.user import User

        def author_link_from_user(user_id):
            return User.get_by_id(user_id).author_link or ""

        return dict(author_link_from_user=author_link_from_user)

    @app.context_processor
    def og_tags_proc():
        def og_tags(
                title: t.Optional[str] = None,
                description: t.Optional[str] = None,
                url: t.Optional[str] = None,
                image: t.Optional[str] = None,
                type_: t.Optional[str] = None,
                locale: t.Optional[str] = "en_GB",
        ):
            ogs = []
            if title:
                ogs.append(f'<meta property="og:title" content="{title}" />')
            if description:
                ogs.append(f'<meta property="og:description" content="{description}" />')
            if url:
                ogs.append(f'<meta property="og:url" content="{url}" />')
            if image:
                ogs.append(f'<meta property="og:image" content="{image}" />')
            if type_:
                ogs.append(f'<meta property="og:type" content="{type_}" />')
            if locale:
                ogs.append(f'<meta property="og:locale" content="{locale}" />')

            return Markup("\n".join(ogs))

        return dict(og_tags=og_tags)
