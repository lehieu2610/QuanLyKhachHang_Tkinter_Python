import json

import os

BASE_DIR = os.path.dirname(__file__)


class Authorization:
    def __init__(self):
        self.user_list = []
        self.read_data()

    def read_data(self):

        with open(
            os.path.join(BASE_DIR, "user.json"),
            "r",
        ) as file:
            data = json.load(file)

        for user in data:
            self.user_list.append(user)

    def login(self, username, password):

        for user in self.user_list:
            if username == user["username"] and user["password"] == password:
                return user["role"]
        return None
