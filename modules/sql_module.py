from extensions.database import db
from app import create_app


def bulk_insert_no_context(db_model, to_insert):
    print('create_app()1')
    app = create_app()
    # app = current_app()
    # print('create_app()2')
    # app = app.create_app()
    print('create_app()3')
    with app.app_context():
        # with current_app.app_context():
        print('db.create_all()')
        db.create_all()
        model = db.insert(db_model)
        # print(f'type(model): {type(model)}')
        # results = db.session.execute(model, to_insert)
        db.session.execute(model, to_insert)
        # db.session.commit()


def raw_sql_execute_no_context(raw_sql, params):
    app = create_app()
    # app = app.create_app()
    with app.app_context():
        # with current_app.app_context():
        db.create_all()
        results = db.engine.execute(raw_sql, params)
        return results
