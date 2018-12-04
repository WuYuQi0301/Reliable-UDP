import os
from parse import parseFileName
file = "../testData/saveVideo.avi"
# print(os.path.exists(file))
# name = file.split('/')
# name = name[len(name)-1].split('.')
# name = name[0]
# f = name[1]
# print(name)

# print(f)
name, f = parseFileName(file)
print(name, f)