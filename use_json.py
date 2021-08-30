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

data = {"filename": "f1.txt", "create_time": "today", "size": 111}
j = json.dumps(data)
print(j)
print(type(j))

data = {"filename": "f1.txt", "create_time": "today", "size": 111}
with open("data.json", "w") as f:
    json.dump(data, f)

print("直接当纯文本读：")
with open("data.json", "r") as f:
    print(f.read())

print("用 json 加载了读：")
with open("data.json", "r") as f:
    new_data = json.load(f)
print("字典读取：", new_data["filename"])

class File:
    def __init__(self, name, create_time, size):
        self.name = name
        self.create_time = create_time
        self.size = size
    
    def change_name(self, new_name):
        self.name = new_name

data = File("f4.txt", "now", 222)
# 存，会报错
with open("data.json", "w") as f:
    try:
        json.dump(data, f)
    except Exception as e:
        print(e)
