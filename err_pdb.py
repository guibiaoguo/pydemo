import pdb

s = '4'
n = int(s)
print(10 / n)

s = '0'
n = int(s)
pdb.set_trace() # 运行到这里会自动暂停
print(10 / n)