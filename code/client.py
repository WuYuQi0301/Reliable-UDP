# path python3
# 
import socket
import random

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
f = open('../testdata/saveVideo.avi', mode='rb')
# seq = random.randint(1,100)
seq = 1
print("seq "+ str(seq))
mss = 1024 - 2 #读取字节数

for i in range(1):
    data = f.read(mss)
    test = bytes([seq]) + bytes([0]) + data
    s.sendto(test, ('127.0.0.1',9999))
    reply = s.recvfrom(1024)          #字节数
    print(reply)
    seq = seq + 1

f.close()

s.close()