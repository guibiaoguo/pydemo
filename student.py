class Student(object):
    """docstring for Student"""
    def __init__(self, name, score):
        super(Student, self).__init__()
        self.name = name
        self.score = score

    def print_score(self):
        print('%s: %s' % (self.name, self.score))

    def get_grade(self):
            if self.score >= 90:
                return 'A'
            elif self.score >= 60:
                return 'B'
            else:
                return 'C'

bart = Student('Bart Simpson', 80)
print(bart.name)
print(bart.score)
print(bart.print_score())
lisa = Student('Lisa', 90)
jim = Student('Jim',59)
print(lisa.name, lisa.get_grade())
print(jim.name, jim.get_grade())
bart.age = 8
print(bart.age)
print(jim.age)

        