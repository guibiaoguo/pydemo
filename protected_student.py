class Student(object):
    """docstring for Student"""
    def __init__(self, name, score,gender):
        super(Student, self).__init__()
        self.__name = name
        self.__score = score
        self.__gender = gender

    def print_score(self):
        print('%s: %s' % (self.__name, self.__score))
    
    def get_name(self):
        return self.__name
    def get_score(self):
        return self.__score
    def set_score(self, score):
        if 0 <= score <= 100:
            self.__score = score
        else:
            raise ValueError('bad score')
    def get_gender(self):
        return self.__gender
    def set_gender(self, gender):
        self.__gender = gender

bart = Student('Bart Student', 59,'male')
#print(bart.__name)
#print(bart._Student__name)
print(bart.get_name())
print(bart.get_score())
bart = Student('Bart',75,'male')
if bart.get_gender() != 'male':
    print('测试失败!')
else:
    bart.set_gender('female')
    if bart.get_gender() != 'female':
        print('测试失败!')
    else:
        print('测试成功!')
