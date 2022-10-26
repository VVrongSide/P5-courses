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
		else:
			self.dictionary['Channel_name'].append(Channel_name)
			self.dictionary['Channel_members'].append([Account])
			self.dictionary['Channel_log'].append([])
			print(f'Added the Channel_name: |{Channel_name}| with Channel_members: |{Account}|')

	def associateUser(self, Channel_name, Account):
		if Channel_name not in self.dictionary['Channel_name']:
			print(f'Channel: |{Channel_name}| does not exist')
		else:
			index = self.dictionary['Channel_name'].index(Channel_name)
			if Account in self.dictionary['Channel_members'][index]:	# Checking if the Channel_name exists in the dictionary
				print(f'{Account} already exists in that channel') 		
			else:
				self.dictionary['Channel_members'][index].append(Account)
				print(f'Asoociated |{Account}| to |{Channel_name}| members')
	
	def lookup(self, key=None, channel=None, Bool=False):
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
				if self.indexExists(self.dictionary[key],index):
					if Bool:
						return self.dictionary[key][index]
					else:
						return self.dictionary[key][-1:][0]
				else:
					print(f'Channel: |{channel}| does not exist')
		elif channel is not None:
			lookup = []
			if channel not in self.dictionary['Channel_name']:
				print(f'Channel: |{channel}| does not exist')
			else:
				index = self.dictionary['Channel_name'].index(channel)
				for column in self.columns:
					if self.indexExists(self.dictionary[column],index):
						lookup.append(self.dictionary[column][index])
					else:
						if (len(self.dictionary[column])-1) < 0:
							print(f'There are currently no channels in the database')
							return
						else:
							print(f'channel: |{channel}| does not exist, largest index is {len(self.dictionary[column])-1}')
							return
			return lookup	
		elif key is not None:
			return self.dictionary[key]
		else:
			return self.dictionary

	def run(self):	
		return

