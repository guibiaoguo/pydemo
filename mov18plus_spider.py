
import requests,json,os,threading,time,logging
from bs4 import BeautifulSoup
from multiprocessing import Process,Queue
from multiprocessing.queues import Empty
from urllib.request import urlretrieve
import subprocess
import mysql.connector

#***********************************************************************************#
api_id = 1143827  # your telegram api id
api_hash = '5238af5531a07c5e99d281bddc8e8b46'  # your telegram api hash
bot_token = '1429939977:AAFGfZldFZTDUcPKKavgtL1SWw3nIhS5R5I'  # your bot_token
admin_id = 754878456 # your chat id
save_path = 'e:/downloads'  # file save path
upload_file_set = False # set upload file to google drive
drive_id = '0AEtGeQW0667dUk9PVA'  # google teamdrive id
drive_name = 'gc'  # rclone drive name
max_num = 5  # 同时下载数量
# filter file name/文件名过滤
filter_list = ['你好，欢迎加入 Quantumu', '\n']
# filter chat id /过滤某些频道不下载
blacklist = [1388464914,]
donwload_all_chat = False # 监控所有你加入的频道，收到的新消息如果包含媒体都会下载，默认关闭
filter_file_name = []
pageSize=51
#***********************************************************************************#


logging.basicConfig(level=logging.ERROR,filename='failed_img.log')

# logger = logging.getLogger(__name__)

# 抓取地址
answers_url='https://www.zhihu.com/api/v4/questions/29815334/answers?data[*].author.follower_count%2Cbadge[*].topics=&data[*].mark_infos[*].url=&include=data[*].is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled&limit=5&offset=0&platform=desktop&sort_by=default'

page_url='https://mov18plus.com/genre/korea/page/'

# 待下载图片队列
mp4_queue = Queue()
# 下载图片失败队列
bad_queue = Queue()

# 请求头
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
    'Host':'www.zhihu.com'
}

# 获取本地时间
def get_local_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


'''
请求知乎回答数据
:param answers_url: 知乎问题的第一个回答请求地址
:param imgq: 待下载图片队列
:param count: 递归结束标识，用于判断是否最后一页
:return: 
'''
def getR(answers_url, imgq, count=0):

    while True:
        try:
            r = requests.get(answers_url, headers=headers)
        except BaseException:
            continue
        else:
            rj = str(r.json()).replace("True", "\"true\"").replace("False", "\"false\"")
            rj = json.loads(json.dumps(eval(rj)))

            for x in rj['data']:
                content = x['content']
                soup = BeautifulSoup(content, 'lxml')
                # 查找img标签并且class属性等于origin_image zh-lightbox-thumb的元素
                for img in soup.find_all('img', attrs={'class': 'origin_image zh-lightbox-thumb'}):
                    # 保存图片到mp4_queue队列
                    imgq.put(img['data-original'])
                    print('保存%s到mp4_queue' % os.path.split(img['data-original'])[1])
            if rj['paging']['is_end'] != 'true':
                answers_url = rj['paging']['next']
            else:
                print('request_pro 执行完毕')
                # 最后一页
                break

def save(name, url):
    conn = mysql.connector.connect(user='root', password='root', database='test') 
    cursor = conn.cursor()
    cursor.execute('insert into media (name,url,country) values (%s, %s, %s)', [name, url,'Korea'])
    print(cursor.rowcount)
    conn.commit()
    cursor.close()
    conn.close()
def select(name, url):
    conn = mysql.connector.connect(user='root', password='root', database='test') 
    cursor = conn.cursor()
    cursor.execute('select * from media where name = %s and url = %s', (name, url))
    values = cursor.fetchall()
    print(values)
    cursor.close()
    conn.close()
    return values

def saveVideo(name, url):
    conn = mysql.connector.connect(user='root', password='root', database='test') 
    cursor = conn.cursor()
    cursor.execute('insert into video (name,url,country) values (%s, %s, %s)', [name, url,'Korea'])
    print(cursor.rowcount)
    conn.commit()
    cursor.close()
    conn.close()
def selectVideo(name, url):
    conn = mysql.connector.connect(user='root', password='root', database='test') 
    cursor = conn.cursor()
    cursor.execute('select * from video where name = %s and url = %s', (name, url))
    values = cursor.fetchall()
    print(values)
    cursor.close()
    conn.close()
    return values

def handler(page_url,pageSize, imgq, count=0):
    
    for pageNo in range(1,pageSize+1):
        m_url = f'{page_url}{pageNo}/'
        print(m_url)
        try:
            get_page=requests.get(url=m_url)
        except Exception as e:
            print("分页下载失败")
            logging.error(f'{get_local_time()} - {m_url} 出现异常，重新尝试下载！')
            time.sleep(10)
            continue

        soup = BeautifulSoup(str(get_page.content,'utf-8',errors='ignore'),'lxml')
        viewkey=soup.select(".items article")
        #print(viewkey)
        page='第'+str(pageNo)+'页'
        for key in viewkey:
            try:
                title=key.h3.string
                print(title)
                media_url=key.a['href']
                print(media_url)
                media_page=requests.get(url=str(media_url))
                tsoup = BeautifulSoup(str(media_page.content,'utf-8',errors='ignore'),'lxml')
                furl=tsoup.select("#download a")
                if (len(furl) == 0):
                    continue
                print(furl)
                time.sleep(5)
                try:
                    saveVideo(str(title),furl[0]['href'])
                    f_page=requests.get(url=furl[0]['href'])
                except Exception as e:
                    print("获取下载地址异常")
                    logging.error(f'{get_local_time()} - {furl} 出现异常，重新尝试下载！')
                    time.sleep(10)
                
                fsoup = BeautifulSoup(str(f_page.content,'utf-8',errors='ignore'),'lxml')
                d_url=str(fsoup.select("#link")[0]['href'])
                print(d_url)
                headers={"referer":"https://sexhd.co/"}
                values=select(str(title),d_url)
                if(d_url.find('sexhd.co') < 0 ):
                    continue
                if(len(values) == 0):
                    save(str(title),d_url)
    #             continue
    #             get_page=requests.post(d_url.replace('/f/','/api/source/'),data={})
    #             data = {}
    #             if(get_page.status_code != 200):
    #                 continue
    # #            print(str(get_page.content,'utf-8',errors='ignore'))
    #             data = json.loads(str(get_page.content,'utf-8',errors='ignore'))
    #             list=data.get('data')
    #             for media in list:
    #                 label=media.get('label')
    #                 file=media.get('file')
    #                 type1=media.get('type')
    #                 file_name = f"{title}-{label}.{type1}"
    #                 print(file_name)
    #                 imgq.put({'file_name':file_name,'file':file})       
    #                 print('保存%s %s到mp4_queue' %(file,file_name))
            except Exception as e:
                print("远程关闭连接")
                print(e)
                time.sleep(10)

            # break
    print('request_pro 执行完毕')
'''
下载进程：分别创建四个线程，用于下载图片
:param imgq:    待下载图片队列
:param badq:    下载图片失败队列
:param pname:   进程名称
:return: 
'''
def download_pro(imgq,badq,pname):

    # 这里设置name可用于区分是哪个进程的哪个线程
    t1 = threading.Thread(target=download,args=(imgq,badq),name='%s - 下载线程1' % pname)
    t2 = threading.Thread(target=download,args=(imgq,badq),name='%s - 下载线程2' % pname)
    t3 = threading.Thread(target=download,args=(imgq,badq),name='%s - 下载线程3' % pname)
    t4 = threading.Thread(target=download,args=(imgq,badq),name='%s - 下载线程4' % pname)

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()


'''
下载图片函数
:param imgq:    待下载图片队列
:param badq:    下载图片失败队列
:return: 
'''
def download(imgq,badq):

    thread_name = threading.current_thread().name
    while True:
        try:
            # 设置timeout=10,10秒后队列都拿取不到数据，那么数据已经下载完毕
            list = imgq.get(True, timeout=10)
        except Empty:
            print('%s 执行完毕' % thread_name)
            # 退出循环
            break
        else:
            file_name = list.get('file_name')
            file = list.get('file')
            headers={"referer":"https://sexhd.co/"}
            req=requests.head(url=file,headers=headers,stream=True)
            if(req.status_code != 302):
                badq.put(list)
                continue
            url=req.headers['Location']
            print(url)
            dirname = "Korea";#validateTitle(f'{chat_title}({entity.id})')
            datetime_dir_name = ""#message.date.strftime("%Y年%m月")
            file_save_path = os.path.join(save_path, dirname, datetime_dir_name)
            if not os.path.exists(file_save_path):
                os.makedirs(file_save_path)
            try:                
                if file_name not in os.listdir(file_save_path):
                    # imgcontent = requests.get(url)
                    # ''' 图片请求失败,将图片地址放入bad_queue,等待bad_pro处理'''
                    # if imgcontent.status_code != 200:
                    #     print('%s 下载%s失败' % (thread_name,file_name))
                    #     badq.put(list)
                    #     continue
                    # with open(os.path.join(file_save_path, file_name), 'wb') as f:
                    #     f.write(imgcontent.content)
                    #     print('%s 下载%s成功' % (threading.current_thread().name, file_name))
                    if upload_file_set and file_name in os.listdir(file_save_path):
                        print("开始上传"+file_name)
                        proc = subprocess.call(['gclone','move',os.path.join(file_save_path, file_name),f"{drive_name}:{{{drive_id}}}/{dirname}/{datetime_dir_name}",'--ignore-existing'])
                        print(f"{get_local_time()} - {file_name} 下载并上传完成")
            except Exception as e:
                print(f"{get_local_time()} - {file_name} {e}")
                badq.put(list)
            finally:
                # 无论是否上传成功都删除文件。
                if upload_file_set:
                    try:
                        print("开始删除文件")
                        os.remove(os.path.join(file_save_path, file_name))
    #                    break
                    except:
                        pass     

'''
创建四个线程用于尝试bad_queue队列中的图片，
:param badp: bad_queue
:return: 
'''
def again_pro(badq):

    b1 = threading.Thread(target=again_download, args=(badq,),name='重下线程1')
    b2 = threading.Thread(target=again_download, args=(badq,),name='重下线程2')
    b3 = threading.Thread(target=again_download, args=(badq,),name='重下线程3')
    b4 = threading.Thread(target=again_download, args=(badq,),name='重下线程4')

    b1.start()
    b2.start()
    b3.start()
    b4.start()


'''
尝试重复下载bad_queue队列中的图片
:param badq: bad_queue
:return: 
'''
def again_download(badq):

    thread_name = threading.current_thread().name
    while True:
        try:
            # 设置timeout=10,10秒后队列都拿取不到数据，那么数据已经下载完毕
            list = badq.get(True, timeout=10)
        except Empty:
            print('%s 执行完毕' % thread_name)
            # 退出循环
            break
        else:
            file_name = list.get('file_name')
            file = list.get('file')
            headers={"referer":"https://sexhd.co/"}
            req=requests.head(url=file,headers=headers,stream=True)
            if(req.status_code != 302):
                badq.put(list)
                continue
            url=req.headers['Location']
            print(url)
            dirname = "Korea";#validateTitle(f'{chat_title}({entity.id})')
            datetime_dir_name = ""#message.date.strftime("%Y年%m月")
            file_save_path = os.path.join(save_path, dirname, datetime_dir_name)
            try:                
                if file_name not in os.listdir(file_save_path):
                    for x in range(5):
                        try:
                            # 个人感觉使用urlretrieve下载的成功率要高些，哈哈^_^
                            # urlretrieve(url,os.path.join(file_save_path, file_name))
                            pass
                        except BaseException as e:
                            if x==4:
                                logging.error('%s 重复下载失败,error：[%s]'% (url,repr(e)))
                            # 下载失败; 再次尝试
                            continue
                        else:
                            # 下载成功；跳出循环
                            print('%s 在第%s次下载%s成功' % (threading.current_thread().name,(x+1),name))
                            break

                    if upload_file_set and file_name in os.listdir(file_save_path):
                        print("开始上传"+file_name)
                        proc = subprocess.call(['gclone','move',os.path.join(file_save_path, file_name),f"{drive_name}:{{{drive_id}}}/{dirname}/{datetime_dir_name}",'--ignore-existing'])
                        print(f"{get_local_time()} - {file_name} 下载并上传完成")
            except Exception as e:
                print(f"{get_local_time()} - {file_name} {e}")
                badq.put(list)
            finally:
                # 无论是否上传成功都删除文件。
                if upload_file_set:
                    try:
                        print("开始删除文件")
                        os.remove(os.path.join(file_save_path, file_name))
    #                    break
                    except:
                        pass 
'''
监听器，用于关闭程序，10秒刷新一次
:param imgq: mp4_queue
:param badq: bad_queue
:return: 
'''
def monitor(imgq,badq):

    while True:
        time.sleep(10)
        if imgq.empty() and badq.empty():
            print('所有任务执行完毕，40秒后系统关闭')
            count = 39
            while count > 0:
                time.sleep(1)
                print('距离系统关闭还剩：%s秒'%count)
                count-=1
            break


if __name__=='__main__':

    # 请求数据进程
    request_pro = Process(target=handler, args=(page_url,pageSize, mp4_queue))

    ''' 下载图片进程[first]和[second] '''
    # download_pro_first = Process(target=download_pro, args=(mp4_queue,bad_queue,'download process first'))
    # download_pro_second = Process(target=download_pro, args=(mp4_queue,bad_queue,'download process second'))

    # 处理[first]和[second]进程下载失败的图片
    # bad_pro = Process(target=again_pro,args=(bad_queue,))
    # bad_pro.daemon = True

    # req_pro进程启动
    request_pro.start()
    print('3秒之后开始下载 >>>>>>>>>>>>>>>')
    time.sleep(3)

    # first 和 second 进程启动
    # download_pro_first.start()
    # download_pro_second.start()

    # 重复下载进程启动
    # bad_pro.start()

    # 监听线程：判断系统是否退出
    request_pro.join()
    print('监听线程启动 >>>>>>>>>>>>>>>')
    # sys_close_t = threading.Thread(target=monitor,args=(mp4_queue,bad_queue,))
    # sys_close_t.start()