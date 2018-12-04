def parseFileName(filePath):
	name = filePath.split('/')
	name = name[len(name)-1].split('.')
	f = name[1]
	name = name[0]
	print(name)
	return name, f