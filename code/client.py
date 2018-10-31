# path python3
# 
import socket
import random

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
f = open('../testdata/testpdf.pdf', mode='rb')
mss = 1024
seq = random.randint(1,170)
print(str(seq))
# while True:
# replyBuffer = [1024]
for i in range(3):
    test = bytes(seq) + bytes('0', 'utf-8') + f.read(mss)
    print(len(bytes(seq)))
    s.sendto(test, ('127.0.0.1',9999))
    reply = s.recvfrom(1024)
    print(reply)
    seq = seq + 1

# for data in [b'Michael', b'Tracy', b'Sarah']:
#     print(s.recv(1024).decode('utf-8'))
#     s.sendto(data, ('127.0.0.1', 9999))


f.close()

s.close()