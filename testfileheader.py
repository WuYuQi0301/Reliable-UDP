

f1 = open("./testdata/saveVideo.avi", "rb")
t = f1.read(1024)
for i in range(15):
    print(ord(bytes([t[i]])))
print(t)
f1.close()