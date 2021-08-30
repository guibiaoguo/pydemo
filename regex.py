# -*- coding: utf-8 -*-

import re,time,json

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

print(re.search(re_domain,"http://m.31xs.com/22").group())
print(re.search(re_domain,"https://m.3li.cc").group())
print(re.search(re_hdomain,"https://www.qidian.com 🌸444444"))
print(re.search(re_domain,re.sub('[^A-Za-z0-9:/.]+', '/','https://www.qidian.com/🌸444444')))
print(re.search(re_domain,re.sub('[^A-Za-z0-9:/.]+', '/','https://www.qidian.com-By')))
turl = re.sub('/.*', '', 'https://www.qidian.com/🌸aaa')
print(turl)
print(re.search(re_domain,'https://www.b5200.net/By'))
print(len({'a':1}))
print("" != None)
file = re.findall(r'\d+',"https://m.sinodan.cc/view/34818.html");
print(file)

print(re.sub('jīng(?=液)','精','员的jīng液'))
print(re.sub('aì(?=液)','爱','身的aì液源'))
print(re.sub('(?<=鸡)ba','巴','鸡ba早已'))
print(re.sub('(?<=鸡)baca','巴操','的鸡baca进来'))
print(re.sub('gui(?=头)','龟','假鸡bagui头小'))
print(re.sub('ròu(?=棒|洞)','肉','的鸡baròu棒充'))
print(re.sub('shè(?=精)','射','的鸡bashè精过'))
print(re.sub('xiā(?=穴)','小','xiā穴'))
print(re.sub('sā[o]*(?=穴)','骚','妙的sā穴又'))
print(re.sub('y[iīíǐì]*n(?=唇|道|蒂|户|囊|毛|茎)','阴','己的yin道中'))
print(re.sub('y[i]*n(?=水|荡)','淫','晶的yin水'))
print(re.sub('y[i]*n(?=水|荡)','淫','起了yn荡的'))
print(re.sub('xìng(?=奴|具)','性','xìng奴隶'))
print(re.sub('nǎi(?=子)','奶','她的nǎi子'))
print(re.sub('(?<=玉)rǔ|rǔ(?=房|头|峰|沟|汁)','乳','嫩大rǔ房颤'))
print(re.sub('mī(?=穴)','蜜','我的mī穴'))
print(re.sub('l[à|a]*ng(?=穴)','浪','的小làang穴口'))
print(re.sub('xiōng','胸','xiōng前晃'))
print(re.sub('yīnjīng','阴茎','在yīnjīng根部'))
print(re.sub('ca','操','好好caca你'))
print(re.sub('Bī','逼','骚Bīca死我'))
print(re.sub('(?<=玉|巨|双)rǔ|rǔ(?=房|头|峰|沟|汁)','乳','她玉rǔ上的'))

file = re.findall(r'(\d+)\.html',"http://hdyp.net/1/1975/24065.html");
print(re.sub('\\d+\\.html',"257651_2.html","http://hdyp.net/1/1975/24065.html"))
print(file)
print(re.match(r'[+-] ','厦'))
print(re.match(r'[+-] [^\u4e00-\u9fa5]','+ 回'))
print(re.match(r'[+-] ','- 大'))
print(re.sub(r'[+-] |[\s]|．','','+ 下\n\n\n\xa0\xa0\xa0\xa0．． \n'))
print(re.sub(r'[^\u4e00-\u9fa5]','','10头办公'))
str1="#11234#大于#23324#"
print(str1.split('#'))

print(re.sub('#0407334288#','涛','波#0407334288#汹涌'))
start = None
print(2 if start else 3)
file="34788.txt"
start = 34788
def add(num,start):
    return (int(num) - start)
file = file if start == None else re.sub(r'(\d+)',lambda x:f"{int(x.group(1)) - start}",file)
print(file)
cc = "波#0407334288,!?.。#汹yina-zāáǎàōóǒòēéěèīíǐìūúǔùüǖǘǚǜńňǹḿmɡ涌__"
print(cc)
cc = re.sub('_','',cc)
print(cc)
cc = re.sub('#','_',cc)
print(cc)
cc = re.sub(r'[\W+]', '', cc)
print(cc)
cc = re.sub('_','#',cc)
print(cc)

# content.append(f"result=`{cc}`;\n")
# with open(os.path.join("book/大雄5","diff.json"),'r',encoding='utf-8', errors='ignore') as f:
#     dict1 = json.load(f)
#     print(len(dict1))
#     content.append("m=[];n=[];function x(a,b){m.push(a);n.push(b);}\n")
#     for k,v in dict1.items():
#         content.append(f"x(/<img src=\"\\/toimg\\/data\\/{k}.png\">/gi,\"{v}\");\n")
# content.append("for(i in n){result=result.replace(m[i],n[i])}\n")
# with open(os.path.join("book/大雄5","diff.js"),'w',encoding='utf-8', errors='ignore') as f:
#     f.writelines(content)

av = "magnet:?xt=urn:btih:CEDD3CE823D8D6F408FDFD51C6B3DC63FA666D6C&dn=heyzo-1773-C"
tt = re.match(r'.*dn=(.*)',av)
print(tt)
print(tt.group(1))
tv = "[无码高清] ATID-407 从小被最差劲的继父侵犯长大的夏目彩春正准备和爱人结婚童年的噩梦又找上门来了"
tc = re.findall(r'^\[[有|无]码高清\] (.*?) ',tv)
print(tc)
tz = re.findall(r'\[.*?\] (.*?) ',tv)
print(tz[0])
tm = "【】SNIS-712 素人初解禁！！RIONファン感謝祭 素中文字幕人男性10人とヤリまくり10本番"
print(tm.find("中文字幕") > 0)
print("gc:{"+tm+"}")
print(re.findall(r'\[.*\] (.*?) ',"[] SGSR-222 ナンパされたエッチな素人女性たち ガチ友達の前で痴態を晒すも思わず感じ濡れる女の子たち 4時間"))

# matching string
pattern1 = "cat"
pattern2 = "bird"
string = "dog runs to cat"
print(pattern1 in string)
print(pattern2 in string)

# regular expression
print(re.search(pattern1, string))
print(re.search(pattern2, string))

# multiple patterns ("run" or "ran")
ptn = r"r[au]n"
print(re.search(ptn, string))
print(re.search(r"r[A-Z]n", string))
print(re.search(r"r[a-z]n", string))
print(re.search(r"r[0-9]n", "dog r2ns to cat"))
print(re.search(r"r[0-9a-z]n", "dog runs to cat"))
"""\d : 任何数字
\D : 不是数字
\s : 任何 white space, 如 [\t\n\r\f\v]
\S : 不是 white space
\w : 任何大小写字母, 数字和 _ [a-zA-Z0-9_]
\W : 不是 \w
\b : 空白字符 (只在某个字的开头或结尾)
\B : 空白字符 (不在某个字的开头或结尾)
\\ : 匹配 \
. : 匹配任何字符 (除了 \n)
^ : 匹配开头
$ : 匹配结尾
? : 前面的字符可有可无"""

# \d : decimal digit
print(re.search(r"r\dn", "run r4n"))           # <_sre.SRE_Match object; span=(4, 7), match='r4n'>
# \D : any non-decimal digit
print(re.search(r"r\Dn", "run r4n"))           # <_sre.SRE_Match object; span=(0, 3), match='run'>
# \s : any white space [\t\n\r\f\v]
print(re.search(r"r\sn", "r\nn r4n"))          # <_sre.SRE_Match object; span=(0, 3), match='r\nn'>
# \S : opposite to \s, any non-white space
print(re.search(r"r\Sn", "r\nn r4n"))          # <_sre.SRE_Match object; span=(4, 7), match='r4n'>
# \w : [a-zA-Z0-9_]
print(re.search(r"r\wn", "r\nn r4n"))          # <_sre.SRE_Match object; span=(4, 7), match='r4n'>
# \W : opposite to \w
print(re.search(r"r\Wn", "r\nn r4n"))          # <_sre.SRE_Match object; span=(0, 3), match='r\nn'>
# \b : empty string (only at the start or end of the word)
print(re.search(r"\bruns\b", "dog runs to cat"))    # <_sre.SRE_Match object; span=(4, 8), match='runs'>
# \B : empty string (but not at the start or end of a word)
print(re.search(r"\B runs \B", "dog   runs  to cat"))  # <_sre.SRE_Match object; span=(8, 14), match=' runs '>
# \\ : match \
print(re.search(r"runs\\", "runs\ to me"))     # <_sre.SRE_Match object; span=(0, 5), match='runs\\'>
# . : match anything (except \n)
print(re.search(r"r.n", "r[ns to me"))         # <_sre.SRE_Match object; span=(0, 3), match='r[n'>
# ^ : match line beginning
print(re.search(r"^dog", "dog runs to cat"))   # <_sre.SRE_Match object; span=(0, 3), match='dog'>
# $ : match line ending
print(re.search(r"cat$", "dog runs to cat"))   # <_sre.SRE_Match object; span=(12, 15), match='cat'>
# ? : may or may not occur
print(re.search(r"Mon(day)?", "Monday"))       # <_sre.SRE_Match object; span=(0, 6), match='Monday'>
print(re.search(r"Mon(day)?", "Mon"))          # <_sre.SRE_Match object; span=(0, 3), match='Mon'>

string1 = """
dog runs to cat.
I run to dog.
"""
print(re.search(r"^I", string1))                 # None
print(re.search(r"^I", string1, flags=re.M))     # <_sre.SRE_Match object; span=(18, 19), match='I'>

# * : occur 0 or more times
print(re.search(r"ab*", "a"))             # <_sre.SRE_Match object; span=(0, 1), match='a'>
print(re.search(r"ab*", "abbbbb"))        # <_sre.SRE_Match object; span=(0, 6), match='abbbbb'>

# + : occur 1 or more times
print(re.search(r"ab+", "a"))             # None
print(re.search(r"ab+", "abbbbb"))        # <_sre.SRE_Match object; span=(0, 6), match='abbbbb'>

# {n, m} : occur n to m times
print(re.search(r"ab{2,10}", "a"))        # None
print(re.search(r"ab{2,10}", "abbbbb"))   # <_sre.SRE_Match object; span=(0, 6), match='abbbbb'>

match = re.search(r"(\d+), Date: (.+)", "ID: 021523, Date: Feb/12/2017")
print(match.group())                   # 021523, Date: Feb/12/2017
print(match.group(1))                  # 021523
print(match.group(2))                  # Date: Feb/12/2017

match = re.search(r"(?P<id>\d+), Date: (?P<date>.+)", "ID: 021523, Date: Feb/12/2017")
print(match.group('id'))                # 021523
print(match.group('date'))              # Date: Feb/12/2017

# findall
print(re.findall(r"r[ua]n", "run ran ren"))    # ['run', 'ran']

# | : or
print(re.findall(r"(run|ran)", "run ran ren")) # ['run', 'ran']\\

# replace re.sub
print(re.sub(r"r[au]ns", "catches", "dog runs to cat"))     # dog catches to cat

#split re.split

print(re.split(r"[,;\.]", "a;b,c.d;e"))             # ['a', 'b', 'c', 'd', 'e']

#compile
compiled_re = re.compile(r"r[ua]n")
print(compiled_re.search("dog ran to cat"))  # <_sre.SRE_Match object; span=(4, 7), match='ran'>

