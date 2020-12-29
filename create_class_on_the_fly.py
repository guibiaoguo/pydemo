from hello import Hello

h = Hello()
h.hello()
print(type(Hello))
print(type(h))

def fn(self, name='world'):
    print('Hello, %s.' %name)

Hello1 = type('Hello1', (object,), dict(hello=fn))
h1 = Hello1()
print(h1.hello())
print(type(Hello1))
print(type(h1))
