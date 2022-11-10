class account_DB(object):
	def __init__(self):
		self.accDB = {
			"Username" : [],
			"Password" : []
			}
	

	def lookUpAccount(self, Username):
		if Username in self.accDB["Username"]:
			return True
		else:
			return False


	def createUser(self, Username, Password):
		if self.lookUpAccount(Username):
			print(f'{Username} already exist')
			return False
		else:
			self.accDB["Username"].append(Username)
			self.accDB["Password"].append(Password)
			print(f'User {Username} was succesfully created')
			return True
	

	def logIn(self, Username, Password):
		if self.lookUpAccount(Username):
			self.index = self.accDB["Username"].index(Username)
			if self.accDB["Password"][self.index] == Password:
				print(f'Succesful login to user: {Username}')
				return True

		print(f'Failed login attempt for user {Username}')
		return False