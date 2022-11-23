import pickle

class Channel_DB(object):
	
	def __init__(self):
		self.columns = ['Channel_name','Channel_members','Channel_log']
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
		
		if Channel_name in self.dictionary['Channel_name']:
			print(f'{Channel_name} already exists') 		# Checking if the Channel_name exists in the dictionary
			return False
		else:
			self.dictionary['Channel_name'].append(Channel_name)
			self.dictionary['Channel_members'].append([Account])
			self.dictionary['Channel_log'].append([])
			print(f'Added the Channel_name: |{Channel_name}| with Channel_members: |{Account}|')
			return True

	def associateUser(self, Channel_name, Account):
		if Channel_name not in self.dictionary['Channel_name']:
			print(f'Channel: |{Channel_name}| does not exist')
			return False
		else:
			index = self.dictionary['Channel_name'].index(Channel_name)
			if Account in self.dictionary['Channel_members'][index]:	# Checking if the Channel_name exists in the dictionary
				print(f'{Account} already exists in that channel')
				return False 		
			else:
				self.dictionary['Channel_members'][index].append(Account)
				print(f'Asoociated |{Account}| to |{Channel_name}| members')
				return True
	
	def logEntry(self, Channel_name, username, msg):
		if Channel_name not in self.dictionary['Channel_name']:
			print(f'Channel: |{Channel_name}| does not exist')
		else:
			index = self.dictionary['Channel_name'].index(Channel_name)
			self.dictionary['Channel_log'][index].append([username, msg])
			print(f'Log entry into Channel: |{Channel_name}| succesful')

	def lookup(self, key=None, channel=None, last_entry=True):
		"""
		If argument |channel=int| is stated, it returns the channel of the channel database
		if |key=str| is defined it returns the column for the str
		if |key=str| and |value=int| is defines, it returns a specific entry in the database 
		"""
		if (channel and key) is not None:
			if channel not in self.dictionary['Channel_name']:
				print(f'Channel: |{channel}| does not exist')
			else:
				index = self.dictionary['Channel_name'].index(channel)
				if last_entry:
					return self.dictionary[key][index][-1:][0]
				else:
					return self.dictionary[key][index][0]

		elif channel is not None:
			lookup = []
			if channel not in self.dictionary['Channel_name']:
				print(f'Channel: |{channel}| does not exist')
			else:
				index = self.dictionary['Channel_name'].index(channel)
				for column in self.columns:
					lookup.append(self.dictionary[column][index])

			return lookup

		elif key is not None:
			return self.dictionary[key]
		else:
			return self.dictionary

	def run(self):	
		return

if __name__=="__main__":

	# Format for a channel log
	"""
	channel_log = {
				"time": [],
				"user": [],
				"message": []
			}
	"""
	Channel_DB_manager = Channel_DB()
	filename = 'Channel_DB_manager.txt'
	with open(filename, "wb") as f:
		pickle.dump(Channel_DB_manager, f)

