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
	
	def lookup(self, key=None, value=None, row=None):
		"""
		If argument |row=int| is stated, it returns the row of the channel database
		if |key=str| is defined it returns the column for the str
		if |key=str| and |value=int| is defines, it returns a specific entry in the database 
		"""
		if row is not None:
			lookup = []
			for column in self.columns:
				if self.indexExists(self.dictionary[column],row):
					lookup.append(self.dictionary[column][row])
				else:
					if (len(self.dictionary[column])-1) < 0:
						print(f'There are currently no rows in the database')
						return
					else:
						print(f'Row: |{row}| does not exist, largest index is {len(self.dictionary[column])-1}')
						return
			return lookup	
		elif (value and key) is not None:
			if self.indexExists(self.dictionary[key],value):
				return self.dictionary[key][value]
			else:
				print(f'Value: |{value}| deos not exist')
		elif key is not None:
			return self.dictionary[key]
		else:
			return self.dictionary

	def run(self):	
		return

