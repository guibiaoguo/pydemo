import requests

r = requests.get('https://www.baidu.com')
print(r.status_code)
print(r.text)

r = requests.get('https://www.douban.com/search', params={'q': 'python', 'cat': '1001'})
print(r.url)
print(r.encoding)

r = requests.post('https://sexhd.co/api/source/nxj5rt234zxeq-y',data={})
print(r.json()['data'])
print('请求头')
print(r.headers)
print(r.cookies)
r = requests.get('https://www.douban.com/', headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit'})
print(r.text)

r = requests.post('https://accounts.douban.com/login', data={'form_email': 'abc@example.com', 'form_password': '123456'})

# params = {'key': 'value'}
# r = requests.post(url, json=params)

# upload_files = {'file': open('report.xls', 'rb')}

# r = requests.post(url, files=upload_files)
# 
url = "https://www.baidu.com"
cs = {'token': '12345', 'status': 'working'}
r = requests.get(url, cookies=cs)
r = requests.get(url, timeout=2.5)

m3u8 = requests.get("http://183.207.249.14/PLTV/3/224/3221225567/index.m3u8")
print(str(m3u8.content,'utf-8',errors='ignore'))