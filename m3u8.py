# -*- coding: utf-8 -*-
import os,json
from functools import reduce
import requests
import subprocess,random

check = False
group = ""

def listm3u8(line):
    name = line.split(',')[0]
    urls = line.split('#')
    m3u8s = []
    clarity = ""
    global group
    if line.find("#genre#") > 0:
        print(line)
        group = ""+name
        return ""
    for url in urls:
        if check:
            clarity = "-" + ffprobe(url.replace(f'{name},','').replace('\n',''))
        if check and clarity=="-":
            continue
        #print(data)
        #if (data!=None and data != ""):
            #img = f"https://api.btstu.cn/sjbz/api.php?lx=meizi&t={random.random()}"
        m3u8s.append(f"#EXTINF:-1 group-title=\"{group}\"")
        #m3u8s.append(f'tvg-logo="{img}"')
        m3u8s.append(',')
        m3u8s.append(f"{name}{clarity}")
        m3u8s.append('\n')
        m3u8s.append(url.replace(f'{name},','').replace('\n','')+'\n')
        #else:
        #    m3u8s.append("\n")
        # m3u8s+=(f'#EXTINF:-1 ,{name}')+'\n'+url.replace(f'{name},','').replace('\n','')+'\n'
    if (len(m3u8s)>0):
        return reduce(lambda x,y: x + y,m3u8s)

def toM3U8(path,m3u8_file):
    m3u8list = ["#EXTM3U\n"]
    for root, dirs, files in os.walk(path):
        for file in files:
            with open(os.path.join(root,file),'r',encoding='utf-8', errors='ignore') as f:
                #for line in f.readlines():
                #    print(line)
                lines = f.readlines()
                if (len(lines) >0):
                    m3u8list.append(reduce(lambda x,y: x + y,map(listm3u8,filter(lambda line:line != '' and line != '\n',lines))))
    #             m3u8s=reduce(lambda x,y: x + y,map(listm3u8,filter(lambda line:line != '' and line != '\n',f.readlines())))
    #         m3u8list.append(m3u8s)
    with open(m3u8_file,'w',encoding='utf-8') as f:
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
    i = 0
    m3u8list = ["#EXTM3U\n"]
    m3u8FailList = ["#EXTM3U\n"]
    clarity = ""
    for info in infos:
        if check:
            clarity = "-" + ffprobe(urls[i].replace('\n',''))
        print(clarity)
        if check and clarity == "-":
            m3u8FailList.append(f'{info}{clarity}\n')
            m3u8FailList.append(urls[i])
            m3u8FailList.append('\n')
        else:
            m3u8list.append(f'{info}{clarity}\n')
            m3u8list.append(urls[i])
            m3u8list.append('\n')
        i = i + 1

    with open('iptv.m3u8','w',encoding='utf-8') as f:
        f.writelines(m3u8list)
    with open('iptv_fail.m3u8','w',encoding='utf-8') as f:
        f.writelines(m3u8FailList)

def toM3U8Url(url):
    get_page = requests.get(url);
    content = str(get_page.content,'utf-8',errors='ignore');
    m3u8s = content.splitlines();
    m3u8list = []
    for m3u8 in m3u8s:
        urls = m3u8.split(",")
        name = urls[0]
        url = urls[1]
        img = urls[2]
        m3u8list.append(f'#EXTINF:-1 group-title="{name}" ')
        m3u8list.append(f'tvg-logo="{img}"')
        m3u8list.append(',')
        m3u8list.append(name)
        m3u8list.append('\n')
        m3u8list.append(url+'\n')
    with open('韩国伦理电影.m3u8','w',encoding='utf-8') as f:
        f.writelines(m3u8list)

def getM3u8Steam():
    pass

def ffprobe(url):
    print("执行ffprobe")
    try:
        requests.get(url=url)
    except Exception as e:
        return ""
    proc = subprocess.run(['ffprobe',"-timeout","200000",'-print_format','json','-show_format','-show_streams','-v','quiet',url],stdout=subprocess.PIPE)
    print(proc)
    data = json.loads(proc.stdout.decode('utf-8'))
    if(len(data)>0):
        for d in data.get("streams"):
            if(d.get("codec_name") == "h264"):
                width = d.get("width")
                height = d.get("height")
                print(f"{width}-{height}")
                if(width >= 1920):
                    return "蓝光"
                elif (width >= 1280):
                    return "高清"
                elif (width >= 1080):
                    return "标清"
                else:
                    return "普清"
    return ""
if __name__ == '__main__':
    # toM3U8("E:\\workspace\\hikerView2\\tv\\202108",'iptv6.m3u8')
    toM3U8("m3u81/","ipv7.m3u8")
    # readM3U8("iptv6.m3u8")
    # jsontoM3U8("E:\\workspace\\hikerView\\tv\\202006","iptv3.m3u8")
    # toM3U8Url("https://gitee.com/shentong_012/HikerRules/raw/master/m3u8.txt")
    # print(ffprobe("http://58.243.4.22:1935/live/zonghe/playlist.m3u8"))