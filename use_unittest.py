def my_div(a, b):
    return a / b
try:
    my_div(1,0)
except Exception as e:
    print(e)

import unittest

class TestFunc(unittest.TestCase):
    def test_div(self):
        self.assertEqual(my_div(2,1), 2)
        self.assertEqual(my_div(2,-1), -2)
    def test_zero_div(self):
        # 这里后面我填了一个 1 纯粹是为了占一个位置，2/0 != 1，你知道的，
        # 后面我们再介绍更优雅的写法
        self.assertEqual(my_div(2,0), 1)   
#unittest.main()

def my_func(a):
    return None

class TestFunc(unittest.TestCase):
    def test_func(self):
        self.assertEqual(my_func(1), 2)   
        self.assertEqual(my_func(-1), 3)
        for i in range(-100, 100):
            if i == 1 or i == -1:
                continue
            self.assertEqual(my_func(i), 1)

#unittest.main()

def my_func1(a):
    if a == 1:
        return 2
    elif a == -1:
        return 3
    else:
        return 1

def my_func2(b):
    if b != "yes":
        raise ValueError("you can only say yes!")
    else:
        return True

class TestFunc(unittest.TestCase):
    def test_func1(self):
        self.assertEqual(my_func1(1), 2)   
        self.assertEqual(my_func1(-1), 3)
        for i in range(-100, 100):
            if i == 1 or i == -1:
                continue
            self.assertEqual(my_func1(i), 1)
    
    def test_func2(self):
        self.assertTrue(my_func2("yes"))
        with self.assertRaises(ValueError):
            my_func2("nononono")

unittest.main()

"""[summary]

assert  含义
assertEqual(a, b)   a == b
assertNotEqual(a, b)    a != b
assertTrue(condition)   condition 是不是 True
assertFalse(condition)  condition 是不是 False
assertGreater(a, b) a > b
assertGreaterThan(a, b) a >= b
assertLess(a, b)    a < b
assertLessEqual(a, b)   a <= b
assertIs(a, b)  a is b，a 和 b 是不是同一对象
assertIsNot(a, b)   a is not b，a 和 b 是不是不同对象
assertIsNone(a) a is None，a 是不是 None
assertIsNotNone(a)  a is not None，a 不是 None？
assertIn(a, b)  a in b, a 在 b 里面？
assertNotIn(a, b)   a not in b，a 不在 b 里？
assertRaises(err)   通常和 with 一起用，判断 with 里的功能是否会报错（上面练习有用到过）
[description]

Arguments:
    a {[type]} -- [description]
    b)a / b try(1,0) except Exception as e(e)  import unittest  class TestFunc(unittest.TestCase)test_div(self)(my_div(2,1) {[type]} -- [description]
    2) self.assertEqual(my_div(2,-1) {[type]} -- [description]
    1) #unittest.main()  def my_func(a)None  class TestFunc(unittest.TestCase)test_func(self)(my_func(1) {[type]} -- [description]
    2) self.assertEqual(my_func(-1) {[type]} -- [description]
    2) self.assertEqual(my_func1(-1) {[type]} -- [description]
    1)  def test_func2(self)(my_func2("yes")) with self.assertRaises(ValueError)("nononono")  unittest.main( {[type]} -- [description]

Keyword Arguments:
    -2) def test_zero_div(self): # 这里后面我填了一个 1 纯粹是为了占一个位置，2/0 ! {[type]} -- [description] (default: {1，你知道的， # 后面我们再介绍更优雅的写法 self.assertEqual(my_div(2,0)})
    3) for i in range(-100, 100)i {[type]} -- [description] (default: {})
    1)  #unittest.main()  def my_func1(a)a {[type]} -- [description] (default: {})
    3) for i in range(-100, 100)i {[type]} -- [description] (default: {})
""" 

class TestFunc(unittest.TestCase):
    def test_func1(self):
        self.assertEqual(my_func1(1), 2)   
        self.assertEqual(my_func1(-1), 3)
        for i in range(-100, 100):
            if i == 1 or i == -1:
                continue
            self.assertEqual(my_func1(i), 1)
    
    def test_func2(self):
        self.assertTrue(my_func2("yes"))
        with self.assertRaises(ValueError):
            my_func2("nononono")

# 定义一个 suite 替换 unittext.main()
suite = unittest.TestSuite()
suite.addTest(TestFunc('test_func1'))
unittest.TextTestRunner().run(suite)