# path python3
import socket
import random
import struct
import os
from packet import initPacket


def replyDownload(s, RcvBuffer, addr):
	# 服务端日志
	logf = open('../log/server-log.txt', mode='w')
	logf.write("Replying Download ")	
	print("Replying Download ")	
	
	uniSize = 1024 + 8
	commandformat = '2I'
	ackformat = '2I'
	mss = 1024 #读取字节数
	format = '2I1024s'
	flowCtlrFormat = 'Ii'
	flowCtlrLen = struct.calcsize(flowCtlrFormat)
	receiveSize = 8

	InitialSeqNum = 1
	print("Replying InitialSeqNum ")	
	s.sendto(struct.pack(commandformat, 1, InitialSeqNum), addr)
	
	while True :
		fileInfo, addr = s.recvfrom(1024)

		if len(fileInfo)!=8:
			fileInfo = str(fileInfo, encoding = 'utf-8')
			print("File Info : ", fileInfo)
			break

	if os.path.exists(fileInfo) == False:
		s.sendto(struct.pack(commandformat, InitialSeqNum, 0), addr)
		print("file requested does not exists")
		return

	print("ACK file exist")	
	s.sendto(struct.pack(commandformat, InitialSeqNum, 1), addr)
	s.setblocking(0)

	f = open(fileInfo, mode = 'rb')

	# 超时重传机制
	TTL = 3
	Timer = 3;

	RcvBuffer = 0

	# GBN机制
	Sendbase = InitialSeqNum   # 已发送但未被确认的最小序号
	NextSeqNum = InitialSeqNum # 下一个要发送的字节序号
	Window = []                # 缓存已发送但未确认的分组
	windowSize = 10            # 窗口大小
	baseIndex = 0
	avaliable = 0

	# 流控制机制
	LastByteSent = 0;    # 最后一个已经发送的字节
	LastByteAcked = 0;    # 最后一个被确认的字节
	rwnd = RcvBuffer

	FileEndFlag = 0
	AllAcked = 0

	# 拥塞控制机制
	cwnd = 1
	ssthresh = 16
	State = 0             # 0：慢启动， 1：拥塞避免
	dupACKcount = 0
	lastACK = 0

	print("Starting file transmition")
	# for i in range(1000):
	while FileEndFlag == 0 or AllAcked == 0:
		#event : data recieved from application : bug not fixed
		if (LastByteSent-LastByteAcked) <= rwnd*mss and (NextSeqNum-Sendbase)/mss < windowSize:
		
			data = f.read(mss)
			if len(data) < mss: #补长
				data = data + bytes(mss-len(data))
				FileEndFlag = 1

			Window.append(initPacket(NextSeqNum, data))
			AllAcked = 0

			s.sendto(struct.pack(format, NextSeqNum, 0, data), addr)

			logf.write("sending : " + str(NextSeqNum))
			for x in range(len(Window)):
				logf.write(str(Window[x].seqNum))
			logf.write("\n")

			LastByteSent = NextSeqNum - 1
			NextSeqNum = NextSeqNum + mss

		elif (LastByteSent-LastByteAcked) > rwnd*mss:
			logf.write('\nsending flowCtlr pkt : '+ str(NextSeqNum-mss)+ ' rwnd : '+str(rwnd)+ "\n")
			logf.write('LastByteSent : '+ str(LastByteSent) + 'LastByteAcked : '+ str(LastByteAcked)+ "\n")
			s.sendto(struct.pack(flowCtlrFormat, NextSeqNum-mss, -1), addr)
		# NextSeqNum = NextSeqNum + 1

		#event : ACK received, with field value of y
		reply = 0;
		try:
			reply, dstAddr = s.recvfrom(receiveSize)
			ackSeq, rwnd = struct.unpack(ackformat, reply)
		
			LastByteAcked = ackSeq + mss  # 流控制中，ack seq 不变化

			if lastACK != ackSeq:
				if State == 0:
					cwnd += 1
				else: 
					cwnd += 1/cwnd			
				dupACKcount = 0
				lastACK = ackSeq
			else :
				duoACKcount += 1


			logf.write("recieve ACK : "+str(ackSeq))
			for x in range(len(Window)):
				logf.write(str(Window[x].seqNum))

			if Sendbase <= ackSeq:        # 累计确认，之前的都是正确确认收到的	

				Sendbase = ackSeq + mss
				logf.write("update sendbase : " + str(Sendbase) + "\n")
				while len(Window) != 0:
					if Window[0].seqNum < Sendbase:
						del Window[0]
					else: break
				if Sendbase != NextSeqNum:  #如果当前还有已发送但未被确认的分组: reset timer
					Timer = 0;
				if len(Window) == 0:
					AllAcked = 1


			# print(reply)
			logf.write("updated Window : ")
			for x in Window:
				logf.write(str(x.seqNum))

		except BlockingIOError:
			pass
	
		#event : timer out / duoACKcount
		Timer += 1
		if Timer == TTL or dupACKcount == 3:
			State = 0
			ssthresh = cwnd / 2
			cwnd = 1
			duoACKcount = 0
			Timer = 0

			# if Sendbase != NextSeqNum and (LastByteSent-LastByteAcked) <= rwnd*mss: 
			if len(Window) != 0:	#retransmit not-ack pkt with smallest seq(Sendbase)(Window[0])?
				logf.write("TIME OUT : retransmit " +str(Window[0].seqNum)+ "\n")
				retransmit = struct.pack(format, Window[0].seqNum, 0, Window[0].data)
				s.sendto(retransmit, addr)

	#挥手
	Timer = 3
	while True:
		print("Starting connection closing")
		FIN = -2
		if Timer == 3:
			s.sendto(struct.pack(flowCtlrFormat, 0, FIN), addr)
			Timer = 0
		Timer += 1
		try:
			reply, addr = s.recvfrom(receiveSize)
			seq, FIN = struct.unpack(commandformat, reply)
			print("Close connection ack recieved")
		
			while True:
				try :
					reply, addr = s.recvfrom(receiveSize)
					print("third wave recieved")
					break
				except BlockingIOError:
					pass
			break
		except BlockingIOError:
			pass

	f.close()
	# s.close()
	logf.close()