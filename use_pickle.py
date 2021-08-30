import pickle

d = dict(name='Bob', age=20, score=88)

print(pickle.dumps(d))
f = open('dump.txt', 'wb')
pickle.dump(d, f)
f.close()

f = open('dump.txt', 'rb')
d = pickle.load(f)
f.close()
print(d)

#序列化

class File:
    def __init__(self, name, create_time, size):
        self.name = name
        self.create_time = create_time
        self.size = size
    
    def change_name(self, new_name):
        self.name = new_name

data = File("f2.txt", "now", 222)
# 存
with open("data.pkl", "wb") as f:
    pickle.dump(data, f)
# 读
with open("data.pkl", "rb") as f:
    read_data = pickle.load(f)
print(read_data.name)
print(read_data.size)

class File:
    def __init__(self, name, create_time, size):
        self.name = name
        self.create_time = create_time
        self.size = size
        self.file = open(name, "w")

data = File("f3.txt", "now", 222)
# pickle 存，会报错
with open("data.pkl", "wb") as f:
    try:
        pickle.dump(data, f)
    except Exception as e:
        print(e)

class File:
    def __init__(self, name, create_time, size):
        self.name = name
        self.create_time = create_time
        self.size = size
        self.file = open(name, "w")

    def __getstate__(self):
        # pickle 出去需要且能被 pickle 的信息
        pickled = {"name": self.name, "create_time": self.create_time, "size": self.size}
        return pickled

    def __setstate__(self, pickled_dict):
        # unpickle 加载回来，重组 class
        self.__init__(
            pickled_dict["name"], pickled_dict["create_time"], pickled_dict["size"])

data = File("f3.txt", "now", 222)
# 存
with open("data.pkl", "wb") as f:
    pickle.dump(data, f)
# 读
with open("data.pkl", "rb") as f:
    read_data = pickle.load(f)
print(read_data.name)
print(read_data.size)

