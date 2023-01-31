from extensions.database import db
from sqlalchemy import text
import pandas as pd


class Sql_context_class:
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    def __init__(self):
        super().__init__()

    def query_run(query_obj):
        results = None
        try:
            # print(f'has_app_context(): ', has_app_context())
            results = db.execute(query_obj)
            # print(f'results: {results}')
        except Exception as error:
            print(f'error: {error}')

        return results

    def bulk_insert(self, db_model, df_obj):
        """
            db_passed = passed db
            db_model = sqlalchemy model
            df_obj = pandas dataframe
        """
        # print('sql_class bulk_insert')
        # print('db')
        # print(type(db))
        # print('current_db')
        # print(type(current_db))
        to_insert = df_obj.to_dict('records')
        # print(f'to_insert: {to_insert}')
        # print('type(db.session)')
        # print(type(db.session))
        # print('type(current_db.session)')
        # print(type(current_db.session))
        # print('type(db.session.execute)')
        # print(type(db.session.execute))
        # print('type(current_db.session.execute)')
        # print(type(current_db.session.execute))
        try:
            # print(f'has_app_context(): ', has_app_context())
            results = db.session.execute(model, to_insert)
            # print(f'results: {results}')
        except Exception as error:
            print(f'error: {error}')

        return 'Done'

    def raw_sql_execute(self, raw_sql, params={}, has_return=True):
        # print(f'raw_sql_execute params: {params}')
        try:
            # print(f'raw_sql_execute raw_sql: {raw_sql}')
            text_sql = text(raw_sql)
            # print(f'raw_sql_execute text_sql: {text_sql}')
            if has_return == True:
                results = db.engine.execute(text_sql, params)
                # print(f'raw_sql_execute results: {results}')
                df = pd.DataFrame(results)
                # print(f'raw_sql_execute df: ', df)
                # print(f'raw_sql_execute has_return: ', has_return)
                return df
            else:
                db.engine.execute(text_sql, params)
        except Exception as error:
            print(f'error: {error}')
