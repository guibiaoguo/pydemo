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
