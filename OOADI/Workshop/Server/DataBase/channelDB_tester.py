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

class TestFloatOperations(unittest.TestCase):
	def setUp(self):											# Sets up (instantiates) a class to test all test cases
		self.Channel_DB_manager = Channel_DB()
	def test_lookupEmpty(self):
		print("")
		# Lookup tests
		key_lookup = 'Channel_name'
		channel_lookup = 'Hej'

		## Key lookup
		self.assertEqual(self.Channel_DB_manager.lookup(key=key_lookup),[])
		## Value lookup
		self.assertEqual(self.Channel_DB_manager.lookup(key=key_lookup,channel=channel_lookup),None)
		## Row lookup
		self.assertEqual(self.Channel_DB_manager.lookup(channel=channel_lookup),[])

	def test_createChannel(self):
		print("")
		new_channel = 'Channel_0'
		channel_creater = 'Account_0'

		self.Channel_DB_manager.createChannel(new_channel,channel_creater)

		self.assertEqual(self.Channel_DB_manager.lookup(channel=new_channel), [new_channel, [channel_creater], []])

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
		new_log_entrys = [['timestamp_0','user_0','msg_0'],['timestamp_1','user_1','msg_1'],['timestamp_2','user_2','msg_2'],['timestamp_3','user_3','msg_3']]
		for idx in range(len(new_channels)):
			self.Channel_DB_manager.createChannel(new_channels[idx],channel_creaters[idx])
			self.Channel_DB_manager.associateUser(new_channels[idx],new_users[idx])
			self.Channel_DB_manager.logEntry(new_channels[idx], new_log_entrys[idx])
			if (idx > 0):
				self.Channel_DB_manager.logEntry(new_channels[0], new_log_entrys[idx])

		key_lookup = self.Channel_DB_manager.columns[2]
		
		for idx in range(len(new_channels)):
			
			if idx == 0:
				self.assertEqual(self.Channel_DB_manager.lookup(channel=new_channels[idx]), [new_channels[idx], [channel_creaters[idx], new_users[idx]], [new_log_entrys[x] for x in range(len(new_log_entrys))]])
				self.assertEqual(self.Channel_DB_manager.lookup(key=key_lookup, channel=new_channels[idx],last_entry=False), [new_log_entrys[x] for x in range(len(new_log_entrys))])
				self.assertEqual(self.Channel_DB_manager.lookup(key=key_lookup, channel=new_channels[idx]), new_log_entrys[3])
			else:
				self.assertEqual(self.Channel_DB_manager.lookup(channel=new_channels[idx]), [new_channels[idx], [channel_creaters[idx], new_users[idx]], [new_log_entrys[idx]]])
				self.assertEqual(self.Channel_DB_manager.lookup(key=key_lookup, channel=new_channels[idx]), new_log_entrys[idx])

			print(f'Lookup return: {self.Channel_DB_manager.lookup(key=key_lookup, channel=new_channels[idx], last_entry=False)}')
if __name__=="__main__":
	unittest.main()