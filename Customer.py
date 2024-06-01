from datetime import datetime


class Customer:
    def __init__(self, id, name, address, phone_number, email, dob):
        self.id = id
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.email = email
        self.dob = dob

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "phone_number": self.phone_number,
            "email": self.email,
            "dob": self.dob,
        }

    def get_age(self):
        return datetime.strptime(self.dob, "%d/%m/%Y").year
