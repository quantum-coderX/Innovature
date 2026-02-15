class Member:
    def __init__(self, member_id, name, email):
        self.member_id = member_id
        self.name = name
        self.email = email

    def to_dict(self):
        return {
            'member_id': self.member_id,
            'name': self.name,
            'email': self.email
        }

    def __str__(self):
        return f"Member({self.member_id}, {self.name}, {self.email})"