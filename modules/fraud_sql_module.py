from classes.sql_context_class import Sql_context_class

transaction_cutoff = 1000


def get_random_order_for_play():
    print('get_random_order_for_play')
    sql_fun = Sql_context_class()

    sql_raw = '''
		SELECT fd.id FROM fraud_data_extract.kaggle_d1_fraud_data fd
		JOIN (SELECT CASE WHEN FLOOR(RAND()*10) > 5 THEN false ELSE true END AS is_fraud) r ON r.is_fraud = fd.is_fraud
		WHERE fd.id >= :cutoff ORDER BY RAND() LIMIT 1
		'''

    results = sql_fun.raw_sql_execute(sql_raw, {'cutoff': transaction_cutoff})
    print(results)
    return_results = []
    print(f'length: {len(results)}')
    if len(results) == 1:
        print('In len results')
        print(results.iloc[0].to_dict())
        return_results = get_order_data_by_params(results.iloc[0].to_dict())

    print('get_random_order_for_play return_results')
    print(return_results)
    return return_results


def get_order_data_by_params(sentParams):
    print(f'get_order_data sentParams: {sentParams}')
    sql_fun = Sql_context_class()

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

    print(f'is_valid: {is_valid}')

    print(f'sql_param: {sql_param}')

    if is_valid == True:
        sql_params_string = " AND ".join(sql_param)
        print(f'params: {sql_params_string}')
        results = sql_fun.raw_sql_execute(
            f'{sql_raw} {sql_params_string}', sentParams)
        print(results)

        return results
    else:
        return []
