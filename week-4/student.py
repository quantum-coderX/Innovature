class Student:
    def __init__(self, id, name, grade):
        self.id = id
        self.name = name
        self.grade = grade

    def __str__(self):
        return f"{self.id}: {self.name} - {self.grade}"