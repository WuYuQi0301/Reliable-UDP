# path python3
# coding utf-8

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# bing port
s.bind(('127.0.0.1', 9999))

print('Bing UDP on 9999')

while True:
    #recv data
    data, addr = s.recvfrom(1030)
    print('Received from %s:%s.'% addr)
    print(data[0])
    reply = 'Hello, %d!' % data[0]
    s.sendto(reply.encode('utf-8'), addr)

s.close()