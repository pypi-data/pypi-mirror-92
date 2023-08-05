class ReferentialInstance:

	def __init__(self, mongo_client, symbol):
		self.symbol = symbol
		self.referential = mongo_client['MData'].Referential
		self.cursor = self.referential.find_one({'Symbol': self.symbol})

	def get_(self, key):
		if key not in self.cursor.keys():
			return None
		else:
			return self.cursor[key]

	def add_(self, key, value):
		if key in self.cursor.keys():
			print(key + ' already in ' + self.symbol + ' referential')
		else:
			self.referential.update_one({'Symbol': self.symbol}, {'$set': {key: value}})
			print(key + ':' + str(value) + ' added')

	def mod_(self, key, value):
		if key not in self.cursor.keys():
			print(key + ' not in ' + self.symbol + ' referential')
		else:
			self.referential.update_one({'Symbol': self.symbol}, {'$set': {key: value}})
			print(key + ' value modified to ' + str(value))


if __name__ == '__name__':
	from . import database_connection
	mongo_client = database_connection.DatabaseConnection.get_instance().get_client()
	referential = mongo_client['MData'].Referential
	cursor = referential.find({})
	print(cursor[0])
