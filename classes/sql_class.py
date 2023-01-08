from app import create_app
from extensions.database import db
# from extensions import database, commands


class Sql_class:
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    def __init__(self):
        super().__init__()

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
            app = create_app()
            with app.app_context():
                db.create_all()
                model = db.insert(db_model)
                # print(f'type(model): {type(model)}')
                # results = db.session.execute(model, to_insert)
                db.session.execute(model, to_insert)
                db.session.commit()
                # print(f'results: {results}')
        except Exception as error:
            print(f'error: {error}')

        # results = db.engine.execute(model, to_insert)
        # print('results')
        # print(results)
        # return results
        return 'Done'
