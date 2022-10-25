class accountDB:
	def __init__(self):
		self.accDB = {
			"Username" : [],
			"Password" : [],
			"Associated Channels" : []
			}
	
	def lookUpAccount(self, Username):
		for c in self.accDB["Username"]:
			if c == Username:
				return True
		
		return False
	
	def createUser(self, Username, Password):
		if self.lookUpAccount(Username):
			return False
		else:
			self.accDB["Username"].append(Username)
			self.accDB["Password"].append(Password)
			self.accDB["Associated Channels"].append([])
			return True
	
	def logIn(self, Username, Password):
		if self.lookUpAccount(Username):
			self.index = self.accDB["Username"].index(Username)
			if self.accDB["Password"][self.index] == Password:
				return True
			else:
				return False
			
		else:
			return False
		
	def addChannel(self, Username, ChannelID):
		self.index = self.accDB["Username"].index(Username)
		for c in self.accDB["Associated Channels"][self.index]:
			if c == ChannelID:
				print("Channel already exists in account database")
				return False
		self.accDB["Associated Channels"][self.index].append(ChannelID)
		return True
	
	def printDB(self):
		print(self.accDB)