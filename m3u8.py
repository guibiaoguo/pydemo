# -*- coding: utf-8 -*-
import os,json
from functools import reduce

def listm3u8(line):
    name = line.split(',')[0]
    urls = line.split('#')
    m3u8s = []
    for url in urls:
        m3u8s.append(f'#EXTINF:-1 group-title="{name}" ')
        m3u8s.append(f'tvg-logo=""')
        m3u8s.append(',')
        m3u8s.append(name)
        m3u8s.append('\n')
        m3u8s.append(url.replace(f'{name},','').replace('\n','')+'\n')
        # m3u8s+=(f'#EXTINF:-1 ,{name}')+'\n'+url.replace(f'{name},','').replace('\n','')+'\n'
    return reduce(lambda x,y: x + y,m3u8s)

def toM3U8(path):
    m3u8list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            with open(os.path.join(root,file),'r',encoding='utf-8', errors='ignore') as f:
                # for line in f.readlines():
                #     name = list([k,v for ])
                #     print(name)
                m3u8s=reduce(lambda x,y: x + y,map(listm3u8,filter(lambda line:line != '' and line != '\n',f.readlines())))
            m3u8list.append(m3u8s)
    with open('iptv2.m3u8','w',encoding='utf-8') as f:
        f.writelines(m3u8list)

def jsontoM3U8(path,wfile):
    m3u8list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            with open(os.path.join(root,file),'r',encoding='utf-8', errors='ignore') as f:
                # for line in f.readlines():
                #     name = list([k,v for ])
                #     print(name)
                m3u8s = reduce(lambda x,y: x + y,map(listm3u8,filter(lambda line:line.find('#') != 0,f.readlines())))
            m3u8list.append(m3u8s)
    with open(wfile,'w',encoding='utf-8') as f:
        f.writelines(m3u8list)

def readM3U8(file):
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    infos=[x.replace('#EXTINF:-1 ,','').replace('\n','') for x in lines if x.find('EXTINF')>=0]
    urls=[x.replace('\n','') for x in lines if x.find('EXTINF') < 0 and x.find('EXTM3U') < 0]
    dict={}
    i = 0
    for info in infos:
        if(dict.get(info) and len(dict.get(info))>0):
            list = dict.get(info)
            k = k + 1
        else:
            list = []
            k = 0
        list.append(f'源{k}={urls[i]}')
        dict[info] = list    
        i = i + 1
    m3u8list = []
    for k,v in dict.items():
        m3u8list.append(f'[{k}]\n')
        m3u8list.append(reduce(lambda x,y: x + '\n' + y,v))
        m3u8list.append('\n')
    with open('iptv.txt','w',encoding='utf-8') as f:
        f.writelines(m3u8list)

if __name__ == '__main__':
    # toM3U8("E:\\workspace\\hikerView\\tv\\202006")
    # readM3U8("C:\\Users\\bill\\Desktop\\Crack\\直播-online.m3u8")
    jsontoM3U8("E:\\workspace\\hikerView\\tv\\202006","iptv3.m3u8")