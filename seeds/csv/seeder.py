from flask import current_app
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial
from extensions.database import db
from models.model import Kaggle_D1_Fraud_Data, Kaggle_D1_IpAddress_To_Country, Kaggle_D1_meta
from flask_seeder import Seeder, Faker, generator
from classes.file_class import File_class
from modules.sql_no_context_module import bulk_insert_no_context, raw_sql_execute_no_context
from modules.timer_module import timer_func
from datetime import datetime
import pandas as pd
import pathlib
import time
import hashlib

actual_dir = pathlib.Path().absolute()
csv_loc = f'{actual_dir}/seeds/csv/'


class Kaggle_D1_IpAddress_To_Country_Seeder(Seeder):
    def __init__(self, db=None):
        Seeder.__init__(self, db=db)
        self.priority = 1

    @timer_func
    def run(self):
        names = ['lb_ip_address', 'ub_ip_address', 'country']
        filepath = csv_loc + 'fraud_ecommerce/IpAddress_to_Country.csv'

        file_fun = File_class(names=names, filepath=filepath)

        partial_function = partial(self.process_csv, file_fun)

        # returnarray = []

        if partial_function:
            # print('multithread_csv_partial_function2a')
            file_fun.set_start_rows_of_csv()
            # print(
            #     f'multithread_csv_partial_function2b: {file_fun.csv_rowstart_array}')
            # print(f'partial_function1 workers: {file_fun.workers}')
            with ThreadPoolExecutor(max_workers=5) as executor:
                # print('ThreadPoolExecutor1')
                # returnarray.append(executor.map(partial_function, file_fun.csv_rowstart_array))
                futures = [executor.submit(self.process_csv, row_start, file_fun)
                           for row_start in file_fun.csv_rowstart_array]
                # process each result as it is available
                for future in as_completed(futures):
                    # get the downloaded url data
                    df_chunk = future.result()
                    # print(f'df_chunk: {df_chunk}')
                    # check for no data
                    # if df_chunk is None:
                    #     print(f'>Error downloading {url}')
                    #     continue
                    # # save the data to a local file
                    # outpath = save_file(url, data, path)
                    # # report progress
                    # print(f'>Saved {url} to {outpath}')

        # returnarray = self.multithread_csv_partial_function(partial_function)

        # print(f'returnarray: {returnarray}')

    def process_csv(self, row_start, file_fun):
        # print(f'process_csv row_start: {row_start}')
        # print(f'process_csv file_fun.get_file_rows: {file_fun.get_file_rows}')
        # print(f'process_csv file_fun.rows_to_get: {file_fun.rows_to_get}')
        # print(f'process_csv file_fun.names: {file_fun.names}')
        # print(f'process_csv file_fun.filepath: {file_fun.filepath}')

        # sql_fun = Sql_class()

        df = file_fun.get_file_rows(
            row_start, file_fun.rows_to_get, file_fun.names, file_fun.filepath)

        # print(f'process_csv df: {df}')

        bulk_insert_no_context(Kaggle_D1_IpAddress_To_Country, df)

        return df


class Kaggle_D1_Fraud_Data_Seeder(Seeder):
    def __init__(self, db=None):
        Seeder.__init__(self, db=db)
        self.priority = 2

    @timer_func
    def run(self):
        names = ['id', 'signup_time', 'purchase_time', 'purchase_value',
                 'device_id', 'source', 'browser', 'sex', 'age', 'ip_address', 'is_fraud']
        filepath = csv_loc + 'fraud_ecommerce/Fraud_Data.csv'

        file_fun = File_class(names=names, filepath=filepath)

        partial_function = partial(self.process_csv, file_fun)

        # returnarray = []

        if partial_function:
            # print('multithread_csv_partial_function2a')
            file_fun.set_start_rows_of_csv()
            # print(
            #     f'multithread_csv_partial_function2b: {file_fun.csv_rowstart_array}')
            # print(f'partial_function1 workers: {file_fun.workers}')
            with ThreadPoolExecutor(max_workers=5) as executor:
                # print('ThreadPoolExecutor1')
                # returnarray.append(executor.map(partial_function, file_fun.csv_rowstart_array))
                futures = [executor.submit(self.process_csv, row_start, file_fun)
                           for row_start in file_fun.csv_rowstart_array]
                # process each result as it is available
                for future in as_completed(futures):
                    # get the downloaded url data
                    df_chunk = future.result()

        self.process_post_insert(file_fun)

        # print(f'returnarray: {returnarray}')

    def process_csv(self, row_start, file_fun):
        # print(f'process_csv row_start: {row_start}')
        # print(f'process_csv file_fun.get_file_rows: {file_fun.get_file_rows}')
        # print(f'process_csv file_fun.rows_to_get: {file_fun.rows_to_get}')
        # print(f'process_csv file_fun.names: {file_fun.names}')
        # print(f'process_csv file_fun.filepath: {file_fun.filepath}')

        # sql_fun = Sql_class()

        df = file_fun.get_file_rows(
            row_start, file_fun.rows_to_get, file_fun.names, file_fun.filepath)

        # print(f'process_csv1 df: {df}')
        self.add_extra_to_row(df)
        # print(f'process_csv2 df: {df}')

        bulk_insert_no_context(Kaggle_D1_Fraud_Data, df)

        # features_df = self.add_extracted_features(df)
        # # print(f'features_df: {features_df}')
        # sql_fun.bulk_insert(Kaggle_D1_meta, features_df)

        return df

    def add_extra_to_row(self, df):
        # print('add_extracted_features')
        # print(f'add_extracted_features df: {df}')
        to_insert = []
        for index, row in df.iterrows():
            # print(f'index: {index}, row: {row}')
            df.loc[index, 'device_fingerprint'] = self.create_device_fingerprint(
                row)
            df.loc[index, 'purchase_fingerprint'] = self.create_purchase_fingerprint(
                row)
            df.loc[index, 'user_fingerprint'] = self.create_user_fingerprint(
                row)
        # to_insert.append(self.create_signup_purchase_diff_sec(index, row))
        # self.insert_ip_country_from_ip_address(df)
        # print(f'to_insert: {to_insert_df}')

    def create_device_fingerprint(self, row):
        # print('create_device_fingerprint')
        # print(f'create_device_fingerprint row: {row}')
        str2hash = row['device_id'] + row['browser']
        # print(f'create_device_fingerprint str2hash: {str2hash}')
        fingerprint = hashlib.md5(str2hash.encode())
        fingerprint = fingerprint.hexdigest()
        # print(f'create_device_fingerprint fingerprint: {fingerprint}')
        return fingerprint

    def create_purchase_fingerprint(self, row):
        # print('create_purchase_fingerprint')
        str2hash = str(row['purchase_value']) + str(row['source'])
        fingerprint = hashlib.md5(str2hash.encode())
        fingerprint = fingerprint.hexdigest()
        return fingerprint

    def create_user_fingerprint(self, row):
        # print('create_purchase_fingerprint')
        str2hash = str(row['sex']) + str(row['age'])
        fingerprint = hashlib.md5(str2hash.encode())
        fingerprint = fingerprint.hexdigest()
        return fingerprint

    # def insert_ip_country_from_ip_address(self, df):
    #     # print('create_purchase_fingerprint')
    #     ip_address_list = df["ip_address"]

    # def add_extracted_features(self, df):
    #     # print('add_extracted_features')
    #     # print(f'add_extracted_features df: {df}')
    #     to_insert = []
    #     for index, row in df.iterrows():
    #         pass
    #         # print(f'index: {index}, row: {row}')
    #         # to_insert.append(self.create_device_fingerprint(index, row))
    #         # to_insert.append(self.create_purchase_fingerprint(index, row))
    #         # to_insert.append(self.create_signup_purchase_diff_sec(index, row))
    #     to_insert_df = pd.DataFrame(to_insert)
    #     # print(f'to_insert: {to_insert_df}')
    #     return to_insert_df

    def process_post_insert(self, file_fun):
        print('process_post_insert')

        executors_list = []

        with ThreadPoolExecutor(max_workers=5) as executor:
            executors_list.append(executor.submit(
                self.insert_signup_purchase_diff_sec))
            executors_list.append(executor.submit(
                self.insert_ip_address_history))
            executors_list.append(executor.submit(
                self.insert_ip_address_velocity))
            executors_list.append(executor.submit(
                self.insert_device_fingerprint_velocity))
            executors_list.append(executor.submit(
                self.insert_purchase_fingerprint_velocity))
            executors_list.append(executor.submit(
                self.insert_user_fingerprint_velocity))

        for x in executors_list:
            # print('executors_list result1')
            x.result()
            # print('executors_list result2')
            # print(x.result())

        # sql_fun = Sql_class()

        # df = file_fun.get_file_rows(
        #     row_start, file_fun.rows_to_get, file_fun.names, file_fun.filepath)

        # print(f'process_post_insert df: {df}')
        # print(f'df["id"]: {df["id"]}')
        # id_list = df["id"]

        # self.get_ip_address_hist_from_id(id_list)

    @timer_func
    def insert_signup_purchase_diff_sec(self):
        print('insert_signup_purchase_diff_sec1')
        # sql_fun = Sql_class()

        sql_raw = '''
            INSERT INTO fraud_data_extract.kaggle_d1_meta
            SELECT id, "signup_purchase_diff_sec" AS name,
            TIMESTAMPDIFF(SECOND, signup_time, purchase_time) AS value, NOW() AS created_at
            FROM fraud_data_extract.kaggle_d1_fraud_data
            '''
        raw_sql_execute_no_context(sql_raw, returnValue=False)
        print('insert_signup_purchase_diff_sec2')

    @timer_func
    def insert_ip_address_history(self):
        print('insert_ip_address_history1')
        # sql_fun = Sql_class()

        sql_raw = '''
            INSERT INTO fraud_data_extract.kaggle_d1_meta
            ((SELECT fd.id, 'ip_history_total' AS name,
            (SELECT COUNT(id) FROM fraud_data_extract.kaggle_d1_fraud_data fd_ip WHERE fd_ip.ip_address = fd.ip_address AND fd_ip.purchase_time < fd.purchase_time) AS value,
            now() AS created_at FROM fraud_data_extract.kaggle_d1_fraud_data fd)
            UNION ALL
            (SELECT fd.id, 'ip_history_fraudulent' AS name,
            (SELECT COUNT(id) FROM fraud_data_extract.kaggle_d1_fraud_data fd_ip WHERE fd_ip.ip_address = fd.ip_address AND fd_ip.purchase_time < fd.purchase_time AND fd_ip.is_fraud = 1) AS value,
            now() AS created_at FROM fraud_data_extract.kaggle_d1_fraud_data fd))
            '''
        raw_sql_execute_no_context(sql_raw, returnValue=False)
        print('insert_ip_address_history2')

    @timer_func
    def insert_ip_address_velocity(self):
        print('insert_ip_address_velocity1')
        # sql_fun = Sql_class()

        sql_raw = '''
            INSERT INTO fraud_data_extract.kaggle_d1_meta
            (SELECT fd.id, 'ip_address_velocity' AS name,
            (SELECT COUNT(id) FROM fraud_data_extract.kaggle_d1_fraud_data fd_ip
            WHERE fd_ip.ip_address = fd.ip_address AND fd_ip.purchase_time BETWEEN DATE_SUB(fd.purchase_time, INTERVAL 24 HOUR) AND fd.purchase_time) AS value,
            NOW() AS created_at FROM fraud_data_extract.kaggle_d1_fraud_data fd)
            '''
        raw_sql_execute_no_context(sql_raw, returnValue=False)
        print('insert_ip_address_velocity2')

    @timer_func
    def insert_device_fingerprint_velocity(self):
        print('insert_device_fingerprint_velocity1')
        # sql_fun = Sql_class()

        sql_raw = '''
            INSERT INTO fraud_data_extract.kaggle_d1_meta
            (SELECT fd.id, "device_fingerprint_velocity" AS name,
            (SELECT COUNT(fd_df.device_id) FROM fraud_data_extract.kaggle_d1_fraud_data fd_df
            WHERE fd_df.device_fingerprint = fd.device_fingerprint AND fd_df.purchase_time BETWEEN DATE_SUB(fd.purchase_time, INTERVAL 24 HOUR) AND fd.purchase_time) AS value,
            NOW() AS created_at FROM fraud_data_extract.kaggle_d1_fraud_data fd)
            '''
        raw_sql_execute_no_context(sql_raw, returnValue=False)
        print('insert_device_fingerprint_velocity2')

    @timer_func
    def insert_purchase_fingerprint_velocity(self):
        print('insert_purchase_fingerprint_velocity1')
        # sql_fun = Sql_class()

        sql_raw = '''
            INSERT INTO fraud_data_extract.kaggle_d1_meta
            (SELECT fd.id, "purchase_fingerprint_velocity" AS name,
            (SELECT COUNT(fd_df.purchase_fingerprint) FROM fraud_data_extract.kaggle_d1_fraud_data fd_df
            WHERE fd_df.purchase_time BETWEEN DATE_SUB(fd.purchase_time, INTERVAL 24 HOUR) AND fd.purchase_time AND fd_df.purchase_fingerprint = fd.purchase_fingerprint) AS value,
            NOW() AS created_at FROM fraud_data_extract.kaggle_d1_fraud_data fd)
            '''
        raw_sql_execute_no_context(sql_raw, returnValue=False)
        print('insert_purchase_fingerprint_velocity2')

    @timer_func
    def insert_user_fingerprint_velocity(self):
        print('insert_user_fingerprint_velocity1')
        # sql_fun = Sql_class()

        sql_raw = '''
            INSERT INTO fraud_data_extract.kaggle_d1_meta
            (SELECT fd.id, "user_fingerprint_velocity" AS name,
            (SELECT COUNT(fd_df.user_fingerprint) FROM fraud_data_extract.kaggle_d1_fraud_data fd_df
            WHERE fd_df.purchase_time BETWEEN DATE_SUB(fd.purchase_time, INTERVAL 24 HOUR) AND fd.purchase_time AND fd_df.user_fingerprint = fd.user_fingerprint) AS value,
            NOW() AS created_at FROM fraud_data_extract.kaggle_d1_fraud_data fd)
            '''
        raw_sql_execute_no_context(sql_raw, returnValue=False)
        print('insert_user_fingerprint_velocity2')

# Not to be used at the moment. Dataset was to large and I don't want to pay for storage
# class Kaggle_D2_OnlineFraud_Seeder(Seeder, File_class, Sql_class):
#     def __init__(self, db=None, *args, **kwargs):
#         Seeder.__init__(self, db=db)
#         File_class.__init__(self, *args, **kwargs)
#         Sql_class.__init__(self)
#         self.priority = 1

#     @timer_func
#     def run(self):
#         # self.rows_to_get = 2000
#         # self.workers = 5
#         print(f'rows_to_get: {self.rows_to_get}, workers: {self.workers}')
#         self.names = ['step', 'type', 'amount', 'nameOrig', 'oldbalanceOrg', 'newbalanceOrig',
#                       'nameDest', 'oldbalanceDest', 'newbalanceDest', 'isFraud', 'isFlaggedFraud']
#         self.filepath = csv_loc + 'online_payment_fraud_detection/onlinefraud.csv'

#         partial_function = partial(self.process_csv)

#         returnarray = self.multithread_csv_partial_function(partial_function)

#         # print(f'returnarray: {returnarray}')

#     def process_csv(self, row_start):
#         df = self.get_file_rows(
#             row_start, self.rows_to_get, self.names, self.filepath)

#         self.bulk_insert(Kaggle_D2_OnlineFraud, df)

#         return df
