from app.extensions import bigapp


class User:
    @classmethod
    def get_by_id(cls, user_id):
        return bigapp.model("User").get_by_id(user_id)

    @classmethod
    def check_login(cls, username, password):
        return bigapp.model("User").check_login(username, password)
