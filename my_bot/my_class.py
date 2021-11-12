class User:
    users = dict()

    def __init__(self, id):
        self.id = id
        self.users[id] = self
        self.search_data = []

