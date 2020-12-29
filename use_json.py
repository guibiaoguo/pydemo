import json

print("Json模块提供了四个功能：dumps、dump、loads、load")
d = dict(name='Bob', age=20, score=88)
print(json.dumps(d))
print("json dumps把数据类型转换成字符串 dump把数据类型转换成字符串并存储在文件中  loads把字符串转换成数据类型  load把文件打开从字符串转换成数据类型")
json_str = '{"age": 20, "score": 88, "name": "Bob"}'
print(json.loads(json_str))

class Student(object):
    """docstring for Student"""
    def __init__(self, name, age, score):
        super(Student, self).__init__()
        self.name = name
        self.age = age
        self.score = score
    
def student2dict(std):
    return {
        'name': std.name,
        'age': std.age,
        'score': std.score
    }

s = Student('Bob', 20, 88)
print(json.dumps(s, default=student2dict))
print(json.dumps(s, default=lambda obj: obj.__dict__))

obj = dict(name='小明', age=20)
s = json.dumps(obj, ensure_ascii=True)
print(s)