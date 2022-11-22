import pickle
from cryptography import fernet

class Client_DB(object):
	
	def __init__(self):
		self.columns = ['Channel_name','Channel_key']
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

	def createChannel(self, Channel_name, Key):
		
		if Channel_name in self.dictionary[self.columns[0]]:
			print(f'{Channel_name} already exists') 		# Checking if the Channel_name exists in the dictionary
			return False
		else:
			self.dictionary[self.columns[0]].append(Channel_name)
			self.dictionary[self.columns[1]].append([Key])
			print(f'Added the Channel_name: |{Channel_name}| with key: |{Key}|')
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
	
	def lookup(self, key=None, channel=None, last_entry=True):
		"""
		If argument |channel=int| is stated, it returns the channel of the channel database
		if |key=str| is defined it returns the column for the str
		if |key=str| and |value=int| is defines, it returns a specific entry in the database 
		"""
		print("lookup: ", 1)
		if (channel and key) is not None:
			if channel not in self.dictionary[self.columns[0]]:
				print(f'Channel: |{channel}| does not exist')
			else:
				index = self.dictionary[self.columns[0]].index(channel)
				print("lookup: ", 2)
				if last_entry:
					print("lookup: ", 3)
					return self.dictionary[key][index][-1:][0]
				else:
					print("lookup: ", 4)
					print(key,":_Key  Index:" ,index)
					print(self.dictionary[key][index][0])
					return self.dictionary[key][index][0]

		elif channel is not None:
			print("lookup: ", 5)
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
