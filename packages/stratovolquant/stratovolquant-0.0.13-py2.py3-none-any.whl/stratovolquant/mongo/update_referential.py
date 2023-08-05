from mongo.database_connection import DatabaseConnection
from mongo.referential_instance import ReferentialInstance

if __name__ == '__main__':

	# regex = {'ER' + 'i' + 'Comdty', 'ED' + 'i' + 'Comdty'}

	# symbols = ['ER' + str(i) + ' Comdty' for i in range(1, 10)] + ['ED' + str(j) + ' Comdty' for j in range(1, 10)]

	# for symbol in symbols:
	# 	r = ReferentialInstance(symbol)
	# 	r.add_(key='Return factor', value=-1)

	client = DatabaseConnection.get_instance().get_client()
	r = ReferentialInstance(client, 'SPX Index')
	if r.get_(key='Return Factor') == -1:
		print('yes')
	else:
		print('no')
