import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port on the server
# given by the caller
server_address = (sys.argv[1], int(sys.argv[2]))
#server_address = ('100.27.30.197', 6666)
sock.connect(server_address)

while True:
    message = input()
    com = message.split( ) #注意此slipt以空格會分隔符
    count = len(com)
    if com[0] != 'draw' or count != 2:
        print('wrong command!')
    else:
        num = int(com[1])  #將input的數字字串轉成integer
        for x in range(num):
            sock.send(message.encode('utf-8')) #transform string to byte then send to server
            msg = sock.recv(2048)
            print(msg.decode('utf-8'))
sock.close()
