class account_DB(object):
	def __init__(self):
		# Initialize the dictionary
		self.accDB = {
			"Username" : [],
			"Password" : [],
			"Associated Channels" : []
			}
	
	# Check if account exists
	def lookUpAccount(self, Username):
		if Username in self.accDB["Username"]:
			return True
		else:
			return False

	# Call lookUpAccount, and append account to dictionary if the account doesn't exist
	def createUser(self, Username, Password):
		if self.lookUpAccount(Username):
			print(f'{Username} already exist')
			return False
		else:
			self.accDB["Username"].append(Username)
			self.accDB["Password"].append(Password)
			self.accDB["Associated Channels"].append([])
			print(f'User {Username} was succesfully created')
			return True
	
	# Call lookUpAccount, and return successful if the account exists AND the password given matches the one in dictionary.
	def logIn(self, Username, Password):
		if self.lookUpAccount(Username):
			self.index = self.accDB["Username"].index(Username)
			if self.accDB["Password"][self.index] == Password:
				print(f'Succesful login to user: {Username}')
				return True

		print(f'Failed login attempt for user {Username}')
		return False

	# If a user is not member of a given channel, add it to the dictionary entry for channels the user is member of
	def addChannel(self, Username, ChannelID):
		self.index = self.accDB["Username"].index(Username)
		if ChannelID in self.accDB["Associated Channels"][self.index]:
			print("Channel already exists in account database")
			return
		self.accDB["Associated Channels"][self.index].append(ChannelID)
		print(f'{Username} succesfully associated with channel: {ChannelID}')
		return

	# Return a list of the channels a given user is a member off.
	def memberOfChannels(self, Username):
		self.index = self.accDB["Username"].index(Username)
		return self.accDB["Associated Channels"][self.index]