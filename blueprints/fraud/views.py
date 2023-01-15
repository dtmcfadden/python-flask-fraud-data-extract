from flask import Blueprint, request
import pandas as pd
from classes.fraud_data_class import Fraud_data_class
from modules.fraud_sql_module import get_order_data_by_params, get_random_order_for_play
# from modules.convert_module import convert_tuple_to_dict

fraud = Blueprint('fraud', __name__)


@fraud.route("/")
def fraud_data():
    print('fraud_data')
    args_dict = request.args.to_dict()
    print(args_dict)
    results = get_order_data_by_params(args_dict)
    # args_dict = convert_tuple_to_dict(request.args)
    # print('args_dict')
    # print(args_dict)
    # print(f'results.to_json(orient="records"): {results.to_json(orient="records")}')
    # print(f'request.form: {request.form["id"]}')

    return results.to_json(orient="records")


@fraud.route("/play")
def fraud_play():
    # print('fraud_play')
    results = get_random_order_for_play()
    # print('fraud_play results')
    # print(results.to_json(orient="records"))
    # print(results.to_json())
    return results.to_json(orient="records")


@fraud.route("/id/<id>")
def get_by_id(id):
    # print(f'get_by_id id: {id}')
    fd_class = Fraud_data_class(id)

    results = fd_class.get_order_data()
    df = pd.DataFrame(results)

    return df.to_json(orient="records")
