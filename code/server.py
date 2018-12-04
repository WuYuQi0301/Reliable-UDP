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

# 服务端日志
logf = open('../log/server-log.txt', mode='w')

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

RcvBufferSize = 20 # 分配buffer数量
s.sendto(struct.pack(commandformat, RcvBufferSize, expSeqNum), addr)

# 接收文件信息
fileInfo, addr = s.recvfrom(1024)
f = open(str(fileInfo, encoding = 'utf-8'), mode='wb')
print("file info : ", fileInfo)
s.sendto(struct.pack(commandformat, RcvBufferSize, expSeqNum), addr)



ReceiveBuffer = PriorityQueue(RcvBufferSize) # 按缓存的seqNum从小到大排列
bufferedSeq = []
rwnd = RcvBufferSize            # 缓存可用空间

# f = open("data.txt", mode='wb')

# for i in range(1000):
while True:

	data, addr = s.recvfrom(uniSize)

	if len(data) == flowCtlrLen:  # flow control or close connection
		seq, testSeg = struct.unpack(flowCtlrFormat, data)
		if seq == 0 and testSeg == -2:
			print("Close connection pkt recieved")
			break
		else:
			logf.write("flow control pkt recieved : " + str(seq)+ "\n")
			s.sendto(struct.pack(flowCtlrFormat, seq, rwnd), addr)
			continue

	seq, ack, w = struct.unpack(format, data);
	logf.write("Recieved seq: " + str(seq)+ "\n")

	if seq < expSeqNum:    # 丢弃冗余分组
		logf.write("redundant pkt："+ str(seq)+ "\n")
		continue

	elif seq > expSeqNum:  # 若缓存仍有空间，缓存乱序到达的pkt
		if not ReceiveBuffer.full() and seq not in bufferedSeq:
			logf.write("put buffer : " + str(seq)+ "\n")
			ReceiveBuffer.put(initPacket(seq, w))
			bufferedSeq.append(seq)
			rwnd -= 1
	else :	               #seq == expSeqNum:
		ackSeq = seq
		f.write(w)
		expSeqNum += len(w)

		#检查buffer中有无 顺序可写的数据包
		if not ReceiveBuffer.empty():       # buffer不为空
			tmp = ReceiveBuffer.get()    # 取队头元素
			bufferedSeq.remove(tmp.seqNum)

			while tmp.seqNum <= expSeqNum:
				if tmp.seqNum < expSeqNum:    # 若队列中有小于expNum的缓存（冗余），丢弃
					if ReceiveBuffer.empty():
						break
					tmp = ReceiveBuffer.get()
					bufferedSeq.remove(tmp.seqNum)

				elif expSeqNum == tmp.seqNum: # 确认并写入磁盘
					ackSeq = tmp.seqNum
					f.write(w)
					expSeqNum += len(tmp.data)

					if ReceiveBuffer.empty():
						break
					tmp = ReceiveBuffer.get()
					bufferedSeq.remove(tmp.seqNum)

			if expSeqNum < tmp.seqNum:
				ReceiveBuffer.put(tmp)
				bufferedSeq.append(tmp.seqNum)

		rwnd = RcvBufferSize - ReceiveBuffer.qsize()
		logf.write("get excepted : " + str(seq) + "update expNum to : " + str(expSeqNum)+ "\n")

		# 发送ack				
		ackPkt = struct.pack(ackformat, ackSeq, rwnd)
		s.sendto(ackPkt, addr)


#close connection
s.sendto(struct.pack(commandformat, seq+1, 1), addr)

s.sendto(struct.pack(commandformat, seq+1, 2), addr)


s.close()
f.close()
logf.close()