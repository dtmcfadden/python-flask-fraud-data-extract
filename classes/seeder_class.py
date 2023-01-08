# from app import create_app
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
import concurrent.futures
from functools import partial
from extensions.database import db
from models.model import Kaggle_D1_IpAddress_To_Country
# from flask_seeder import Seeder, Faker, generator
from classes.file_class import File_class
from classes.sql_class import Sql_class
import pandas as pd
import pathlib

actual_dir = pathlib.Path().absolute()
print(f'actual_dir: {actual_dir}')
csv_loc = f'{actual_dir}/csv/'
print(f'csv_loc: {csv_loc}')


class Seeder_run(File_class, Sql_class):
    def __init__(self, names, filepath, priority=1, startrow=1, rows_to_get=10000, workers=5, csv_run=[]):
        self.names = names
        self.file = csv_loc + filepath
        self.priority = priority
        self.startrow = startrow
        self.rows_to_get = rows_to_get
        self.workers = workers
        self.csv_run = csv_run
