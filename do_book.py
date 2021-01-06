import os,json,re,requests,logging
from functools import reduce
from collections import ChainMap
import hashlib,random,time


re_domain = r"(?<=[http|https]://)(((((\d{1,2})|(1\d{2})|(2[0-4]\d)|(25[0-5]))\.){3}((\d{1,2})|(1\d{2})|(2[0-4]\d)|(25[0-5]))(:\d{,8})?)|([.\w-]*))((?=/)|(?!/))"

re_hdomain = r"(?<=)(http|https)://(((((\d{1,2})|(1\d{2})|(2[0-4]\d)|(25[0-5]))\.){3}((\d{1,2})|(1\d{2})|(2[0-4]\d)|(25[0-5]))(:\d{,8})?)|([.\w-]*))((?=/)|(?!/))"

logging.basicConfig(level=logging.ERROR,filename=f'book-{time.strftime("%Y-%m-%d", time.localtime())}.log')

# 获取本地时间
def get_local_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def deleteDuplicate(li):
    func = lambda x, y: x if y in x else x + [y]
    li = reduce(func, [[], ] + li)
    print(li)
    return li

def deleteDuplicateKey(li,key):
    def func(x,y):
        tkey = re.search(re_domain,y.get(key)).group()
        if(tkey in x):
            return x
        else:
            x[tkey] = y
        return x
    li = reduce(func, [{}, ] + li)
    return li

def deleteDuplicateByFor(bookFaillist):
    remove = []
    for i, d1 in enumerate(bookFaillist):
        for j, d2 in enumerate(bookFaillist):
            if d1.get('bookSourceUrl') == d2.get('bookSourceUrl') and i < j:
                remove.append(i)    
    bookFaillistSet = []
    for i,d1 in enumerate(bookFaillist):
        if i not in remove:
            bookFaillistSet.append(d1)
    return bookFaillistSet

def getHKey(x, key):
    return str(x.get(key)).replace('https:','').replace('http:','')

def deleteDuplicateMaxKey(fun, li, key):
    def func(x,y):
        tkey =  fun(y, key)
        if(tkey in x and len(json.dumps(x[tkey])) > len(json.dumps(y))):
            return x
        else:
            x[tkey] = y
        return x
    li = reduce(func, [{}, ] + li)
    return li

def getDkey(x, key):
    turl = re.sub('[^A-Za-z0-9:./]+', '/', x.get(key))
    return re.search(re_domain, turl).group() if re.search(re_domain, turl) else turl

def deleteDuplicateGroup(fun, li, key):
    def func(x,y):
        tkey = fun(y, key)
        if(tkey in x):
            x[tkey].append(y)
            return x
        else:
            x[tkey] = [y]
        return x
    li = reduce(func, [{}, ] + li)
    return li

def deleteDuplicateMD5Key(fun, listBook,key,*args, **kw):
    def func(x,y):
        c = dict(y)
        for k in kw:
            if(k in c):
                c.pop(k)
        c[key] = fun(y, key)
        # c['bookInfoBean'].pop('finalRefreshData')
        # c['bookInfoBean'].pop('name')
        md5 = hashlib.md5()
        md5.update(json.dumps(c).encode('utf-8'))
        tkey = md5.hexdigest()
        # if(c[key].find('99lib.net')>-1):
        #     print(c)
        #     print(y)
        #     print(tkey)
        if(tkey in x):
            return x
        else:
            x[tkey] = y
            # print(c['bookSourceUrl'])
        return x
    listBook = reduce(func, [{}, ] + listBook)
    return listBook


def getDHkey(x, key):
    turl = re.sub('[^A-Za-z0-9:./]+', '/', x.get(key))
    return re.search(re_hdomain, turl).group() if re.search(re_domain, turl) else turl

def getMD5Key(x, key):
    c = dict(x)
    for key1 in key:
        if key1 in x:
            c.pop(key1)
    md5 = hashlib.md5()
    md5.update(json.dumps(c).encode('utf-8'))
    return md5.hexdigest()

def vaildUrl(fun, x, key):
    try:
        url1 = fun(x,key)
        print(url1)
        proxies = {'http': 'http://127.0.0.1:10809', 'https': 'http://127.0.0.1:10809'}
        page = requests.head(url1,proxies=proxies,timeout=2.5);
        return page.status_code == 200
    except Exception as e:
        print(e)
        logging.error(e)
        return False

def jsonToList(fun, path, *args, **kw):
    bookFaillist = []
    bookSuccesslist = []
    keyFaillist = []
    keySuccesslist = []
    group = kw.get('group')
    postfix = kw.get('postfix')
    vaildResult = kw.get('vaildResult')
    def validBook(x):
        flag = True
        # print(x)
        for g in group:
            y = dict(x)
            for g1 in g:
                if (y):
                    y = y.get(g1)
            # print(y)
            if(isinstance(y, str)):
                flag = vaildResult == y if vaildResult == '' else y.find(vaildResult) > -1 and flag
            else:
                flag = True and flag if vaildResult == '' else False and flag
        return flag

    def validNotBook(x):
        return not validBook(x)

    for root, dirs, files in os.walk(path):
        for file in files:
            # print(os.path.join(root,file))
            with open(os.path.join(root,file),'r',encoding='utf-8', errors='ignore') as f:
                dict1 = json.load(f)
                booksFail = list(filter(validBook ,dict1))
                booksSuccess = list(filter(validNotBook,dict1))
                key1 = list(map(lambda x:fun(x, kw.get('key')),booksFail))
                key2 = list(map(lambda x:fun(x, kw.get('key')),booksSuccess))
                # print(key1)
                # print(key2)    
            keyFaillist.extend(key1)
            keySuccesslist.extend(key2)
            bookFaillist.extend(booksFail)
            bookSuccesslist.extend(booksSuccess)
    
    print(f'失败的key列表数量：{len(keyFaillist)}')
    print(f'失败的key列表去重后数量:{len(set(keyFaillist))}')
    print(f'成功的key列表数量：{len(keySuccesslist)}')
    print(f'成功的key列表去重后数量：{len(set(keySuccesslist))}')             
    print(f'失败的列表数量：{len(bookFaillist)}')
    print(f'成功的列表数量: {len(bookSuccesslist)}')    
    
    return keyFaillist, bookFaillist, keySuccesslist, bookSuccesslist

def monkeybook():
        # keyFaillist, bookFaillist, keySuccesslist, bookSuccesslist = jsonToList(getDkey,'fail',key='bookSourceUrl',group=[('ruleBookContent',)],vaildResult='',postfix='.json')
    # keyFaillist1, bookFaillist1, keySuccesslist1, bookSuccesslist1 = jsonToList(getDkey,'legado',key='bookSourceUrl',group=[('ruleContent','content'),('ruleToc','chapterList')],vaildResult='',postfix='.json')
    # print(json.dumps(bookFaillist1, ensure_ascii/*=False,sort_keys=True, indent=4, separators=(',', ':')))
    keyFaillist2, bookFaillist2, keySuccesslist2, bookSuccesslist2 = jsonToList(getDkey,'monkey',key=('bookSourceType','loginUrl','bookSourceGroup','bookSourceName','enable','lastUpdateTime','serialNumber','weight'),group=[('ruleBookContent',),('ruleContentUrl',)],vaildResult='',postfix='')
    # print(json.dumps(bookFaillist2, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':')))
    param = {'bookSourceType':'','loginUrl':'','bookSourceGroup':'','bookSourceName':'','enable':'','lastUpdateTime':'','serialNumber':'','weight':''}
    bookFailSet = list(deleteDuplicateMD5Key(getDkey, bookFaillist2, 'bookSourceUrl', **param).values()); 
    print(len(bookFailSet))
    bookSuccessSet = list(deleteDuplicateMD5Key(getDkey, bookSuccesslist2,'bookSourceUrl', **param).values()); 
    print(len(bookSuccessSet))
    bookSuccessSetGroup = deleteDuplicateGroup(getDkey,bookSuccessSet, 'bookSourceUrl')
    for k,v in bookSuccessSetGroup.items():
        if(len(v) > 4):
            print(f'{k}:{len(v)}')
            # print(json.dumps(v, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':')))
    with open('test/monkeybook/fail11.json','w',encoding='utf-8') as f:
        json.dump(bookFailSet, f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':'))
    bookSuccessSetVaild=list(filter(lambda x: x.get('bookSourceGroup').find('失效') > -1 if x.get('bookSourceGroup') else False,bookSuccessSet))
    bookSuccessSetNotVaild=list(filter(lambda x: x.get('bookSourceGroup').find('失效') < 0 if x.get('bookSourceGroup') else True ,bookSuccessSet))
    print(len(bookSuccessSetVaild))
    print(len(bookSuccessSetNotVaild))
    for i in range(len(bookSuccessSetVaild)//2000 + 1):
        with open(f'monkeybook/fail{i}.json','w',encoding='utf-8') as f:
            json.dump(bookSuccessSetVaild[2000*i:2000*i+2000], f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':'))
    for i in range(len(bookSuccessSetNotVaild)//2000+1):
        print(2000*i)
        with open(f'monkeybook/success{i}.json','w',encoding='utf-8') as f:
            json.dump(bookSuccessSetNotVaild[2000*i:2000*i+2000], f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':')) 

def success(start,step):
    keyFaillist2, bookFaillist2, keySuccesslist2, bookSuccesslist2 = jsonToList(getMD5Key,'test/monkeybook/success',key=('bookSourceType','loginUrl','bookSourceGroup','bookSourceName','enable','lastUpdateTime','serialNumber','weight'),group=[('ruleBookContent',),('ruleContentUrl',)],vaildResult='',postfix='')
    keyFaillist3, bookFaillist3, keySuccesslist3, bookSuccesslist3 = jsonToList(getMD5Key,'monkeybook/success',key=('bookSourceType','loginUrl','bookSourceGroup','bookSourceName','enable','lastUpdateTime','serialNumber','weight'),group=[('ruleBookContent',),('ruleContentUrl',)],vaildResult='',postfix='')
    bookSuccessSet = list(filter(lambda x:getMD5Key(x,('bookSourceType','loginUrl','bookSourceGroup','bookSourceName','enable','lastUpdateTime','serialNumber','weight'))  not in keySuccesslist2,bookSuccesslist3))
    print(len(bookSuccessSet))
    for i in range(start,len(bookSuccessSet)//step+start+1):
        print(step*i)
        with open(f'monkeybook/success{i}.json','w',encoding='utf-8') as f:
            json.dump(bookSuccessSet[step*(i-start):step*(i-start)+step], f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':')) 
    bookSuccessSetGroup = deleteDuplicateGroup(getDkey,bookSuccessSet, 'bookSourceUrl')
    bookFailSet1 = [[] for x in range(15)]
    for k,v in bookSuccessSetGroup.items():
        for i,x in enumerate(v):
            bookFailSet1[i].append(x)
        print(f'{k}:{len(v)}')
            # bookFailSet1.append(v[0])
            # bookFailSet2.append(v[1])
    for i,x in enumerate(bookFailSet1):
        print(len(x))
        with open(f'monkeybook/success4{i}.json','w',encoding='utf-8') as f:
            json.dump(x, f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':')) 
def fail(start,step):
    keyFaillist2, bookFaillist2, keySuccesslist2, bookSuccesslist2 = jsonToList(getMD5Key,'test/monkeybook/fail',key=('bookSourceType','loginUrl','bookSourceGroup','bookSourceName','enable','lastUpdateTime','serialNumber','weight'),group=[('ruleBookContent',),('ruleContentUrl',)],vaildResult='',postfix='')
    keyFaillist3, bookFaillist3, keySuccesslist3, bookSuccesslist3 = jsonToList(getMD5Key,'monkeybook/fail',key=('bookSourceType','loginUrl','bookSourceGroup','bookSourceName','enable','lastUpdateTime','serialNumber','weight'),group=[('ruleBookContent',),('ruleContentUrl',)],vaildResult='',postfix='')
    bookSuccessSet = list(filter(lambda x:getMD5Key(x,('bookSourceType','loginUrl','bookSourceGroup','bookSourceName','enable','lastUpdateTime','serialNumber','weight'))  not in keySuccesslist2,bookSuccesslist3))
    print(len(bookSuccessSet))
    for i in range(start,len(bookSuccessSet)//step+start+1):
        print(step*i)
        with open(f'monkeybook/fail{i}.json','w',encoding='utf-8') as f:
            json.dump(bookSuccessSet[step*(i-start):step*(i-start)+step], f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':')) 
    bookSuccessSetGroup = deleteDuplicateGroup(getDkey,bookSuccessSet, 'bookSourceUrl')
    bookFailSet1 = [[] for x in range(4)]
    for k,v in bookSuccessSetGroup.items():
        for i,x in enumerate(v):
            bookFailSet1[i].append(x)
        print(f'{k}:{len(v)}')
            # bookFailSet1.append(v[0])
            # bookFailSet2.append(v[1])
    for i,x in enumerate(bookFailSet1):
        print(len(x))
        with open(f'monkeybook/fail4{i}.json','w',encoding='utf-8') as f:
            json.dump(x, f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':')) 
    # with open(f'monkeybook/fail35.json','w',encoding='utf-8') as f:
    #     json.dump(bookFailSet2, f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':')) 
def makeDictory(path):
    paths = os.path.split(path)
    pa = ''
    for dic in paths:
        pa = os.path.join(pa, dic)
        if(not os.path.exists(pa)):
            os.makedirs(dic)

def printBookGroup(fun,key,bookFailSet,path,filename,max):
    bookFailSetGroup = deleteDuplicateGroup(fun,bookFailSet, key)
    bookFailSet1 = [[] for x in range(max)]
    for k,v in bookFailSetGroup.items():
        for i,x in enumerate(v):
            bookFailSet1[i].append(x)
        print(f'{k}:{len(v)}')
            # bookFailSet1.append(v[0])
            # bookFailSet2.append(v[1])
    
    for i,x in enumerate(bookFailSet1):
        print(len(x))
        with open(f'{path}/{filename}/{filename}{i}.json','w',encoding='utf-8') as f:
            json.dump(x, f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':')) 

def monkeybook(start,step):
    keyFaillist2, bookFaillist2, keySuccesslist2, bookSuccesslist2 = jsonToList(getMD5Key,'monkey',key=('bookSourceType','loginUrl','bookSourceGroup','bookSourceName','enable','lastUpdateTime','serialNumber','weight'),group=[('ruleBookContent',),('ruleContentUrl',)],vaildResult='',postfix='')
    param = {'bookSourceType':'','loginUrl':'','bookSourceGroup':'','bookSourceName':'','enable':'','lastUpdateTime':'','serialNumber':'','weight':''}
    bookFailSet = list(deleteDuplicateMD5Key(getDkey, bookFaillist2, 'bookSourceUrl', **param).values()); 
    print(len(bookFailSet))
    bookSuccessSet = list(deleteDuplicateMD5Key(getDkey, bookSuccesslist2,'bookSourceUrl', **param).values()); 
    print(len(bookSuccessSet))
    # printBookGroup(bookFailSet,'fail',4)
    # bookSuccessSetGroup = deleteDuplicateGroup(getDkey,bookSuccessSet, 'bookSourceUrl')
    # bookFailSet1 = [[] for x in range(100)]
    # for k,v in bookSuccessSetGroup.items():
    #     for i,x in enumerate(v):
    #         bookFailSet1[i].append(x)
    #     print(f'{k}:{len(v)}')
    #         # bookFailSet1.append(v[0])
    #         # bookFailSet2.append(v[1])
    # for i,x in enumerate(bookFailSet1):
    #     print(len(x))
    #     with open(f'success2/success{i}.json','w',encoding='utf-8') as f:
    #         json.dump(x, f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':')) 
def monkeyFail():
    keyFaillist2, bookFaillist2, keySuccesslist2, bookSuccesslist2 = jsonToList(getDkey,'success2/success',key='bookSourceUrl',group=[('ruleBookContent',),('ruleContentUrl',)],vaildResult='',postfix='')
    keyFaillist3, bookFaillist3, keySuccesslist3, bookSuccesslist3 = jsonToList(getDkey,'success2/fail',key='bookSourceUrl',group=[('ruleBookContent',),('ruleContentUrl',)],vaildResult='',postfix='')
    keyFaillist4, bookFaillist4, keySuccesslist4, bookSuccesslist4 = jsonToList(getDkey,'success3',key='bookSourceUrl',group=[('ruleContent',),('ruleContentUrl',)],vaildResult='',postfix='')
    keyFaillist5, bookFaillist5, keySuccesslist5, bookSuccesslist5 = jsonToList(getDkey,'fail3.1',key='bookSourceUrl',group=[('ruleContent',),('ruleContentUrl',)],vaildResult='',postfix='')
    bookFailSet = list(filter(lambda x:getDkey(x,'bookSourceUrl') not in keySuccesslist2 and getDkey(x,'bookSourceUrl') not in keyFaillist4 and getDkey(x,'bookSourceUrl') not in keyFaillist5,bookFaillist3))
    print(len(bookFailSet))
    with open(f'success2/fail.json','w',encoding='utf-8') as f:
        json.dump(bookFailSet, f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':')) 
def booksource():
    keyFaillist2, bookFaillist2, keySuccesslist2, bookSuccesslist2 = jsonToList(getDkey,'success2.0',key='bookSourceUrl',group=[('bookSourceGroup',)],vaildResult='失效',postfix='')
    keyFaillist3, bookFaillist3, keySuccesslist3, bookSuccesslist3 = jsonToList(getDkey,'success3/success',key='bookSourceUrl',group=[('bookSourceGroup',)],vaildResult='失效',postfix='')
    param = {'bookSourceType':'','loginUrl':'','bookSourceGroup':'','bookSourceName':'','enable':'','lastUpdateTime':'','serialNumber':'','weight':''}
    bookFailSet = list(deleteDuplicateMD5Key(getDkey, bookFaillist2, 'bookSourceUrl', **param).values()); 
    print(len(bookFailSet))
    bookSuccessSet = list(deleteDuplicateMD5Key(getDkey, bookSuccesslist2,'bookSourceUrl', **param).values()); 
    print(len(bookSuccessSet))
    with open(f'success2/success.json','w',encoding='utf-8') as f:
        json.dump(bookSuccesslist2, f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':'))   
    with open(f'success2/fail.json','w',encoding='utf-8') as f:
        json.dump(bookFaillist2, f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':'))   
    with open(f'success2/fail1.json','w',encoding='utf-8') as f:
        json.dump(bookFailSet, f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':'))
    # printBookGroup(getDkey,'bookSourceUrl',bookFailSet,'success2.1','fail',29)
    printBookGroup(getDkey,'bookSourceUrl',bookSuccessSet, 'success2.1', 'success', 33)
    bookSuccess=list(deleteDuplicateMaxKey(getHKey,bookSuccessSet,'bookSourceUrl').values())
    print(len(bookSuccess))
    bookFail=list(deleteDuplicateMaxKey(getHKey,list(filter(lambda x:getDkey(x,'bookSourceUrl') not in keySuccesslist2 and getDkey(x,'bookSourceUrl') not in keySuccesslist3,bookFailSet)),'bookSourceUrl').values())
    print(len(bookFail))
    printBookGroup(getDkey,'bookSourceUrl',bookFail,'success2.1','fail',29)
    with open(f'success2.1/fail.json','w',encoding='utf-8') as f:
        json.dump(bookFail, f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':'))
    with open(f'success2.1/success.json','w',encoding='utf-8') as f:
        json.dump(bookSuccess, f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':'))    
def myBookShelf():
    keyFaillist2, bookFaillist2, keySuccesslist2, bookSuccesslist2 = jsonToList(getHKey,'myBookShelf',key='noteUrl',group=[('bookSourceGroup',)],vaildResult='失效',postfix='')
    param = {'group':'','variableMap':'','variable':'','lastChapterName':'','chapterListSize':'','finalDate':'','finalRefreshData':'','durChapter':'','durChapterName':'','durChapterPage':'','isLoading':'','replaceEnable':'','hasUpdate':''}
    bookSuccessSet = list(deleteDuplicateMD5Key(getDkey, bookSuccesslist2,'noteUrl', **param).values()); 
    print(len(bookSuccessSet))
    with open(f'success2.1/myBookShelf.json','w',encoding='utf-8') as f:
        json.dump(bookSuccessSet, f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':'))
    printBookGroup(getHKey,'noteUrl',bookSuccessSet,'success2.1','myBookShelf',2)
def bookShelf():
    keyFaillist2, bookFaillist2, keySuccesslist2, bookSuccesslist2 = jsonToList(getHKey,'bookshelf',key='bookUrl',group=[('bookSourceGroup',)],vaildResult='失效',postfix='')
    param = {'intro':'','name':'','group':'','latestChapterTitle':'','durChapterIndex':'','lastCheckCount':'','durChapterPos':'','wordCount':'','totalChapterNum':'','durChapterTitle':'','type':'','useReplaceRule':'','readConfig':'','originOrder':'','canUpdate':'','durChapterTime':'','lastCheckTime':'','latestChapterTime':'','order':''}
    bookSuccessSet = list(deleteDuplicateMD5Key(getDkey, bookSuccesslist2,'bookUrl', **param).values()); 
    print(len(bookSuccessSet))
    # with open(f'success2.1/myBookShelf.json','w',encoding='utf-8') as f:
    #     json.dump(bookSuccessSet, f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':'))
    printBookGroup(getHKey,'bookUrl',bookSuccessSet,'success3','bookShelf',2)

def bookShelfExist():
    keyFaillist2, bookFaillist2, keySuccesslist2, bookSuccesslist2 = jsonToList(getHKey,'bookshelf/1',key='bookUrl',group=[('bookSourceGroup',)],vaildResult='失效',postfix='')
    keyFaillist3, bookFaillist3, keySuccesslist3, bookSuccesslist3 = jsonToList(getHKey,'bookshelf/2',key='bookUrl',group=[('bookSourceGroup',)],vaildResult='失效',postfix='')
    param = {'intro':'','name':'','group':'','latestChapterTitle':'','durChapterIndex':'','lastCheckCount':'','durChapterPos':'','wordCount':'','totalChapterNum':'','durChapterTitle':'','type':'','useReplaceRule':'','readConfig':'','originOrder':'','canUpdate':'','durChapterTime':'','lastCheckTime':'','latestChapterTime':'','order':''}
    bookSuccessSet = list(deleteDuplicateMD5Key(getDkey, bookSuccesslist2,'bookUrl', **param).values()); 
    print(len(bookSuccessSet))
    # with open(f'success2.1/myBookShelf.json','w',encoding='utf-8') as f:
    #     json.dump(bookSuccessSet, f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':'))
    printBookGroup(getHKey,'bookUrl',bookSuccessSet,'success3','bookShelf',2)
    bookSuccessSet = list(filter(lambda x: getHKey(x,'bookUrl') not in keySuccesslist2,bookSuccesslist3))
    print(len(bookSuccessSet))
    with open(f'success3/bookShelf1.json','w',encoding='utf-8') as f:
        json.dump(bookSuccessSet, f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':'))
if __name__ == '__main__': 
    # monkeybook(1,1000)
    # success(41,350)
    # fail(21,210)

    # booksource()
    keyFaillist2, bookFaillist2, keySuccesslist2, bookSuccesslist2 = jsonToList(getDkey,'success2.1/fail',key='bookSourceUrl',group=[('bookSourceGroup',)],vaildResult='失效',postfix='')
    keyFaillist3, bookFaillist3, keySuccesslist3, bookSuccesslist3 = jsonToList(getDkey,'fail3',key='bookSourceUrl',group=[('ruleBookContent',)],vaildResult='',postfix='')
    param = {}
    bookFailSet = list(deleteDuplicateMD5Key(getDkey, bookFaillist2, 'bookSourceUrl', **param).values()); 
    print(len(bookFailSet))
    # printBookGroup(getDkey,'bookSourceUrl',bookFailSet,'success3','fail',5)
    bookFailVaildSet = list(filter(lambda x:vaildUrl(getDHkey,x,'bookSourceUrl') or vaildUrl(getDHkey,x,'searchUrl'),bookFailSet))
    with open(f'success2.1/failvalid1.json','w',encoding='utf-8') as f:
        json.dump(bookFailVaildSet, f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':'))