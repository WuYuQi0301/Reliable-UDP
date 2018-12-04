def initPacket(_seqNum, _Data):
	return Packet(_seqNum, _Data)	

class Packet(object):
	"""docstring for Packet"""
	def __init__(self, _seqNum, _Data):
		self.seqNum = _seqNum
		self.data = _Data
		self.ackState = -1;

	def __lt__(self,other):#operator < 
		return self.seqNum < other.seqNum

	def __str__(self):
		return '(' + str(self.seqNum) + ")"
