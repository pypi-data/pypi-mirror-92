from .database_connection import DatabaseConnection
import pandas as pd
import numpy as np

if __name__ == '__main__':

	client = DatabaseConnection.get_instance().get_client(use_arctic=True)
	# sdata = client['Static Data']
	mdata = client['Market Data']
	# referential = pd.read_csv('../../../data/Referential/referential_v0.csv', index_col=0)
	# sdata.write('Referential', referential)
	# list_symbol = referential.index
	# path = '../../../data/backup_h5/mdata_mongo_v0_'

	# for symbol in list_symbol:
	# 	print(symbol)
	# 	if '/' in symbol:
	# 		symbol = symbol.replace('/', '_')
	# 		df_symb = pd.read_hdf(path + symbol + '.h5')
	# 		print('modified '+symbol)
	# 		symbol = symbol.replace('_', '/')
	# 		print('modified '+symbol)
	# 		mdata.write(symbol, df_symb)
	# 	else:
	# 		df_symb = pd.read_hdf(path + symbol + '.h5')
	# 		mdata.write(symbol, df_symb)

	# ------------
	# Implied Vol
	# ------------
	vol = pd.read_csv('../../../data/csvs/Index_vol.csv', index_col=0, header=[0, 1], parse_dates=True)
	print(vol.head())
	list_index = []
	for col in vol.columns:
		list_index.append(col[0])
	symbols = np.unique(np.array(list_index))
	suffix = 'IMPVOL'
	#
	# for symbol in symbols:
	# 	df = vol[symbol]
	# 	df.to_hdf('../../../data/backup_h5/mdata_mongo_v0_'+symbol + ' ' + suffix + '.h5', key='df')
	# '''
	#
	# path = '../../../data/backup_h5/mdata_mongo_v0_'
	# for symbol in symbols:
	# 	df = pd.read_hdf(path + symbol + ' ' + suffix+'.h5')
	# 	mdata.write(symbol + ' ' + suffix, df)
