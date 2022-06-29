import socket
import sys
import threading
import numpy as np

# Create LootBox Number list
random_num = np.random.permutation(100000)
random_ls = random_num.tolist()
LootBox_num = []
for i in range(len(random_ls)):
    random_ls[i] += 1  # 全部加1
    LootBox_num.append(str(random_ls[i]))  # 注意一定要轉成string
    
count = 0
lock = threading.Lock()
print("LootBox-Server is waiting for connection...")

class Client(threading.Thread):
    def __init__(self, ip, port, conn, lock):
        threading.Thread.__init__(self)
        self.conn = conn
        self.ip = ip
        self.port = port
        self.lock = lock
        
    def run(self):
        global count
        while True:
            data = self.conn.recv(1024)
            print('received command from {!r}'.format(data))
            if data:
                #self.lock.acquire()
                LBN = LootBox_num[count]
                print('Send (LootBox number: %d) back to the client (count = %d)' %(int(LBN),(count+1)))
                self.conn.sendall(bytes(LBN, encoding = "utf8"))
                count += 1  #因為client端有for loop重覆取值，所以count在此累計
                #self.lock.release()
            else:
                break
        self.conn.close()


class LootBox_Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.address = (self.ip, self.port)
        self.server = None
        self.clients = []
        
    def sock(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #創建socket對象
            self.server.bind(self.address)   #綁定端口
        except socket.error:
            if self.server:
                self.server.close()
            sys.exit(1)    #exit(1)：有错误退出； exit(0)：无错误退出

    def run(self):
        self.sock()
        self.server.listen(5)   # 等待客户端連接
        while True :
            conn, (addr, port) = self.server.accept()   # 建立客户端連接
            print('connection from', (addr,port))
            clt = Client(addr, port, conn, lock)
            clt.start()
            self.clients.append(clt)
        self.server.close()


if __name__ == '__main__':
    svr = LootBox_Server('0.0.0.0', 8899)
    svr.run()
