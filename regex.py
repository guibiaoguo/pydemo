import re,requests

s = r'ABC\-001'
print(re.match(r'^\d{3}\-\d{3,8}$', '010-12345'))
print(re.match(r'^\d{3}\-\d{3,8}$', '010 12345'))

test = '用户输入的字符串'
if re.match(r'正则表达式', test):
    print('ok')
else:
    print('failed')

print('a b   c'.split(' '))
print(re.split(r'\s+','a b   c'))
print(re.split(r'[\s\,]+', 'a,b, c  d'))
print(re.split(r'[\s\,\;]+', 'a,b;; c  d'))

m = re.match(r'^(\d{3})-(\d{3,8})$', '010-12345')
print(m)
print(m.group(0))
print(m.group(1))
print(m.group(2))

t = '19:05:30'
m = re.match(r'^(0[0-9]|1[0-9]|2[0-3]|[0-9])\:(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]|[0-9])\:(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]|[0-9])$', t)
print(m.groups())

print(re.match(r'^(\d+)(0*)$', '102300').groups())
print(re.match(r'^(\d+?)(0*)$', '102300').groups())

re_telephone = re.compile(r'^(\d{3})-(\d{3,8})$')
print("正则提前编译")
print(re_telephone.match('010-12345').groups())
print(re_telephone.match('010-8086').groups())

def is_valid_email(addr):
    if re.match((r'^([\w\d\_\.]+)@(\w+).(\w+)$'),addr):
        return True
    else:
        return False

# 测试:
assert is_valid_email('someone@gmail.com')
assert is_valid_email('bill.gates@microsoft.com')
assert not is_valid_email('bob#example.com')
assert not is_valid_email('mr-bob@example.com')
print('ok')

def name_of_email(addr):
    m = re.match(r'^<?(\w+\s*\w*)>?(\s*\w*)@(\w+).(\w+)$',addr) 
    if m:
        return m.group(1)

# 测试:
assert name_of_email('<Tom Paris> tom@voyager.org') == 'Tom Paris'
assert name_of_email('tom@voyager.org') == 'tom'
print('ok')
print("域名提取测试！")

re_domain = r"(?<=[http|https]://)(((((\d{1,2})|(1\d{2})|(2[0-4]\d)|(25[0-5]))\.){3}((\d{1,2})|(1\d{2})|(2[0-4]\d)|(25[0-5]))(:\d{,8})?)|([.\w-]*))((?=/)|(?!/))"
re_hdomain = r"(?<=)(http|https)://(((((\d{1,2})|(1\d{2})|(2[0-4]\d)|(25[0-5]))\.){3}((\d{1,2})|(1\d{2})|(2[0-4]\d)|(25[0-5]))(:\d{,8})?)|([.\w-]*))((?=/)|(?!/))"

print(re.search(re_domain,"http://m.31xs.com").group())
print(re.search(re_domain,"https://m.3li.cc").group())
print(re.search(re_hdomain,"https://m.3li.cc").groups())
print(requests.head("http://www.lwtxt.cc"))
x.get(key)).group() if re.match(re_domain, x.get(key)) else x.get(key)