# -*- coding: utf-8 -*-
import re,os,json,time,requests
from functools import reduce
from bs4 import BeautifulSoup
import difflib
import pytesseract
from PIL import Image
import shutil

def download(domain, page_url, chapterTag, nextPageTag, contentTag, nextContentTag, path):
    pinyinKeys = []
    pinyinKeys1 = []
    chapterList = []
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    makeDictory(path)
    while True:
        try:
            get_page=requests.get(page_url,headers=headers,timeout=3.5);
            print(page_url)
            soup = BeautifulSoup(str(get_page.content,'utf-8',errors='ignore'),'lxml')
            chapter=soup.select(chapterTag)
            nextPage=soup.select(nextPageTag)
            endPage = soup.select('.endPage')
            # print(chapter)
            print(nextPage)
            chapterList.extend(chapter)
            if(len(nextPage) > 0 and nextPage[0]['href'] != endPage[0]['href']):
                page_url = f"{domain}{nextPage[0]['href']}"
            else:
                break
        except Exception as e:
            time.sleep(2)
            print(e)
            continue
    # print(chapterList)
    print(len(chapterList))
    chapter = chapterList.pop()
    while True:
        try:
            chapter_url = f"{domain}{chapter.a['href']}"
            file = re.findall(r'(\d+)\.html',chapter_url)[0]
            print(file)
            if (os.path.exists(os.path.join(path,f"{file}.txt"))):
                if(len(chapterList) == 0):
                    break
                else:
                    chapter = chapterList.pop()
                continue
            content = ''
            while True:
                try:
                    print(chapter_url)
                    get_page=requests.get(chapter_url, headers=headers, timeout=4.5);
                    soup = BeautifulSoup(re.sub('<img src="\\/toimg\\/data\\/(.*?)\\.png"\\/>',lambda x: f"#{x.group(1)}#",str(get_page.content,'utf-8',errors='ignore')),'lxml')
                    content += soup.select(contentTag)[0].get_text()
                    if(nextContentTag == None):
                        break
                    nextPage=soup.select(nextContentTag)
                    print(nextPage)
                    if(len(nextPage) > 0):
                        chapter_url = re.sub('\\d+\\.html',nextPage[0]['href'],f"{domain}{chapter.a['href']}");
                    else:
                        break
                except Exception as e:
                    time.sleep(2)
                    print(e)
                    continue
            with open(os.path.join(path,f"{file}.txt"),'w',encoding='utf-8') as f:
                f.write(content)
            # break
            if(len(chapterList) == 0):
                break
            else:
                chapter = chapterList.pop()
        except Exception as e:
            time.sleep(2)
            print(e)
            continue
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
def getKey(y, key):
    pinyinKey1=re.findall(r'[a-zāáǎàōóǒòēéěèīíǐìūúǔùüǖǘǚǜńňǹḿmɡ]{2,}',y)
    return pinyinKey1[0]

def photoFont(li):
    def func(x,y):
        tkey = x.get('$word')
        if (tkey == None):
            x['$word'] = re.sub(r'[^\u4e00-\u9fa5]','',y)
            return x
        elif (len(tkey) == 1):
            x[tkey] = re.sub(r'[\u4e00-\u9fa5]','',y)
            x.pop("$word")
        else:
            x[tkey[:1]] = re.sub(r'[\u4e00-\u9fa5]','',y)
            x['$word'] = tkey[1:]
        return x
    li = reduce(func, [{}, ] + li)
    return li

def replace(content):
    content = re.sub('【\\d+】|更\\*多.*说\\*站|最新章节|请访问|海haxsk.岸线文学.*|&rsqu;|\\?a[\\s\\S]*?/>|\\?a[\\s\\S]*?>','',content)
    content = re.sub('https://.*','',content)
    content = re.sub('&qut[o]*;|&ldqu;|&rdqu;|&lsqu;','"',content)
    content = re.sub('y[iīíǐì]*nj[iīíǐì]*ng','阴茎',content)
    content = re.sub(r'[大]*\*\*[巴]*','大鸡巴',content)
    content = re.sub('&([Aa-zZ]*)grave;',lambda x: x.group(1),content)
    content = re.sub('&([Aa-zZ]*)acute;',lambda x: x.group(1),content)
    content = re.sub('c[aāáǎà]','操',content)
    content = re.sub('xi[oōóǒò]ng','胸',content)
    # content = re.sub('[……]y[iīíǐì]*n','阴',content)
    # content = re.sub('rǔ…rǔ','乳…乳',content)
    content = re.sub('y[iīíǐì]*n\n\n','阴',content)
    content = re.sub('j[iīíǐì]*ng\n\n','茎',content)
    content = re.sub('r[uūúǔùü]\n\n','乳',content)
    content = re.sub('shw(?=出)','show',content)
    content = re.sub('(?<=摆)[P|p]se','pose',content)
    content = re.sub('(摸|巨|肥|双|雪|豪|捏|催)\n\n',lambda x: x.group(1),content)
    content = re.sub('y[iīíǐì]*ny[iīíǐì]*n','淫淫',content)
    content = re.sub('B[iīíǐì]','逼',content)
    # content = re.sub('(?<=[你的]|小|浪|[巴和]|骚|嫩|操|贱|美|插|蜜|肉|臭|扣|比|舔|[舔过]|[白虎]|老|大|玩|肥|威|宝|[处女]|玉|好|烂|[yn]|有|将|跟|[当成了]|[操我]|[操姐姐]|[操几次]|[…+]|[女人]|把|[挖她]|日|磨|[擦拭]|这|粉|黑|直)B[iīíǐì]*|B[iīíǐì]*(?=缝|中|里|门|口|心|儿|腔|肉|洞|内|穴|理|上|痒|问|水|毛|字|你|插|[不错]|眼|咋|外|吃|[就是]|[更好玩]|[长的好看]|处|[的深处]|爽)','逼',content)
    content = re.sub('j[iīíǐì]*ng(?=液)','精',content)
    content = re.sub('a[iīíǐì](?=液)','爱',content)
    content = re.sub('(?<=鸡)b[aāáǎà]','巴',content)
    content = re.sub('(?<=肉|玉|青|[子宫]|玉|阴)[\\s]*j[iīíǐì]*ng|j[iīíǐì]*ng(?=根|部|体|[与洞]|围|身|小|柱)','茎',content)
    content = re.sub('gu[iīíǐì]*(?=头)','龟',content)
    content = re.sub('r[oōóǒò]*u(?=棒|洞)','肉',content)
    content = re.sub('sh[eēéěè]*(?=精)','射',content)
    content = re.sub('xi[aāáǎà]*(?=穴)','小',content)
    content = re.sub('s[aāáǎà]*[o]*(?=穴)','骚',content)
    content = re.sub('(?<=会|舔|下|捻|外|江|露|女|浓|摸|光|[……])[\\s]*y[iīíǐì]*n|y[iīíǐì]*n(?=唇|道|蒂|户|囊|毛|茎|部|核|沟|精|逼|阜|沉|门|洞|肉|暗|缝|影|火|壁|臀|丘|胯|错|埠|膣|纯|环|径|帝|谋|璧|中|腔|蕊|交|瓣|根|血|曩|天|霾|袋|力|云|曹|了|肌|碍|内|经|文|香|口)','阴',content)
    # content = re.sub('(?<=会|舔|下|捻)y[iīíǐì]*n|y[iīíǐì]*n[\\S\\S](?=[唇|道|蒂|户|囊|毛|茎|部|核|沟|精|逼|阜|沉|门|洞|肉|暗|缝|影|火|壁|臀|丘|胯|错|埠|膣|纯|环|径|帝|谋|璧|缝|阜])','阴',content)
    content = re.sub('(?<=奸|手|卖|最|浸|意|口|绝|超|欢|真|好|催|弄|很|荒|爱|[任你]|自|夜|奇|骚|狂|同|够|幺|恣|可|她)y[iīíǐì]*n|y[iīíǐì]*n(?=水|惑|荡|妇|乱|贼|穴|液|笑|欲|靡|兴|秽|贱|汁|语|言|叫|骚|浪|声|词|民|媚|糜|棍|性|娃|魔|慾|邪|姐|猥|滑|兽|亵|恶|趣|的|地|舌|戏|态|脚|虐|女|虫|心|奴|呼|唱|弄|威|哼|样|窝|片|意|狎|手|夜|相|丝|湿|呻|姿|念|味|光|汤|茧|蜜|曲|[汉子]|[美妇]|嘴|技|霏|话|窟|迷|乐|潮|徒|具|到|辞|阳|辱|花|母|狼|浸|瘾|得|着|想|过|事|艳|[老婆]|冶|货|哭|奔|挚|摩|击|种|大|眼|起|[……荡])','淫',content)

    content = re.sub('x[iīíǐì]*ng(?=奴|具)','性',content)
    content = re.sub('y[aāáǎà]*ng(?=具)','阳',content)
    content = re.sub('n[aāáǎà]*i(?=子)','奶',content)
    content = re.sub('[aāáǎà]*i(?=子)','奶',content)
    content = re.sub('(?<=玉|鸽|两|挺|[奶油]|摸|大|鲜|巨|双|嫩|酥|坚|[石钟]|丰|雪|残|椒|肥|豪|美|硕|母|左|右|哺|胸|催|[两只]|露|射|[沐浴]|[洗面]|跪|脯|淑|肉|通|芳|涂|浪|舔|[哺过]|笋|粉|翘|香|尖|耸|捏)[\\s]*r[uūúǔùü]|r[uūúǔùü](?=房|头|炮|峰|蜂|沟|汁|罩|晕|交|尖|白|香|根|黄|波|球|浪|蕾|首|液|荡|肉|前|蒂|胸|壕|肌|珠|上|丘|杯|癌|钟|夹|贴|儿|间|型|孔|菽|妇|端|身|…)','乳',content)
    content = re.sub('m[iīíǐì](?=穴)','蜜',content)
    content = re.sub('l[aāáǎà]*ng(?=穴)','浪',content)
    return content

def pinyin(path,dpath,fun):
    makeDictory(dpath)
    pinyinKeys = []
    pinyinKeys1 = []
    for root, dirs, files in os.walk(path):
        for file in files:
            print(os.path.join(root,file))
            with open(os.path.join(root,file),'r',encoding='utf-8', errors='ignore') as f:
                content = f.read()
                content = fun(content)
                pinyinKey1=re.findall(r'[a-zāáǎàōóǒòēéěèīíǐìūúǔùüǖǘǚǜńňǹḿmɡ]{2,}',content)
                pinyinKey=re.findall(r'[\w|\W]{4}[a-zāáǎàōóǒòēéěèīíǐìūúǔùüǖǘǚǜńňǹḿmɡ]{2,}[\w|\W]{4}',content)
                # print(pinyinKey1)
                # print(pinyinKey)
                print(len(pinyinKey1))
                print(len(pinyinKey))
                # if len(pinyinKey1) != len(pinyinKey):
                #     print(pinyinKey1)
                #     print(pinyinKey)
                pinyinKeys.extend(pinyinKey)
                pinyinKeys1.extend(pinyinKey1)
    print(len(pinyinKeys1))
    print(len(set(pinyinKeys1)))
    print(len(pinyinKeys))
    print(len(set(pinyinKeys)))
    pinyinKeysSet=deleteDuplicateGroup(getKey,pinyinKeys,'')
    print(len(pinyinKeysSet))
    # print(pinyinKeysSet)
    with open(f"{dpath}/pinyinKeySet.json",'w',encoding='utf-8') as f:
        json.dump(pinyinKeysSet, f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':'))
    with open(f"{dpath}/pinyinKey.json",'w',encoding='utf-8') as f:
        json.dump({'data':pinyinKeys}, f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':'))
    with open(f"{dpath}/pinyinKey1.json",'w',encoding='utf-8') as f:
        json.dump({'data':pinyinKeys1}, f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':'))

def makeDictory(path):
    paths = os.path.split(path)
    pa = ''
    for dic in paths:
        pa = os.path.join(pa, dic)
        if(not os.path.exists(pa)):
            os.makedirs(dic)

def freplace(*parm):
    content = parm[0]
    content = re.sub('\\?u.*?\\/>|【.*】|更\\*多.*说\\*站|最新章节|请访问|海haxsk.岸线文学.*|&rsqu;|\\?a[\\s\\S]*?/>|\\?a[\\s\\S]*?>','',content)
    content = re.sub('https://.*','',content)
    content = re.sub('&qut[o]*;|&ldqu;|&rdqu;|&lsqu;','"',content)
    content = re.sub('记住地阯發布頁.*?[Ｃоm|protected\\]|ＣＯＭ]|哋.*?Ｃоm|当前网址.*?发布页！|【.*】|更\\*多.*说\\*站|\\n|\\t|\xa0|．*','',content)
    content = re.sub('_','',content)
    content = re.sub('#','_',content)
    content = re.sub(r'\W+','',content)
    content = re.sub('_','#',content)
    return content

def sreplace(*parm):
    # content = freplace(content)
    file = parm[1]
    content = parm[0]

    with open(file,'r',encoding='utf-8', errors='ignore') as f:
        dict1 = json.load(f)
        for k,v in dict1.items():
            content = re.sub(f"#{k}#",v,content)
    content = replace(content)
    return content

def diff(fpath,spath,dpath,fun):
    makeDictory(dpath)
    for file in os.listdir(fpath):
        if not os.path.isdir(file):
            with open(os.path.join(fpath,file),'r',encoding='utf-8', errors='ignore') as f:
                content1 = f.read()
                content1 = fun(content1)
                # print(content)
            with open(os.path.join(spath,file),'r',encoding='utf-8', errors='ignore') as f:
                content2 = f.read()
                content2 = fun(content2)
                # print(content2)
            # diff = difflib.HtmlDiff()
            # result = diff.make_file(content1, content2)
            result = difflib.ndiff(content1,content2)
            def function(x):
                if re.match(r'[+] [^\u4e00-\u9fa5]', x):
                    return True
                elif re.match(r'[-] [\u4e00-\u9fa5]', x):
                    return True

            result = list(filter(function,result));
            print(len(result))
            if(len(result) > 0):
                cc = reduce(lambda x,y: re.sub(r'[+-] ','',x) + re.sub(r'[+-] ','',y),result)
                # print(cc)
                ccs = cc.replace('##','#').split('#')
                # print(ccs)
                print(len(ccs))
                rr = photoFont(ccs)
                print(rr)
                with open(os.path.join(dpath,f"{re.sub('.txt','.json',file)}"),'w',encoding='utf-8') as f:
                    json.dump(rr, f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':'))

    # with open(f"book/result_comparation.html",'w',encoding='utf-8') as f:
    #     f.write(result)

    # with open(f"book/result_comparation.json",'w',encoding='utf-8') as f:
    #     json.dump({'data':list(cc)}, f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':'))
def getKey1(x,key):
    return x[0]

def diffPhoto(path):
    diffDict = {}
    tdict = []
    for file in os.listdir(path):
        if not os.path.isdir(file):
            with open(os.path.join(path,file),'r',encoding='utf-8', errors='ignore') as f:
                dict1 = json.load(f)
                for k,v in dict1.items():
                    if v in diffDict and k != diffDict[v]:
                        tdict.append([v,k])
                    else:
                        diffDict[v] = k
            # os.remove(os.path.join(path,file))
    
    with open(f"{path}/diff.json",'w',encoding='utf-8') as f:
        json.dump(diffDict, f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':'))
    with open(f"{path}/diffc.json",'w',encoding='utf-8') as f:
        json.dump(deleteDuplicateGroup(getKey1,tdict,''), f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':'))

def write2(path,dpath,start,fun,rfile):
    makeDictory(dpath)
    for file in os.listdir(path):
        if not os.path.isdir(file):
            with open(os.path.join(path,file),'r',encoding='utf-8', errors='ignore') as f:
                content = f.read()
                content = fun(content,rfile)
            file = file if start == None or start == 0 else re.sub(r'(\d+)',lambda x:f"{int(x.group(1)) - start}",file)
            with open(os.path.join(dpath,re.sub(os.path.splitext(file)[1],'.txt',file)),'w',encoding='utf-8') as f:
                f.write(content)
def read2(path,dpath):
    photoKeys = []
    for file in os.listdir(path):
        if not os.path.isdir(file):
            with open(os.path.join(path,file),'r',encoding='utf-8', errors='ignore') as f:
                content = f.read()
                pinyinKey1=re.findall(r'#[a-zA-Z0-9]*#',content)
                print(pinyinKey1)
                photoKeys.extend(pinyinKey1)
    print(len(photoKeys))
    print(len(set(photoKeys)))
    with open(f"{dpath}/photoKeys.json",'w',encoding='utf-8') as f:
        json.dump({'data':list(set(photoKeys))}, f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':'))

def read3(path,dpath):
    with open(os.path.join("book/大雄5","diff.json"),'r',encoding='utf-8', errors='ignore') as f:
        dict1 = json.load(f)
        print(len(dict1))
    with open(os.path.join("book/大雄5","photoKeys.json"),'r',encoding='utf-8', errors='ignore') as f:
        dict2 = json.load(f)
        print(len(dict2['data']))
    for x in dict2['data']:
        if (re.sub('#','',x) not in dict1):
            print(x)

def read4(*path):
    makeDictory(path[1])
    makeDictory(path[3])
    with open(os.path.join("book/大雄5","diff.json"),'r',encoding='utf-8', errors='ignore') as f:
        dict1 = json.load(f)
        print(len(dict1))
    with open(os.path.join("book/大雄5",path[4]),'r',encoding='utf-8', errors='ignore') as f:
        dict2 = json.load(f)
        print(len(dict2))
    for k,v in dict2.items():
        t = re.sub(r'_(\d+)','',k);
        print(t)
        if (t in dict1 and v == dict1.get(t) and v != ''):
            try:
                if(os.path.exists(f"{path[0]}/{k}.png")):
                    shutil.move(f"{path[0]}/{k}.png",f"{path[1]}")
                if(os.path.exists(f"{path[2]}/{t}.png")):
                    shutil.move(f"{path[2]}/{t}.png",f"{path[3]}")
            except Exception as e:
                print(e)
                continue

        else:
            print({k:v})




def imgToString(dpath):
    makeDictory(dpath)
    with open(os.path.join("book/大雄5","photoKeys.json"),'r',encoding='utf-8', errors='ignore') as f:
        dict2 = json.load(f)
        print(len(dict2['data']))
    for x in dict2['data']:
        imgFile = f"http://hdyp.net/toimg/data/{re.sub('#','',x)}.png"
        print(imgFile)
        imgcontent = requests.get(imgFile)
        with open(os.path.join(dpath,f"{re.sub('#','',x)}.png"),'wb') as f:
            f.write(imgcontent.content)

def read5(*path):  
    with open(os.path.join("book/大雄5",path[0]),'r',encoding='utf-8', errors='ignore') as f:
        dict1 = json.load(f)
        print(len(dict1))
        dict2 = {}
        for k,v in dict1.items():
            t = re.sub(r'_(\d+)','',k)
            code = re.sub('[^\u4e00-\u9fa5]','',v)
            if code == "":
                continue
            elif t in dict2:
                if dict2.get(t).get(v) == None:
                    dict2[t][v] = 1
                else:
                    k = int(dict2.get(t).get(v)) + 1
                    dict2[t][v] = k
                total = int(dict2.get(t).get('total')) + 1
                dict2[t]['total'] = total
            else:
                dict2[t] = {v:1,'total':1}    
    print(len(dict2))
    with open(os.path.join("book/大雄5","diff.json"),'r',encoding='utf-8', errors='ignore') as f:
        dict3 = json.load(f)
        print(len(dict3))
        stotal = 0
        ftotal = 0
        for k,v in dict3.items():
            if k in dict2:
                success = dict2.get(k).get(v) if dict2.get(k).get(v) != None else 0
                total = dict2.get(k).get('total') if dict2.get(k).get('total') != None else 0
                successrate = success/total if total != 0 else 1
                
                dict2[k]['successrate'] = f"{successrate*1}%"
                dict2[k]['success'] = v
                
                if successrate >= 0.5:
                    stotal += 1
                    try:
                        shutil.move(f"book/ocrimg2/ocrtrue/{k}.png",f"book/ocrimg2/ocrtrue/ocr/")
                        os.remove(f"book/ocrimg5/ocr/{k}*.png")
                    except Exception as e:
                        print(e)
                if successrate > 0 and successrate < 0.5:
                    try:
                        ftotal +=1
                        shutil.move(f"book/ocrimg2/ocrtrue/{k}.png",f"book/ocrimg2/ocrtrue/1/")
                    except Exception as e:
                        print(e)
            else:
                if os.path.exists(f"book/ocrimg2/ocrtrue/{k}.png"): 
                    dict2[k]={'success':v,'successrate':0}
    dict2['stotalRate'] = f"{stotal/len(dict2)}%"
    dict2['ftotalRate'] = f"{ftotal/len(dict2)}%"
    with open(os.path.join("book/大雄5",path[1]),'w',encoding='utf-8') as f:
        json.dump(dict2, f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':'))


def ocr(path,dpath):
    makeDictory(dpath)
    pdict = {}
    for file in os.listdir(path):
        if not os.path.isdir(os.path.join(path,file)):
            print(file)
            img = Image.open(os.path.join(path,file))
            img.load()
            code = pytesseract.image_to_string(img, lang='chi_sim')
            print(code)
            code = re.sub('[^\u4e00-\u9fa5]','',code);
            if code != "":
                pdict[os.path.splitext(file)[0]] = code
    with open(f"{dpath}/photoOCR.json",'w',encoding='utf-8') as f:
        json.dump(pdict, f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':'))

if __name__ == '__main__':
    # domain = "https://m.sinodan.cc"
    # page_url = "https://m.sinodan.cc/list/5240.html"
    # chapterTag = ".chapter-list li"
    # nextPageTag = ".nextPage"
    # contentTag = ".page-content"
    # path = "book/大雄/"
    # download(domain, page_url, chapterTag, nextPageTag, contentTag, '', path)
    # pinyin()
    # domain = "http://hdyp.net"
    # page_url = "http://hdyp.net/1/1975/"
    # chapterTag = ".chapter-list li"
    # nextPageTag = ".nextPage"
    # contentTag = ".page-content"
    # nextContentTag = '.chapterPages>a.curr+a'
    # path = "book/大雄3/"
    # download(domain, page_url, chapterTag, nextPageTag, contentTag, nextContentTag, path)
    # pinyin('book/大雄3/','book/大雄4/',23718)
    # diff("book/大雄2/","book/大雄4/","book/大雄6/",freplace)
    # diff("book/大雄2/","book/大雄4/","book/大雄7/",sreplace)
    # diffPhoto("book/大雄7/")
    # write2('book/大雄/','book/大雄9/',34788,freplace,'')
    # write2('book/大雄3/','book/大雄10/',23718,freplace,'')
    # diff("book/大雄9/","book/大雄10/","book/大雄6/",freplace)
    # diffPhoto("book/大雄6/")
    # pinyin('book/大雄9/','book/大雄6/',freplace)
    # write2('book/大雄3/','book/大雄7/',None,sreplace, "book/大雄5/diff.json")
    # write2('book/大雄10/','book/大雄8/',None,sreplace, "book/大雄5/diff.json")
    # pinyin('book/大雄7/','book/大雄5/',freplace)
    # write2('book/大雄9/','book/大雄11/',0,sreplace, "book/大雄5/diff.json")
    # pinyin('book/大雄11/','book/大雄5/',freplace)
    # write2('book/大雄10/','book/大雄12/',0,sreplace, "book/大雄5/diff.json")
    # diff("book/大雄11/","book/大雄12/","book/大雄1/",freplace)
    # diffPhoto("book/大雄1/")
    # read2("book/大雄3/","book/大雄5/")
    # read3('','')
    # imgToString("book/ocrimg2/")
    # ocr('book/ocrimg5/ocr/','book/大雄5/')
    # read4("photoKeys45_45_85.json")
    # read4("photoKeys_30_30_93_98.json")
    # read4("photoKeys_25_25_93_98.json")
    # read4("photoKeys_20_25_93_98.json")
    # read4("photoKeys_45_45_90_98.json")
    # read4("photoKeys_70_75_90_98.json")
    # read4(""photoKeys_15_100_5_90_98.json"")
    # read4("book/ocrimg2/ocrtrue/","book/ocrimg2/ocrtrue/ocr/","book/ocrimg5/ocr/","book/ocrimg5/ocr/ocrtrue/","photoKeys_15_20_5_90_98.json")
    # read5("photoKeys_15_20_5_90_98.json")
    # read5("photoKeys_15_20_5_90_98.json","photoKeys_15_20_5_90_98_num.json")
    # read5("photoKeys_25_30_5_90_98.json","photoKeys_25_30_5_90_98_num.json")
    # read5("photoKeys_35_40_5_90_98.json","photoKeys_35_40_5_90_98_num.json")
    # read5("photoKeys_40_45_5_90_98.json","photoKeys_40_45_5_90_98_num.json")
    # read5("photoKeys_55_60_5_90_98.json","photoKeys_55_60_5_90_98_num.json")
    # read5("photoKeys_65_70_5_90_98.json","photoKeys_65_70_5_90_98_num.json")
    read5("photoKeys_35_70_5_90_98.json","photoKeys_35_70_5_90_98_num.json")