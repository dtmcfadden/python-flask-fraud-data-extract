from flask import Blueprint, request
import pandas as pd
from modules.fraud_sql_module import get_order_data_by_params, get_random_order_for_play, \
    get_user_action_stats, set_user_action, get_user_action
from modules.authorize_request import receive_authorized_get_request

fraud = Blueprint('fraud', __name__)


@fraud.route("/")
def fraud_data():
    print('fraud_data')
    args_dict = request.args.to_dict()
    # print(args_dict)
    results = get_order_data_by_params(args_dict)
    # args_dict = convert_tuple_to_dict(request.args)
    # print('args_dict')
    # print(args_dict)
    # print(f'results.to_json(orient="records"): {results.to_json(orient="records")}')
    # print(f'request.form: {request.form["id"]}')

    return results.to_json(orient="records")


@fraud.route("/play")
def fraud_play():
    print('fraud_play')
    results = get_random_order_for_play(None)
    # print('fraud_play results')
    # print(results.to_json(orient="records"))
    # print(results.to_json())
    return results.to_json(orient="records")


@fraud.route("/play/<user_id>")
def fraud_play_by_user_id(user_id):
    print(f'fraud_play_by_user_id user_id: {user_id}')

    auth_results = receive_authorized_get_request(request)
    print('auth_results', auth_results)

    results = get_random_order_for_play(user_id)
    # print('fraud_play results')
    # print(results.to_json(orient="records"))
    # print(results.to_json())
    return results.to_json(orient="records")


@fraud.route("/id/<id>")
def get_by_id(id):
    print(f'get_by_id id: {id}')
    # fd_class = Fraud_data_class(id)

    # results = fd_class.get_order_data()
    results = get_order_data_by_params({'id': id})
    df = pd.DataFrame(results)

    return df.to_json(orient="records")


@fraud.route("/transstats")
def get_trans_stats():
    print(f'get_trans_stats')

    auth_results = receive_authorized_get_request(request)
    print('get_trans_stats auth_results', auth_results)

    results = get_user_action_stats(None)
    # print(f'get_trans_stats')
    df = pd.DataFrame(results)
    # print(f'get_trans_stats df: {df}')

    return_dict = {}
    if len(df) == 1:
        return_dict = df.iloc[0].to_dict()

    return return_dict


@fraud.route("/userstats/<user_id>")
def get_user_stats_user_id(user_id):
    print('get_user_stats_user_id')
    auth_results = receive_authorized_get_request(request)
    print('get_user_stats_user_id auth_results', auth_results)
    # print(f'get_user_stats_user_id user_id: {user_id}')
    results = get_user_action_stats(user_id)
    # print(f'get_user_stats_user_id results: {results}')
    df = pd.DataFrame(results)
    # print(f'get_user_stats_user_id df: {df}')
    return_dict = {}
    if len(df) == 1:
        return_dict = df.iloc[0].to_dict()

    return return_dict
    # return df.to_json(orient="records")


@fraud.route("/user/action", methods=["POST"])
def post_user_action():
    print('post_user_action')
    return_dict = {}
    if request.method == 'POST':
        # print(request)
        # print(request.json)
        # print(request.form)
        # <user_id>/id/<id>/is_fraud/<is_fraud>
        data = request.json
        # print(data)
        # print(data['user_id'])

        set_user_action(data['user_id'], data['id'], data['is_fraud'])

        results = get_user_action(data['user_id'], data['id'])

        df = pd.DataFrame(results)
        # print(f'post_user_action df: {df}')
        if len(df) == 1:
            return_dict = df.iloc[0].to_dict()
        # user_id = request.form.get('user_id')
        # id = request.form.get('id')
        # is_fraud = request.form.get('is_fraud')

        # user_id = request.form['user_id']
        # id = request.form['id']
        # is_fraud = request.form['is_fraud']

        # print('user_id', user_id)
        # print('id', id)
        # print('is_fraud', is_fraud)
    return return_dict

    # results = get_user_action_stats(user_id)
    # # print(f'get_user_stats_user_id results: {results}')
    # df = pd.DataFrame(results)
    # print(f'get_user_stats_user_id df: {df}')
    # return_dict = {}
    # if len(df) == 1:
    #     return_dict = df.iloc[0].to_dict()

    # return return_dict
