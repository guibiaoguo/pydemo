# encoding:utf-8
import requests,re
import os,time,json
import subprocess


def av():
    with open(os.path.join("book","AV_GOOD.txt"),'r',encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        magnets = []
        lines.reverse()
        # print(lines)
        while True:
            line = lines.pop()
            #magnet = re.findall(r'^magnet:.*',line)
            #magnet = re.findall(r'\[[有|无]码高清\] (.*?) ',line)
            magnet = re.findall(r'\[.*\] (.*?) ',line)
            if len(magnet) > 0:
                dn = magnet[0]
                print(dn)
                while True:
                    try:
                        get_page=requests.post("https://joes.shentong.workers.dev/0:search",data={'q':dn})
                        files = get_page.json()
                        print(files)
                        t = line
                        for file in files.get('data').get('files'):
                            if file.get('mimeType') == 'application/vnd.google-apps.folder' and str(file.get('name')).lower() == f"{dn}-C".lower():
                                id = file.get('id')
                                print(id)
                                #subprocess.call(['gclone','copy',"gc:{"+id+"}","gc:{"+"0ADSUL2qFcD-UUk9PVA}"+f"/{dn}-C",'--drive-server-side-across-configs','--ignore-existing'])
                                
                                t = f"#{line}"
                            elif file.get('mimeType') == 'application/vnd.google-apps.folder' and file.get('name').find("中文字幕") > 0:
                                id = file.get('id')
                                print(id)
                                subprocess.call(['gclone','copy','--ignore-existing','--drive-server-side-across-configs',"gc:{"+id+"}",f"joesdrive:AV/{dn}-C"])
                                t = f"#{line}"
                        magnets.append(t)
                        if t != line:
                           line = lines.pop()
                           magnets.append(f"#{line}")
                        break
                    except Exception as e:
                        print(e)
                        time.sleep(2)
                        magnets.append(line)
                        break
            else:
                magnets.append(line)

            if len(lines) == 0:
                break
    with open(os.path.join("book","AV_GOOD2.txt"),'w',encoding='utf-8') as f:
        f.writelines(magnets)

if __name__ == '__main__':
    av()