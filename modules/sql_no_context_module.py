from extensions.database import db
from sqlalchemy import text
import pandas as pd
from app import create_app


def bulk_insert_no_context(db_model, df_obj):
    """
        db_passed = passed db
        db_model = sqlalchemy model
        df_obj = pandas dataframe
    """
    to_insert = df_obj.to_dict('records')
    try:
        app = create_app()
        with app.app_context():
            db.create_all()
            model = db.insert(db_model)
            # print(f'type(model): {type(model)}')
            # results = db.session.execute(model, to_insert)
            db.session.execute(model, to_insert)
            # db.session.commit()
            # print(f'results: {results}')
    except Exception as error:
        print(f'bulk_insert_no_context error: {error}')
        print(f'bulk_insert_no_context to_insert: {to_insert}')

    return 'Done'


def raw_sql_execute_no_context(raw_sql, params={}, returnValue=True):
    # print(f'raw_sql_execute params: {params}')
    try:
        app = create_app()
        results = []
        with app.app_context():
            db.create_all()
            # print(f'raw_sql_execute raw_sql: {raw_sql}')
            text_sql = text(raw_sql)
            # print(f'raw_sql_execute text_sql: {text_sql}')
            if returnValue == True:
                results = db.engine.execute(text_sql, params)
            else:
                db.engine.execute(text_sql, params)
            # print(f'raw_sql_execute results: {results}')
            # print(f'raw_sql_execute results', str(results), results == None, type(results))
        df = pd.DataFrame(results)
        # print(f'raw_sql_execute df: {df}')
        return df
    except Exception as error:
        print(f'raw_sql_execute_no_context error: {error}')
