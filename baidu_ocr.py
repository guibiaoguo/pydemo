# encoding:utf-8
import requests,re
import base64,os,time,json
from PIL import Image

def getToken():
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=6ieiq0v5FKIljk7Xf1AzOafw&client_secret=zg4DU3qkFqdiVUkoUx0GkxZzc81sPuMR'
    response = requests.get(host)
    if response:
        print(response.json())
        access_token = response.json().get('access_token')
    return access_token

def baiduocr(access_token,path,dfile):
    '''
    通用文字识别（高精度版）
    '''

    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    request_url = request_url + "?access_token=" + access_token
    photoKeys = {}
    for file in os.listdir(path):
        if not os.path.isdir(os.path.join(path,file)):
            while True:  
                try:
                    with open(os.path.join(path,file),'rb') as f:
                        img = base64.b64encode(f.read())
                    params = {"image":img}
                    headers = {'content-type': 'application/x-www-form-urlencoded'}
                    response = requests.post(request_url, data=params, headers=headers)
                    print(file)
                    if response.status_code == 200:
                        print (response.json())
                        if len(response.json().get("words_result")) > 0:
                            photoKeys[os.path.splitext(file)[0]] = response.json().get("words_result")[0].get("words")
                        break
                    else:
                        time.sleep(5)
                    # time.sleep(10)
                except Exception as e:
                    time.sleep(2)
                    print(e)
                    continue
                # continue 
    print(photoKeys)

    with open(dfile,'w',encoding='utf-8') as f:
        json.dump(photoKeys, f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':'))

if __name__ == '__main__':
    access_token = getToken()
    # baiduocr(access_token, "book/ocrimg5", f"book/大雄5/photoKeys45_45_85.json")
    # baiduocr(access_token, "book/ocrimg5", f"book/大雄5/photoKeys30_30_85.json")
    # baiduocr(access_token, "book/ocrimg5", f"book/大雄5/photoKeys_30_30_93_98.json")
    # baiduocr(access_token, "book/ocrimg5", f"book/大雄5/photoKeys_25_25_93_98.json")
    # baiduocr(access_token, "book/ocrimg5", f"book/大雄5/photoKeys_70_75_90_98.json")
    # baiduocr(access_token, "book/ocrimg5/ocr", f"book/大雄5/photoKeys_15_20_5_90_98.json")
    # baiduocr(access_token, "book/ocrimg5/ocr", f"book/大雄5/photoKeys_25_30_5_90_98.json")
    # baiduocr(access_token, "book/ocrimg5/ocr", f"book/大雄5/photoKeys_35_40_5_90_98.json")
    # baiduocr(access_token, "book/ocrimg5/ocr", f"book/大雄5/photoKeys_40_45_5_90_98.json")
    # baiduocr(access_token, "book/ocrimg5/ocr", f"book/大雄5/photoKeys_65_70_5_90_98.json")
    baiduocr(access_token, "book/ocrimg5/ocr", f"book/大雄5/photoKeys_35_70_5_90_98.json")