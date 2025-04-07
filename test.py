class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def print_info(self):
        print(f"{self.name}: {self.age}")


    def __str__(self):
        return f"{self.name}: {self.age}"


p1 = Person("John", 10)
print(p1)
p1.print_info()
