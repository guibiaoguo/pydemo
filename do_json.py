import os,json,re,requests
from functools import reduce
from collections import ChainMap

re_domain = r"(?<=[http|https]://)(((((\d{1,2})|(1\d{2})|(2[0-4]\d)|(25[0-5]))\.){3}((\d{1,2})|(1\d{2})|(2[0-4]\d)|(25[0-5]))(:\d{,8})?)|([.\w-]*))((?=/)|(?!/))"

re_hdomain = r"(?<=)(http|https)://(((((\d{1,2})|(1\d{2})|(2[0-4]\d)|(25[0-5]))\.){3}((\d{1,2})|(1\d{2})|(2[0-4]\d)|(25[0-5]))(:\d{,8})?)|([.\w-]*))((?=/)|(?!/))"

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
                booksFail = list(filter(lambda x: x.get(group) == None ,dict))
                booksSuccess = list(filter(lambda x: x.get(group) ,dict))
                key1 = list(map(lambda x : re.search(re_domain,x.get(key)).group(),booksFail))
                key2 = list(map(lambda x : re.search(re_domain,x.get(key)).group(),booksSuccess))
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
        return False

def jsontoM3U8(path,wfile):
    key1list, bookFaillist, key2list, bookSuccesslist = jsonToList(os.path.join(path,'fail'),'bookSourceUrl','ruleBookContent')
    keylist1, bookFaillist1, key2list1, bookSuccesslist1 = jsonToList(os.path.join(path,'success'),'bookSourceUrl','ruleBookContent')
    print(len(key1list))
    print(len(set(key1list)))
    print(len(key2list))
    print(len(set(key2list)))             
    print(len(bookFaillist))
    print(len(bookSuccesslist))
    key = []
    key.extend(keylist1)
    key.extend(key2list1)
    key1 = []
    key1.extend(key)
    key1.extend(key2list)
    bookFaillistSet = list(filter(lambda x: re.search(re_domain,x.get('bookSourceUrl')).group() not in key1,deleteDuplicateKey(bookFaillist,'bookSourceUrl').values()))
    bookSuccesslistSet = list(filter(lambda x: re.search(re_domain,x.get('bookSourceUrl')).group() not in key,deleteDuplicateKey(bookSuccesslist, 'bookSourceUrl').values()))
    print(len(bookFaillistSet))
    print(len(bookSuccesslistSet))
    
    # bookSuccessRList = []
    # bookSuccessRList.extend(bookFaillistSet)
    # bookSuccessRList.extend(bookSuccesslistSet)
    # bookSuccessRListSet = list(filter(vaildUrl,bookSuccessRList))
    # print(len(bookSuccessRListSet))
    # print(len(bookSuccesslistSet))
    with open('fail1.json','w',encoding='utf-8') as f:
        json.dump(bookFaillistSet, f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':'))
    with open('fail2.json','w',encoding='utf-8') as f:
        json.dump(bookSuccesslistSet, f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':'))
    # with open('fail3.json','w',encoding='utf-8') as f:
    #     json.dump(bookSuccessRListSet, f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':'))
if __name__ == '__main__':
    # toM3U8("E:\\workspace\\hikerView\\tv\\202006")
    # readM3U8("C:\\Users\\bill\\Desktop\\Crack\\直播-online.m3u8")
    jsontoM3U8("e:\\workspace\\pydemo","fail")