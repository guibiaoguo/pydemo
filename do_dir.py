import os

print(os.name)
#print(os.uname())
print(os.environ)
print(os.environ.get('PATH'))
print(os.path.abspath('.'))
print(os.path.join('E:\\workspace\\pydemo', 'testdir'))
os.mkdir('E:\\workspace\\pydemo\\testdir')
os.rmdir('E:\\workspace\\pydemo\\testdir')

print(os.path.split('E:\\workspace\\pydemo'))

with open('test.txt', 'w') as f:
    f.write('Hello, world!')

os.rename('test.txt','test1.txt')

os.remove('test1.txt')

print([x for x in os.listdir('.') if os.path.isdir(x)])

print([x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1] == '.py'])

def listfile():
    path = os.path.abspath('.')
    taret_str = input('')
    for root, dirs, files in os.walk(path):
        for file in files:
            if taret_str in file:
                print(os.path.join(root,file))

listfile()                