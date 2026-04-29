class Teacher:
    def __init__(self, id, name, subject):
        self.id = id
        self.name = name
        self.subject = subject

    def __repr__(self):
        return f"Teacher({self.id}, {self.name}, {self.subject})"
