import os,json,re,requests,logging
from functools import reduce
from collections import ChainMap

re_domain = r"(?<=[http|https]://)(((((\d{1,2})|(1\d{2})|(2[0-4]\d)|(25[0-5]))\.){3}((\d{1,2})|(1\d{2})|(2[0-4]\d)|(25[0-5]))(:\d{,8})?)|([.\w-]*))((?=/)|(?!/))"

re_hdomain = r"(?<=)(http|https)://(((((\d{1,2})|(1\d{2})|(2[0-4]\d)|(25[0-5]))\.){3}((\d{1,2})|(1\d{2})|(2[0-4]\d)|(25[0-5]))(:\d{,8})?)|([.\w-]*))((?=/)|(?!/))"

logging.basicConfig(level=logging.ERROR,filename='failed.log')

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
        proxies = {'http': 'http://localhost:7890', 'https': 'http://localhost:7890'}
        page = requests.head(url1,proxies=proxies);
        return page.status_code == 200
    except Exception as e:
        print(e)
        logging.error(e)
        return False

def jsontoM3U8(path,wfile):
    key1list, bookFaillist, key2list, bookSuccesslist = jsonToList(os.path.join(path,'fail'),'bookSourceUrl','ruleBookContent')
    keylist1, bookFaillist1, key2list1, bookSuccesslist1 = jsonToList(os.path.join(path,'success'),'bookSourceUrl','ruleBookContent')
    keylist2, bookFaillist2, key2list2, bookSuccesslist2 = jsonToList(os.path.join(path,'legado'),'bookSourceUrl','ruleBookContent.content')
    keylist3, bookFaillist3, key2list3, bookSuccesslist3 = jsonToList(os.path.join(path,'fail3'),'bookSourceUrl','ruleBookContent')
    keylist4, bookFaillist4, key2list4, bookSuccesslist4 = jsonToList(os.path.join(path,'fail3.1'),'bookSourceUrl','ruleBookContent.content')

    print(len(key1list))
    print(len(set(key1list)))
    print(len(key2list))
    print(len(set(key2list)))             
    print(len(bookFaillist))
    print(len(bookSuccesslist))

    print(keylist1)
    print(len(set(keylist1)))
    print(len(key2list1))
    print(len(set(key2list1)))             
    print(len(bookFaillist1))
    print(len(bookSuccesslist1))

    print(len(keylist2))
    print(len(set(keylist2)))
    print(len(key2list2))
    print(len(set(key2list2)))             
    print(len(bookFaillist2))
    print(len(bookSuccesslist2))

    print(len(keylist4))
    print(len(set(keylist4)))
    print(len(key2list4))
    print(len(set(key2list4)))             
    print(len(bookFaillist4))
    print(len(bookSuccesslist4))

    key = []
    key.extend(keylist1)
    key.extend(key2list1)
    key.extend(key2list2)
    key.extend(keylist2)
    
    key2 = []
    # key2.extend(keylist3)
    # key2.extend(key2list3)
    
    key1 = []
    key1.extend(key)
    key1.extend(key2list)
    key1.extend(keylist4)
    bookFaillistSet = list(filter(lambda x: re.search(re_domain,x.get('bookSourceUrl')).group() not in key1, deleteDuplicateKey(bookFaillist,'bookSourceUrl').values()))
    bookSuccesslistSet = list(filter(lambda x: re.search(re_domain,x.get('bookSourceUrl')).group() not in key, deleteDuplicateKey(bookSuccesslist, 'bookSourceUrl').values()))
    print(len(bookFaillistSet))
    print(len(bookSuccesslistSet))
    
    bookSuccessRList = []
    bookSuccessRList.extend(bookFaillistSet)
    bookSuccessRList.extend(bookSuccesslistSet)
    # input('请允许')
    # bookSuccessRListSet = list(filter(vaildUrl,bookSuccessRList))
    # print(len(bookSuccessRListSet))
    with open('fail8.json','w',encoding='utf-8') as f:
        json.dump(bookFaillistSet, f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':'))
    with open('fail9.json','w',encoding='utf-8') as f:
        json.dump(bookSuccesslistSet, f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':'))
    # with open('fail10.json','w',encoding='utf-8') as f:
    #     json.dump(bookSuccessRListSet, f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':'))
if __name__ == '__main__':
    # toM3U8("E:\\workspace\\hikerView\\tv\\202006")
    # readM3U8("C:\\Users\\bill\\Desktop\\Crack\\直播-online.m3u8")
    jsontoM3U8("e:\\workspace\\pydemo","fail")