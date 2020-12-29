class Student(object):
    """docstring for Student"""
    def __init__(self):
        super(Student, self).__init__()

    def get_score(self):
        return self._score

    def set_score(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        if value < 0 or value > 100:
            raise ValueError('score must between 0 ~ 100!')
        self._score = value

s = Student()
s.set_score(69)
print(s.get_score())
#s.set_score(9999)

class Student1(object):

    @property
    def score(self):
        return self._score
    
    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        if value < 0 or value > 100:
            raise ValueError("score must between 0 ~ 100")
        self._score = value

s1 = Student1()
s1.score = 60
print(s1.score)
#s1.score = 998

class Screen(object):
    """docstring for Screen"""
    def __init__(self):
        super(Screen, self).__init__()

    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, value):
        self._height = value

    @property
    def resolution(self):
        return self._width * self._height
 
s2 = Screen()
s2.width = 1024
s2.height = 768
print('resolution =', s2.resolution)
if s2.resolution == 786432:
    print('测试通过!')
else:
    print('测试失败!')   