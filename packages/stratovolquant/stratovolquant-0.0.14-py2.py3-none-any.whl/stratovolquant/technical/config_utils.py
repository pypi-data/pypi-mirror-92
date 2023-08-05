import os
import configparser
# from datetime import timedelta
# from dateutil.relativedelta import *

from ..mongo import database_connection


class ConfigUtils:
    @staticmethod
    def load_config(db_name='UserConfig', library_name='WebApp'):
        connection = database_connection.DatabaseConnection.get_instance()
        poc_lib = connection.get_library('POC')
        poc_lib.collection_names()
        '''
        success, full_filename = ConfigUtils.find_full_filename('poc.json')
        with open(full_filename) as json_file:
            self.config = json.load(json_file)
        '''

    @staticmethod
    def read(filename):
        success, full_filename = ConfigUtils.find_full_filename(filename)
        if not success:
            raise Exception('Cannot find config filename {0}'.format(filename))

        interpolation = configparser.ExtendedInterpolation()
        config = configparser.ConfigParser(interpolation=interpolation, inline_comment_prefixes="#")
        config.read(full_filename)
        return config

    @staticmethod
    def find_full_filename(filename):
        success = False
        data_dir = None
        full_filename = None

        data_dir_list = ['../data/', '../../data/', '../../../data/']
        for data_dir in data_dir_list:
            if os.path.exists(data_dir):
                success = True
                break

        full_filename_list = [data_dir + 'private/' + filename,  data_dir + '/config/' + filename]
        if success:
            success = False
            for full_filename in full_filename_list:
                if os.path.isfile(full_filename):
                    success = True
                    break
        return success, full_filename

    '''
    @staticmethod
    def parse_frequency(frequency_str):
        qty_str, unit_str = frequency_str.split()
        qty = int(qty_str)

        if unit_str == 'D':
            return timedelta(days=qty)
        elif unit_str == 'W':
            return timedelta(weeks=qty)
        elif unit_str == 'M':
            return relativedelta(months=qty)
        elif unit_str == 'Y':
            return relativedelta(years=qty)
        else:
            return None
    '''