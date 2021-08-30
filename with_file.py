import os,shutil

f = open('e:/workspace/pydemo/err.py', 'r')
print(f.read())
f.close()

with open('e:/workspace/pydemo/fact.py', 'r') as f:
    print(f.read())

with open('e:/workspace/pydemo/fact.py', 'r') as f:
    for line in f:
        print(line)

# with open('test.jpg', 'rb') as f:
#     print(f.read())

with open('test_gbk.json', 'r') as f:
    print(f.read())

with open('test.txt', 'w') as f:
    f.write('Hello, world!')

print("当前目录：", os.getcwd())
print("当前目录里有什么：", os.listdir())

os.makedirs("project", exist_ok=True)
print(os.path.exists("project"))

if os.path.exists("user/mofan"):
    print("user exist")
else:
    os.makedirs("user/mofan")
    print("user created")
print(os.listdir("user"))

if os.path.exists("user/mofan"):
    os.removedirs("user/mofan")
    print("user removed")
else:
    print("user not exist")

os.makedirs("user/mofan1", exist_ok=True)
with open("user/mofan1/a.txt", "w") as f:
    f.write("nothing")

try:
   os.removedirs("user/mofan1")  # 这里会报错
except Exception as e:
    print(e)

shutil.rmtree("user/mofan1")
#shutil.rmtree("user/mofanpy")
print(os.listdir("user"))

os.makedirs("user/mofan", exist_ok=True)
#os.rename("user/mofan", "user/mofanpy")
print(os.listdir("user"))

os.makedirs("user/mofan2", exist_ok=True)
with open("user/mofan2/a.txt", "w") as f:
    f.write("nothing")
print(os.path.isfile("user/mofan2/a.txt")) # True
print(os.path.exists("user/mofan2/a.txt")) # True
print(os.path.isdir("user/mofan2/a.txt")) # False
print(os.path.isdir("user/mofan2"))  # True

def copy(path):
    filename = os.path.basename(path)   # 文件名
    dir_name = os.path.dirname(path)    # 文件夹名
    new_filename = "new_" + filename    # 新文件名
    return os.path.join(dir_name, new_filename) # 目录重组
print(copy("user/mofan/a.txt"))

def copy(path):
    dir_name, filename = os.path.split(path)
    new_filename = "new_" + filename    # 新文件名
    return os.path.join(dir_name, new_filename) # 目录重组
print(copy("user/mofan/a.txt"))

