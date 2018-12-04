import queue
import threading
import time

exitFlag = 0

class myThread(threading.Thread):
	def __init__(self, threadID, name, q):
		threading.Thread.__init__(self)
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.q = q
	def runListening(self):
		print("开启监听线程："+self.name)
		Listen(self.name, self.q)
		print("退出监听线程："+self.name)

def Listen():
	pass

import queue
import socket
import threading

def jonnyS():
	try:
		client.settimeout(500)
		buf = client.recv(2048)
		client.sendto(buf, addr)
	except s.timeout:
		print("timeout")
	client.close()

	
def main():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind(('127.0.0.1', 9999))
	print('Bing UDP on 9999')

	while True:
		client, addr = s.recvfrom(1024)
		thread = threading.Thread(target = jonnyS, args=(client, addr))
		thread.start()

if __name__ == '__main__':
	main()