from .database_connection import DatabaseConnection
import pandas as pd
import numpy as np


def summary(library):
	symbols = library.list_symbols()
	df_summary = pd.DataFrame(index=symbols)
	versions = []
	start_dates = []
	end_dates = []
	for symbol in symbols:
		print(symbol)
		tmp = library.read(symbol).data
		sdate = tmp.index[0]
		edate = tmp.index[-1]
		v = library.list_versions(symbol)[0]['version']
		start_dates.append(sdate)
		end_dates.append(edate)
		versions.append(v)

	df_summary['Version'] = versions
	df_summary['Start date'] = start_dates
	df_summary['End date'] = end_dates

	return df_summary


if __name__ == '__main__':
	md_library = DatabaseConnection.get_instance().get_client(use_arctic=True)['Market Data']
	df_summary = summary(md_library)

	static_data_library = DatabaseConnection.get_instance().get_client(use_arctic=True)['Static Data']
	static_data_library.write('Market Data Summary', df_summary)
	mds = static_data_library.read('Market Data Summary').data
	print(mds)
