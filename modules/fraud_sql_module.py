from extensions.database import db
from modules.sql_context_module import raw_sql_execute_context
from models.model import User_D1_Is_Fraud

transaction_cutoff = 1000


def get_random_order_for_play(user_id):
    # print('get_random_order_for_play')

    sql_params = {'cutoff': transaction_cutoff}

    if user_id == None:
        sqk_raw = '''
            SELECT r.id FROM (SELECT fd.id, uds.is_fraud
            FROM fraud_data_extract.kaggle_d1_fraud_data fd
            JOIN (SELECT CASE WHEN FLOOR(RAND()*10) > 5 THEN false ELSE true END AS is_fraud) r
            ON r.is_fraud = fd.is_fraud
            LEFT OUTER JOIN fraud_data_extract.user_d1_is_fraud uds 
            ON uds.id = fd.id AND uds.user_id = :user_id) r
            WHERE r.is_fraud IS NULL AND r.id >= :cutoff ORDER BY RAND() LIMIT 1
            '''
        sql_params['user_id'] = user_id
    else:
        sql_raw = '''
            SELECT fd.id FROM fraud_data_extract.kaggle_d1_fraud_data fd
            JOIN (SELECT CASE WHEN FLOOR(RAND()*10) > 5 THEN false ELSE true END AS is_fraud) r ON r.is_fraud = fd.is_fraud
            WHERE fd.id >= :cutoff ORDER BY RAND() LIMIT 1
            '''

    results = raw_sql_execute_context(sql_raw, sql_params)
    # print(results)
    return_results = []
    # print(f'length: {len(results)}')
    if len(results) == 1:
        # print('In len results')
        # print(results.iloc[0].to_dict())
        return_results = get_order_data_by_params(results.iloc[0].to_dict())

    # print('get_random_order_for_play return_results')
    # print(return_results)
    return return_results


def get_order_data_by_params(sentParams):
    # print(f'get_order_data sentParams: {sentParams}')

    sql_raw = '''
		SELECT fd.id, fd.signup_time, fd.purchase_time, fd.purchase_value
            , fd.device_id, fd.ip_address, fd.source, fd.browser
            , fd.sex, fd.age, fd.device_fingerprint, fd.purchase_fingerprint, fd.user_fingerprint, fd.is_fraud
		, (SELECT itc.country FROM fraud_data_extract.kaggle_d1_ipaddress_to_country itc WHERE fd.ip_address BETWEEN itc.lb_ip_address AND itc.ub_ip_address) AS ip_country
		, (SELECT m.value FROM fraud_data_extract.kaggle_d1_meta m WHERE m.id = fd.id AND m.name = "device_fingerprint_velocity") AS device_fingerprint_velocity
		, (SELECT m.value FROM fraud_data_extract.kaggle_d1_meta m WHERE m.id = fd.id AND m.name = "ip_address_velocity") AS ip_address_velocity
		, (SELECT m.value FROM fraud_data_extract.kaggle_d1_meta m WHERE m.id = fd.id AND m.name = "ip_history_fraudulent") AS ip_history_fraudulent
		, (SELECT m.value FROM fraud_data_extract.kaggle_d1_meta m WHERE m.id = fd.id AND m.name = "ip_history_total") AS ip_history_total
		, (SELECT m.value FROM fraud_data_extract.kaggle_d1_meta m WHERE m.id = fd.id AND m.name = "purchase_fingerprint_velocity") AS purchase_fingerprint_velocity
		, (SELECT m.value FROM fraud_data_extract.kaggle_d1_meta m WHERE m.id = fd.id AND m.name = "user_fingerprint_velocity") AS user_fingerprint_velocity
		, (SELECT m.value FROM fraud_data_extract.kaggle_d1_meta m WHERE m.id = fd.id AND m.name = "signup_purchase_diff_sec") AS signup_purchase_diff_sec
		FROM fraud_data_extract.kaggle_d1_fraud_data fd WHERE
		'''

    is_valid = True
    sql_param = []
    allowed_params = {'id', 'device_id', 'ip_address', 'ip_country',
                      'device_fingerprint', 'purchase_fingerprint', 'user_fingerprint'}

    for key, value in sentParams.items():
        if key in allowed_params == False:
            is_valid = False
            break
        else:
            sql_param.append(f'fd.{key} = :{key}')

    # print(f'is_valid: {is_valid}')

    # print(f'sql_param: {sql_param}')

    if is_valid == True:
        sql_params_string = " AND ".join(sql_param)
        # print(f'params: {sql_params_string}')
        results = raw_sql_execute_context(
            f'{sql_raw} {sql_params_string}', sentParams)
        # print(results)

        return results
    else:
        return []


def get_user_action_stats(user_id):
    # print('get_user_action_stats')
    user_sql = ''

    sql_params = {'cutoff': transaction_cutoff}

    if user_id:
        user_sql = '''
            , CAST(IFNULL((SELECT SUM(uds.is_fraud) FROM fraud_data_extract.user_d1_is_fraud uds 
            WHERE uds.is_fraud = 1 AND uds.user_id = :user_id), 0) AS UNSIGNED) AS user_action_is_fraud_count
            , (SELECT COUNT(uds.user_id) FROM fraud_data_extract.user_d1_is_fraud uds 
            WHERE uds.user_id = :user_id) AS user_action_count
            , (SELECT COUNT(fd.id) AS correct_match FROM fraud_data_extract.user_d1_is_fraud uds
            JOIN fraud_data_extract.kaggle_d1_fraud_data fd ON fd.id = uds.id AND fd.is_fraud = uds.is_fraud 
            WHERE uds.user_id = :user_id) AS user_correct_match
            '''
        sql_params['user_id'] = user_id

    sql_raw = f'''
		SELECT CAST(SUM(fd.is_fraud) AS UNSIGNED) AS trans_is_fraud_count
        , COUNT(fd.id) AS trans_total_count
        {user_sql}
        FROM fraud_data_extract.kaggle_d1_fraud_data fd
		WHERE fd.id >= :cutoff
		'''

    # print(f'sql_raw: {sql_raw}')
    # print(f'sql_params: {sql_params}')
    results = raw_sql_execute_context(sql_raw, sql_params)
    # print(results)

    return results


def set_user_action(user_id, id, is_fraud):
    # print('set_user_action')

    sql_params = {'user_id': user_id, 'id': id, 'is_fraud': is_fraud}

    sql_raw = '''
		INSERT INTO fraud_data_extract.user_d1_is_fraud (user_id, id, is_fraud) 
        VALUES (:user_id,:id,:is_fraud) ON DUPLICATE KEY UPDATE is_fraud=:is_fraud
		'''

    raw_sql_execute_context(sql_raw, sql_params, False)


def get_user_action(user_id, id):
    # print('get_user_action')

    sql_params = {'user_id': user_id, 'id': id}

    sql_raw = '''
		SELECT is_fraud FROM fraud_data_extract.user_d1_is_fraud
        WHERE user_id = :user_id AND id = :id
		'''

    results = raw_sql_execute_context(sql_raw, sql_params)

    return results
