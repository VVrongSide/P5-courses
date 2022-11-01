import pickle

class Client_DB(object):
	
	def __init__(self):
		self.columns = ['Channel_name','Channel_key','Channel_log']
		self.dictionary = self.constructDict()

	def __str__(self):
		for k, v in self.dictionary.items():
			print(f'{k}: {v}')
		return f''

	def indexExists(self, list,index):
		try:
			list[index]
			return True
		except IndexError:
			return False

	def constructDict(self):
		tempDict = {}
		for column in self.columns:
			tempDict[column] = []
		return tempDict

	def createChannel(self, Channel_name, Account):
		
		if Channel_name in self.dictionary[self.columns[0]]:
			print(f'{Channel_name} already exists') 		# Checking if the Channel_name exists in the dictionary
			return False
		else:
			self.dictionary[self.columns[0]].append(Channel_name)
			self.dictionary[self.columns[1]].append([Account])
			self.dictionary[self.columns[2]].append([])
			print(f'Added the Channel_name: |{Channel_name}| with Channel_members: |{Account}|')
			return True

	def associateKey(self, Channel_name, Key):
		if Channel_name not in self.dictionary[self.columns[0]]:
			print(f'Channel: |{Channel_name}| does not exist')
			return False
		else:
			index = self.dictionary[self.columns[0]].index(Channel_name)
			if Key in self.dictionary[self.columns[1]][index]:	# Checking if the Channel_name exists in the dictionary
				print(f'{Key} already exists in that channel')
				return False 		
			else:
				self.dictionary[self.columns[1]][index].append(Key)
				print(f'Asoociated |{Key}| to |{Channel_name}| members')
				return True
	
	def logEntry(self, Channel_name, msg):
		if Channel_name not in self.dictionary[self.columns[0]]:
			print(f'Channel: |{Channel_name}| does not exist')
		else:
			index = self.dictionary[self.columns[0]].index(Channel_name)
			self.dictionary[self.columns[2]][index].append(msg)
			print(f'Log entry into Channel: |{Channel_name}| succesful')

	def lookup(self, key=None, channel=None, last_entry=True):
		"""
		If argument |channel=int| is stated, it returns the channel of the channel database
		if |key=str| is defined it returns the column for the str
		if |key=str| and |value=int| is defines, it returns a specific entry in the database 
		"""
		if (channel and key) is not None:
			if channel not in self.dictionary[self.columns[0]]:
				print(f'Channel: |{channel}| does not exist')
			else:
				index = self.dictionary[self.columns[0]].index(channel)
				if last_entry:
					return self.dictionary[key][index][-1:][0]
				else:
					return self.dictionary[key][index]

		elif channel is not None:
			lookup = []
			if channel not in self.dictionary[self.columns[0]]:
				print(f'Channel: |{channel}| does not exist')
			else:
				index = self.dictionary[self.columns[0]].index(channel)
				for column in self.columns:
					lookup.append(self.dictionary[column][index])

			return lookup

		elif key is not None:
			return self.dictionary[key]
		else:
			return self.dictionary
if __name__=="__main__":

	# Format for a channel log
	"""
	channel_log = {
				"time": [],
				"user": [],
				"message": []
			}
	"""
	Client_DB_manager = Client_DB()
	filename = 'Client_DB_manager.txt'
	with open(filename, "wb") as f:
		pickle.dump(Client_DB_manager, f)
