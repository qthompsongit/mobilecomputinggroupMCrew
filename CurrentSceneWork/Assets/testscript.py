class Test():
    def __init__(self, name):
        self.name = name
    def display(self):
        with open("mytestfile.txt", "w+") as testfile:
            testfile.write("this is test")
        return "Hi, " + self.name

