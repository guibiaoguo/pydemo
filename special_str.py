class Student(object):
    """docstring for Student"""
    def __init__(self, name):
        super(Student, self).__init__()
        self.name = name

    def __str__(self):
        return "Student object (name: %s)" %self.name    

print(Student('Michael'))

