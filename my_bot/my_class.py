class User:
    users = dict()

    def __init__(self, id):
        self.id = id
        User.add_user(id, self)
        self.search_data = []

    @classmethod
    def add_user(cls, id, user):
        cls.users[id] = user

    @classmethod
    def get_user(cls, id):
        if id not in cls.users.keys():
            a = cls(id)
            return a
        else:
            return cls.users[id]
