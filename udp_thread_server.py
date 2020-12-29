import socket,time,threading
#SOCK_DREAM代表UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1',9999))
#不需要listen
print('Bind UDP on 9999...')

#创建新进程（线程）
def udplink(sock,data,addr):
    print('Received from %s:%s.' % addr)
    while True:
        time.sleep(1)
        if not data or data.decode('utf-8')=='exit':
            break
        sock.sendto(b'Hello, %s!' % data, addr)
    sock.close()
    print('Connection from %s:%s closed.' % addr)

def receive_data(sock):
    while True:
        # 接收数据:
        try:#
            data, addr = sock.recvfrom(1024)
            t=threading.Thread(target=udplink,args=(sock,data,addr))
            t.start()
        except Exception as e: #[WinError 10054] 远程主机强迫关闭了一个现有的连接。
            pass #不处理此错误

if __name__=='__main__':
    receive_data(s)