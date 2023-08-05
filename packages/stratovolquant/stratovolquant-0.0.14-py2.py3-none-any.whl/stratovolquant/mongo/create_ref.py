import pandas as pd
from .database_connection import DatabaseConnection
from pprint import pprint


if __name__ == '__main__':
	df = pd.read_csv('../../../data/Referential/referential_v0.csv')
	# print(df.head())
	dico_ref = df.to_dict()
	# print(df.shape[0])
	mongo_client = DatabaseConnection.get_instance().get_client()
	db = mongo_client['MData']
	cursor = db.Referential.find_one({'Symbol': 'SPX Index'})
	# print( 'sdq' in cursor.keys())
	# db.Referential.update_one({'Symbol': 'SPX Index'}, {'$set':{'tenor': '102'}})
	# for i in range(df.shape[0]):
	# 	dic = df.iloc[i, :].to_dict()
	# 	print(df.iloc[i, :].to_dict())
	# 	db.Referential.insert_one(dic)


