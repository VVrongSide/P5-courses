import unittest
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
		else:
			self.dictionary['Channel_name'].append(Channel_name)
			self.dictionary['Channel_members'].append([Account])
			self.dictionary['Channel_log'].append(None)
			print(f'Added the Channel_name: |{Channel_name}| with Channel_members: |{Account}|')

	def associateUser(self, Channel_name, Account):
		if Channel_name not in self.dictionary['Channel_name']:
			print(f'Channel: |{Channel_name}| does not exist')
		else:
			index = self.dictionary['Channel_name'].index(Channel_name)
			if Account in self.dictionary['Channel_members'][index]:	# Checking if the Channel_name exists in the dictionary
				print(f'{Account} already exists in that channel\n') 		
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
						#raise Exception(f'There are currently no rows in the database')
						print(f'There are currently no rows in the database')
						return
					else:
						#raise Exception(f'Row: |{row}| does not exist, largest index is {len(self.dictionary[column])-1}')
						print(f'Row: |{row}| does not exist, largest index is {len(self.dictionary[column])-1}')
						return
			return lookup
		elif key is not None:
			return self.dictionary[key]
		elif value is not None:
			if self.indexExists(self.dictionary[key],value):
				return self.dictionary[key][value]
			else:
				print(f'Value: |{value}| deos not exist')
		else:
			return self.dictionary

	def run(self):	
		return

class TestFloatOperations(unittest.TestCase):
	def setUp(self):											# Sets up (instantiates) a class to test all test cases
		self.Channel_DB_manager = Channel_DB()
	def test_lookupEmpty(self):
		print("")
		# Lookup tests
		key_lookup = 'Channel_name'
		value_lookup = 0
		row_lookup = 0

		## Key lookup
		self.assertEqual(self.Channel_DB_manager.lookup(key=key_lookup),[])
		## Value lookup
		self.assertEqual(self.Channel_DB_manager.lookup(key=key_lookup,value=value_lookup),[])
		## Row lookup
		self.assertEqual(self.Channel_DB_manager.lookup(row=row_lookup),None)

	def test_createChannel(self):
		print("")
		new_channel = 'Channel_0'
		channel_creater = 'Account_0'

		self.Channel_DB_manager.createChannel(new_channel,channel_creater)

		self.assertEqual(self.Channel_DB_manager.lookup(row=0), [new_channel, [channel_creater], None])

	def test_associateUser(self):
		print("")
		new_channel = 'Channel_0'
		channel_creater = 'Account_0'

		self.Channel_DB_manager.createChannel(new_channel,channel_creater)

		new_user = 'Account_1'

		self.Channel_DB_manager.associateUser(new_channel,new_user)

		self.assertEqual(self.Channel_DB_manager.lookup(key='Channel_members'),[[channel_creater,new_user]])

	def test_total(self):
		new_channels = ['Channel_0','Channel_1','Channel_2','Channel_3']
		channel_creaters = ['Account_0','Account_1','Account_2','Account_3']
		new_users = ['Account_1','Account_0','Account_3','Account_2']
		for idx in range(len(new_channels)):
			self.Channel_DB_manager.createChannel(new_channels[idx],channel_creaters[idx])
			self.Channel_DB_manager.associateUser(new_channels[idx],new_users[idx])

		for idx in range(len(new_channels)):
			self.assertEqual(self.Channel_DB_manager.lookup(row=idx), [new_channels[idx], [channel_creaters[idx], new_users[idx]], None])

if __name__=="__main__":
	unittest.main()