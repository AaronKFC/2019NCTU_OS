import socket
import sys

host = '127.0.0.1'
port = 10001
address = (host, port)
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect(address)
imgFile = open('video.mp4', "rb+")
while True:
    imgData = imgFile.readline(512)
    if not imgData:
        break
    socket.send(imgData)
imgFile.close()
socket.close()
