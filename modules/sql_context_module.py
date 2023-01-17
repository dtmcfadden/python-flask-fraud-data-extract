from extensions.database import db
from sqlalchemy import text
import pandas as pd


def query_run_context(query_obj):
    results = None
    try:
        # print(f'has_app_context(): ', has_app_context())
        results = db.execute(query_obj)
        # print(f'results: {results}')
    except Exception as error:
        print(f'error: {error}')

    return results


def bulk_insert_context(db_model, df_obj):
    """
            db_passed = passed db
            db_model = sqlalchemy model
            df_obj = pandas dataframe
    """

    to_insert = df_obj.to_dict('records')

    model = db.insert(db_model)

    try:
        # print(f'has_app_context(): ', has_app_context())
        results = db.session.execute(model, to_insert)
        # print(f'results: {results}')
    except Exception as error:
        print(f'error: {error}')

    return 'Done'


def raw_sql_execute_context(raw_sql, params={}, has_return=True):
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
