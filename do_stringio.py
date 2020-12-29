from io import StringIO
f = StringIO()
f.write('Hello')
f.write(' ')
f.write('World!')
print(f.getvalue())
f1 = StringIO('Hello!\nHi!\nGoodbye!')
while True:
    s = f1.readline()
    if s == '':
        break
    print(s.strip())