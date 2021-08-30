
import requests,json,os,threading,time,logging
from bs4 import BeautifulSoup
from multiprocessing import Process,Queue
from multiprocessing.queues import Empty
from urllib.request import urlretrieve
import subprocess

#***********************************************************************************#
api_id = 1143827  # your telegram api id
api_hash = '5238af5531a07c5e99d281bddc8e8b46'  # your telegram api hash
bot_token = '1429939977:AAFGfZldFZTDUcPKKavgtL1SWw3nIhS5R5I'  # your bot_token
admin_id = 754878456 # your chat id
save_path = '/downloads'  # file save path
upload_file_set = True # set upload file to google drive
drive_id = '0AAaIG-RScShwUk9PVA'  # google teamdrive id
drive_name = 'gc'  # rclone drive name
max_num = 5  # 同时下载数量
# filter file name/文件名过滤
filter_list = ['你好，欢迎加入 Quantumu', '\n']
# filter chat id /过滤某些频道不下载
blacklist = [1388464914,]
donwload_all_chat = False # 监控所有你加入的频道，收到的新消息如果包含媒体都会下载，默认关闭
filter_file_name = []
pageSize=314
m3u8txt_file="m3u8_txt_japan.txt"
m3u8_file="m3u8_japan.txt"
dirname = "Japan"
#***********************************************************************************#


logging.basicConfig(level=logging.ERROR,filename='failed_img.log')

# logger = logging.getLogger(__name__)

page_url='https://bttzyw64.com/?s=vod-show-id-12-p-'

# 待下载图片队列
mp4_queue = Queue()
# 下载图片失败队列
bad_queue = Queue()

# 请求头
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
    'Host':'https://bttzyw64.com'
}

# 获取本地时间
def get_local_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def handler(page_url,pageSize, imgq, count=0):
    m3u8_txt = [];
    m3u8 = []
    for pageNo in range(2,pageSize+1):
        m_url = f'{page_url}{pageNo}.html'
        print(m_url)
        try:
            get_page=requests.get(url=m_url)
        except Exception as e:
            print("分页下载失败")
            logging.error(f'{get_local_time()} - {m_url} 出现异常，重新尝试下载！')
            time.sleep(10)
            continue
        #print(str(get_page.content,'utf-8',errors='ignore'))
        soup = BeautifulSoup(str(get_page.content,'utf-8',errors='ignore'),'lxml')
        viewkey=soup.select(".col-md-2")
        #print(viewkey)
        page='第'+str(pageNo)+'页'
        for key in viewkey:
            try:
                title=key.select('.title')[0].string
                print(title)
                media_url="https://bttzyw64.com"+key['href']
                print(media_url)
                media_page=requests.get(url=str(media_url))
                tsoup = BeautifulSoup(str(media_page.content,'utf-8',errors='ignore'),'lxml')
                furl=tsoup.select(".text input")
                if (len(furl) == 0):
                    continue
                print(furl)
                time.sleep(2)
                file=furl[0]['value']
                img=furl[1]['value']
                print(file)
                m3u8.append(f"{title},{file},{img}\n")
                m3u8_txt.append(f"{title},{file}\n")
                type1="mp4"
                file_name = f"{title}.{type1}"
                imgq.put({'file_name':file_name,'file':file})       
                print('保存%s %s到mp4_queue' %(file,file_name))
            except Exception as e:
                print("远程关闭连接")
                print(e)
                time.sleep(10)
    with open(f"{save_path}/{m3u8txt_file}",'w',encoding='utf-8') as f:
        f.writelines(m3u8_txt)
    with open(f"{save_path}/{m3u8_file}",'w',encoding='utf-8') as f:
        f.writelines(m3u8)
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
            datetime_dir_name = ""#message.date.strftime("%Y年%m月")
            file_save_path = os.path.join(save_path, dirname, datetime_dir_name)
            if not os.path.exists(file_save_path):
                os.makedirs(file_save_path)
            try:                
                if file_name not in os.listdir(file_save_path):
                    proc =subprocess.run(['ffmpeg','-i',file,'-c','copy',os.path.join(file_save_path, file_name)])
                    ''' 图片请求失败,将图片地址放入bad_queue,等待bad_pro处理'''
                    if upload_file_set and file_name in os.listdir(file_save_path):
                        print("开始上传"+file_name)
                        proc = subprocess.run(['gclone','copy',os.path.join(file_save_path, file_name),f"{drive_name}:{{{drive_id}}}/{dirname}/{datetime_dir_name}",'--ignore-existing'])
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
            datetime_dir_name = ""#message.date.strftime("%Y年%m月")
            file_save_path = os.path.join(save_path, dirname, datetime_dir_name)
            if not os.path.exists(file_save_path):
                os.makedirs(file_save_path)
            try:                
                if file_name not in os.listdir(file_save_path):
                    
                    for x in range(5):
                        try:
                            proc =subprocess.run(['ffmpeg','-i',file,'-c','-copy',os.path.join(file_save_path, file_name)])
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
                        proc = subprocess.run(['gclone','copy',os.path.join(file_save_path, file_name),f"{drive_name}:{{{drive_id}}}/{dirname}/{datetime_dir_name}",'--ignore-existing'])
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
    download_pro_first = Process(target=download_pro, args=(mp4_queue,bad_queue,'download process first'))
    download_pro_second = Process(target=download_pro, args=(mp4_queue,bad_queue,'download process second'))

    # 处理[first]和[second]进程下载失败的图片
    bad_pro = Process(target=again_pro,args=(bad_queue,))
    bad_pro.daemon = True

    # req_pro进程启动
    request_pro.start()
    print('3秒之后开始下载 >>>>>>>>>>>>>>>')
    time.sleep(3)

    # first 和 second 进程启动
    download_pro_first.start()
    download_pro_second.start()

    # 重复下载进程启动
    bad_pro.start()

    # 监听线程：判断系统是否退出
    request_pro.join()
    print('监听线程启动 >>>>>>>>>>>>>>>')
    sys_close_t = threading.Thread(target=monitor,args=(mp4_queue,bad_queue,))
    sys_close_t.start()