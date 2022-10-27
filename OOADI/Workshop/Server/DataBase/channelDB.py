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
	
	def logEntry(self, Channel_name, msg):
		if Channel_name not in self.dictionary['Channel_name']:
			print(f'Channel: |{Channel_name}| does not exist')
		else:
			index = self.dictionary['Channel_name'].index(Channel_name)
			self.dictionary['Channel_log'][index].append(msg)
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
					return self.dictionary[key][index]

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

#if __name__=="__main__":
	## To create Channel_DB_manager.txt pickle file
	#Channel_DB_manager = Channel_DB()
	
	## To populate the database
	#new_channels = ['Channel_0','Channel_1','Channel_2','Channel_3']
	#channel_creaters = ['Account_0','Account_1','Account_2','Account_3']
	#new_users = ['Account_1','Account_0','Account_3','Account_2']
	#new_log_entrys = [['timestamp_0','user_0','msg_0'],['timestamp_1','user_1','msg_1'],['timestamp_2','user_2','msg_2'],['timestamp_3','user_3','msg_3']]
	#for idx in range(len(new_channels)):
	#	Channel_DB_manager.createChannel(new_channels[idx],channel_creaters[idx])
	#	Channel_DB_manager.associateUser(new_channels[idx],new_users[idx])
	#	Channel_DB_manager.logEntry(new_channels[idx], new_log_entrys[idx])
	#	if (idx > 0):
	#		Channel_DB_manager.logEntry(new_channels[0], new_log_entrys[idx])
	
	## To store the pickle database manager
	#with open('Channel_DB_manager.txt', "wb") as pickle_file:
	#		pickle.dump(Channel_DB_manager, pickle_file)