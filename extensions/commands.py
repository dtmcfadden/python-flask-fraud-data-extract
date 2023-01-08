import click
from .database import db
from models.model import Kaggle_D1_Fraud_Data, Kaggle_D1_IpAddress_To_Country, Kaggle_D1_meta
# Kaggle_D2_OnlineFraud,


def create_db():
    """Creates database"""
    db.create_all()


def drop_db():
    """Drop / Clean database - DANGER ACTION"""
    db.drop_all()


def create_model_table():
    """Create table model in the database"""
    Kaggle_D1_Fraud_Data.__table__.create(db.engine)
    Kaggle_D1_IpAddress_To_Country.__table__.create(db.engine)
    Kaggle_D1_meta.__table__.create(db.engine)
    # Kaggle_D2_OnlineFraud.__table__.create(db.engine)


def init_app(app):
    # add multiple commands in a bulk
    for command in [create_db, drop_db, create_model_table]:
        app.cli.add_command(app.cli.command()(command))
