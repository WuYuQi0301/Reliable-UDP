# client.py
# 
# 
# LFTP lsend 127.0.0.1 ../testData/saveVideo.avi
import socket
import random
import struct
import os
from packet import initPacket
from Upload import UploadFile


commandLine = 0
commandLine = input("enter command, 'q' to quit : ")

while commandLine != "q":
	command = commandLine.split()

	#命令格式错误
	if len(command) != 4 or command[0] != "LFTP" or (command[1]!="lsend" and command[1]!="lget"):
		print("command format error")
		commandLine = input("enter command, 'q' to quit : ")
		continue

	#上传文件
	if command[1] == "lsend":
		if os.path.exists(command[3]) == False:
			print("File does not exists")
			continue

		file = command[3]
		url = command[2]
		print("Commanding : upload file ", file, " to ", url)

		UploadFile(file, url)

	#下载文件
	elif command[1] == "lget":
		file = command[3]
		url = command[2]
		print("Commanding : download file ", file, " from ", url)

		DownloadFile(file, url)
	commandLine = input("enter command, 'q' to quit : ")