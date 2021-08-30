import os,json,re,requests,logging
from functools import reduce
from collections import ChainMap
import hashlib,random

re_domain = r"(?<=[http|https]://)(((((\d{1,2})|(1\d{2})|(2[0-4]\d)|(25[0-5]))\.){3}((\d{1,2})|(1\d{2})|(2[0-4]\d)|(25[0-5]))(:\d{,8})?)|([.\w-]*))((?=/)|(?!/))"

re_hdomain = r"(?<=)(http|https)://(((((\d{1,2})|(1\d{2})|(2[0-4]\d)|(25[0-5]))\.){3}((\d{1,2})|(1\d{2})|(2[0-4]\d)|(25[0-5]))(:\d{,8})?)|([.\w-]*))((?=/)|(?!/))"

logging.basicConfig(level=logging.ERROR,filename='group.log')

def deleteDuplicate(li):
    func = lambda x, y: x if y in x else x + [y]
    li = reduce(func, [[], ] + li)
    print(li)
    return li

def deleteDuplicateKey(li,key):
    def func(x,y):
        tkey = str(y.get(key)).replace('https:','').replace('http:','') 
        if(tkey in x and len(json.dumps(x[tkey])) > len(json.dumps(y))):
            return x
        else:
            x[tkey] = y
        return x
    li = reduce(func, [{}, ] + li)
    return li

def deleteDuplicateGroup(li,key):
    def func(x,y):
        tkey = re.search(re_domain,y.get(key)).group() if re.search(re_domain, y.get(key)) else y.get(key)
        if(tkey in x):
            x[tkey].append(y)
            return x
        else:
            x[tkey] = [y]
        return x
    li = reduce(func, [{}, ] + li)
    return li

def deleteDuplicateMD5Key(li):
    def func(x,y):
        c = dict(y)
        c['bookSourceName'] = ''
        c['bookSourceGroup'] = ''
        c['lastUpdateTime'] = ''
        c['customOrder'] = ''
        c['enabled'] = True
        c['enabledExplore'] = True
        c['bookSourceComment'] = ''
        turl = re.sub('[^A-Za-z0-9:./]+', '/', y.get('bookSourceUrl'))
        c['bookSourceUrl'] = re.search(re_domain, turl).group() if re.search(re_domain, turl) else turl
        md5 = hashlib.md5()
        md5.update(json.dumps(c).encode('utf-8'))
        tkey = md5.hexdigest()
        if(tkey in x):
            return x
        else:
            x[tkey] = y
            # print(c['bookSourceUrl'])
        return x
    li = reduce(func, [{}, ] + li)
    return li

def deleteDuplicate(bookFaillist):
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



def jsonToList(path,key,group):
    bookFaillist = []
    bookSuccesslist = []
    key1list = []
    key2list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            with open(os.path.join(root,file),'r',encoding='utf-8', errors='ignore') as f:
                dict = json.load(f)
                booksFail = sorted(list(filter(lambda x: x.get(group) == None ,dict)), key= lambda x: re.search(re_domain,x.get(key)).group() if re.search(re_domain, x.get(key)) else x.get(key))
                booksSuccess = sorted(list(filter(lambda x: x.get(group) ,dict)), key= lambda x: x.get('bookSourceUrl'))
                key1 = list(map(lambda x : re.search(re_domain,x.get(key)).group() if re.search(re_domain, x.get(key)) else x.get(key),booksFail))
                key2 = list(map(lambda x : re.search(re_domain,x.get(key)).group() if re.search(re_domain, x.get(key)) else x.get(key),booksSuccess))
                # print(key1)
                # print(key2)    
            key1list.extend(key1)
            key2list.extend(key2)
            bookFaillist.extend(booksFail)
            bookSuccesslist.extend(booksSuccess)
    return key1list, bookFaillist, key2list, bookSuccesslist

def vaildUrl(book):
    try:
        url1 = re.search(re_hdomain,book.get('bookSourceUrl')).group()
        print(url1)
        page = requests.head(url1);
        return page.status_code == 200
    except Exception as e:
        print(e)
        logging.error(e)
        return False

def jsontoM3U8(path,wfile):
    keylist2, bookFaillist2, key2list2, bookSuccesslist2 = jsonToList(os.path.join(path,wfile),'bookSourceUrl','ruleBookContent.content')
    print(len(keylist2))
    print(len(set(keylist2)))
    print(len(key2list2))
    print(len(set(key2list2)))             
    print(len(bookFaillist2))
    print(len(bookSuccesslist2))
    # input("开始过滤数据")
    bookSuccessSet = list(deleteDuplicateMD5Key(bookFaillist2).values());
    print(len(bookSuccessSet))
    bookSuccessSetGroup = deleteDuplicateGroup(bookSuccessSet, 'bookSourceUrl')
    for k,v in bookSuccessSetGroup.items():
        logging.error(f'{k}:{len(v)}')
    bookSuccessSet1 = list(deleteDuplicateKey(bookSuccessSet, 'bookSourceUrl').values());
    print(len(bookSuccessSet1))

    with open('success6.json','w',encoding='utf-8') as f:
        json.dump(bookSuccessSet, f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':'))    

    with open('success8.json','w',encoding='utf-8') as f:
        json.dump(bookSuccessSet1, f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':'))

    # bookFaillistSet = list(filter(lambda x: re.search(re_domain,x.get('bookSourceUrl')).group() not in key1,deleteDuplicateMD5Key(bookFaillist,'bookSourceUrl').values()))
    # bookSuccesslistSet = list(filter(lambda x: re.search(re_domain,x.get('bookSourceUrl')).group() not in key,deleteDuplicateMD5Key(bookSuccesslist, 'bookSourceUrl').values()))
    # print(len(bookFaillistSet))
    # print(len(bookSuccesslistSet))
    
    # bookSuccessRList = []
    # bookSuccessRList.extend(bookFaillistSet)
    # bookSuccessRList.extend(bookSuccesslistSet)
    # bookSuccessRListSet = list(filter(vaildUrl,bookSuccessRList))
    # print(len(bookSuccessRListSet))
    # print(len(bookSuccesslistSet))
    # with open('success3/success1.json','w',encoding='utf-8') as f:
    #     json.dump(bookSuccessSet[0:6500], f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':'))
    # with open('success3/success2.json','w',encoding='utf-8') as f:
    #     json.dump(bookSuccessSet[6500:13000], f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':'))
    # with open('success3/success3.json','w',encoding='utf-8') as f:
    #     json.dump(bookSuccessSet[13000:], f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':'))
if __name__ == '__main__':
    # toM3U8("E:\\workspace\\hikerView\\tv\\202006")
    # readM3U8("C:\\Users\\bill\\Desktop\\Crack\\直播-online.m3u8")
    jsontoM3U8("e:\\workspace\\pydemo","legado")