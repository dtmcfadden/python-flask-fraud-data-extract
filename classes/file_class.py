from functools import partial
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import csv


class File_class():
    def __init__(self, names=[], filepath='', startrow=1, rows_to_get=10000, csv_rowstart_array=[], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.names = names
        self.filepath = filepath
        self.startrow = startrow
        self.rows_to_get = rows_to_get
        self.csv_rowstart_array = csv_rowstart_array
        # if names is None:
        #     names = []
        # else:
        #     self.names = names

        # if csv_rowstart_array is None:
        #     csv_rowstart_array = []
        # else:
        #     self.csv_rowstart_array = csv_rowstart_array

    def read_csv_return_dataset(self, file_location, newline='', delimiter=',', quotechar='"'):
        with open(file_location, newline=newline) as csvfile:
            spamreader = csv.reader(
                csvfile, delimiter=delimiter, quotechar=quotechar)
            # for row in spamreader:
            #     print(', '.join(row))

    # def run_csv_thread(self, process_csv, *args, **kwargs):
    #     print('run_csv_thread1a')
    #     print(f'run_csv_thread1a args: {args}')
    #     print(f'run_csv_thread1a kwargs: {kwargs}')
    #     print(f'self.names: {self.names}')
    #     print(f'self.filepath: {self.filepath}')
    #     print(f'self.startrow: {self.startrow}')
    #     print(f'self.rows_to_get: {self.rows_to_get}')
    #     print(f'self.workers: {self.workers}')
    #     print(f'self.csv_rowstart_array: {self.csv_rowstart_array}')
    #     print('run_csv_thread1b')
    #     self.set_start_rows_of_csv()
    #     print('run_csv_thread2')

    #     returnarray = []
    #     print('run_csv_thread3')

    #     partial_function = partial(process_csv, *args, **kwargs)
    #     print('run_csv_thread4')

    #     if partial_function:
    #         print('partial_function1')
    #         with ThreadPoolExecutor(max_workers=self.workers) as executor:
    #             print('ThreadPoolExecutor1')
    #             returnarray.append(executor.map(
    #                 partial_function, self.csv_rowstart_array))
    #             print('ThreadPoolExecutor2')

    #     return returnarray

    # def run_csv_thread(self, process_csv):
    #     print('run_csv_thread1a')
    #     print(f'self.names: {self.names}')
    #     print(f'self.filepath: {self.filepath}')
    #     print(f'self.startrow: {self.startrow}')
    #     print(f'self.rows_to_get: {self.rows_to_get}')
    #     print(f'self.workers: {self.workers}')
    #     print(f'self.csv_rowstart_array: {self.csv_rowstart_array}')
    #     print('run_csv_thread1b')
    #     self.set_start_rows_of_csv()
    #     print('run_csv_thread2')

    #     returnarray = []
    #     print('run_csv_thread3')

    #     partial_function = partial(process_csv)
    #     print('run_csv_thread4')

    #     if partial_function:
    #         print('partial_function1')
    #         with ThreadPoolExecutor(max_workers=self.workers) as executor:
    #             print('ThreadPoolExecutor1')
    #             returnarray.append(executor.map(
    #                 partial_function, self.csv_rowstart_array))
    #             print('ThreadPoolExecutor2')

    #     return returnarray

    # def multithread_csv_partial_function(self, partial_function):
    #     print('multithread_csv_partial_function1')
    #     returnarray = []

    #     if partial_function:
    #         print('multithread_csv_partial_function2a')
    #         self.set_start_rows_of_csv()
    #         print(
    #             f'multithread_csv_partial_function2b: {self.csv_rowstart_array}')
    #         print(f'partial_function1 workers: {self.workers}')
    #         with ThreadPoolExecutor(max_workers=self.workers) as executor:
    #             # print('ThreadPoolExecutor1')
    #             returnarray.append(executor.map(
    #                 partial_function, self.csv_rowstart_array))
    #     return returnarray

    def set_start_rows_of_csv(self):
        # print('set_start_rows_of_csv1')
        row_count = self.get_file_row_count(self.filepath)
        # print('set_start_rows_of_csv2')
        # row_count = 1  # remove after testing
        # print(f'set_start_rows_of_csv row_count: {row_count}')
        # print(f'self.csv_rowstart_array: {self.csv_rowstart_array}')
        # print(
        #     f'type(self.csv_rowstart_array): {type(self.csv_rowstart_array)}')
        # print(
        #     f'set_start_rows_of_csv len(self.run): {len(self.csv_rowstart_array)}')
        while ((len(self.csv_rowstart_array) * self.rows_to_get) + self.startrow <= row_count):
            # print('set_start_rows_of_csv1')
            self.csv_rowstart_array.append(
                (len(self.csv_rowstart_array) * self.rows_to_get) + self.startrow)
            # print('set_start_rows_of_csv2')

    def get_file_row_count(self, filepath):
        row_count = 0
        with open(filepath) as f:
            row_count = sum(1 for line in f)
        return row_count

    def get_file_rows(self, row_start, rows_to_get, names, filepath):
        # print(f'get_file_rows row_start: {row_start}')
        # print(f'get_file_rows rows_to_get: {rows_to_get}')
        # print(f'get_file_rows names: {names}')
        # print(f'get_file_rows filepath: {filepath}')
        df = pd.read_csv(filepath, skiprows=row_start,
                         nrows=rows_to_get, names=names)
        # print(f'get_file_rows df: {df}')
        return df

    # def run_init(self):
    #     for i in range(self.workers):
    #         self.add_run()

    # def add_run(self):
    #     # print('add_run')
    #     # print(len(self.csv_run))
    #     if self.stop == False:
    #         # print('add_run self.run.add1')
    #         self.csv_run.add(((len(self.csv_run) + len(self.csv_running) +
    #                            len(self.csv_ran)) * self.rows_to_get) + self.startrow)
    #         # print(f'add_run self.run.add2 self.csv_run: {self.csv_run}')
