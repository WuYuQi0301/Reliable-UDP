# path python3
# coding utf-8

import socket
from sys import getsizeof

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
f = open("data.txt", mode='wb')
uniSize = 1024
# bing port
s.bind(('127.0.0.1', 9999))

print('Bing UDP on 9999')

for i in range(1):
# while True:
    #recv data
    data, addr = s.recvfrom(uniSize)
    print('Received from %s:%s.'% addr)
    seq = ord(bytes([data[0]]))      #int:
    ack = ord(bytes([data[1]]))      #int:
    print(seq)
    print(ack)
    for j in range(15):
        print(data[j])
    print(data)

    w = data[2:]
    f.write(w)

    reply = 'reply %d!' % data[0]
    s.sendto(reply.encode('utf-8'), addr)

s.close()

f.close()