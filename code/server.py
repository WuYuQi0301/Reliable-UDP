# path python3
# coding utf-8
# cd Desktop/CNproject/code
import socket
import struct
import os
from queue import PriorityQueue
from packet import initPacket

#一些参数
uniSize = 1024 + 8
format = '2I1024s'
commandformat = '2I'
ackformat = '2I'
flowCtlrFormat = 'Ii'
flowCtlrLen = struct.calcsize(flowCtlrFormat)



# 服务端打开socket接受连接请求
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1', 9999))
print('Bing UDP on 9999')

# while True:
# text, addr = s.recvfrom(struct.calcsize(commandformat))
	# set up connection： bug not fixed
text, addr = s.recvfrom(struct.calcsize(commandformat))
command, expSeqNum = struct.unpack(commandformat, text)
print("Received command from ", addr, " command : ", command, " expSeq : ", expSeqNum)

if command == 1   # 上传命令

	replyUpload(expSeqNum, addr)


elif command == 0 # 下载命令

	replyDownload(addr)