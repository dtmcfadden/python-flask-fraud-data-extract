from flask import Blueprint
import pandas as pd
from classes.fraud_data_class import Fraud_data_class

fraud = Blueprint('fraud', __name__)


@fraud.route("/user_id/<user_id>")
def get_by_user_id(user_id):
    # print(f'get_by_user_id user_id: {user_id}')
    fd_class = Fraud_data_class(user_id)

    results = fd_class.get_order_data()
    df = pd.DataFrame(results)

    return df.to_json()
