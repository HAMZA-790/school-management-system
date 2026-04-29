class Student:
    def __init__(self, id, name, student_class, age):
        self.id = id
        self.name = name
        self.student_class = student_class
        self.age = age

    def __repr__(self):
        return f"Student({self.id}, {self.name}, {self.student_class})"
