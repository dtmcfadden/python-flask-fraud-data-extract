from extensions.database import db
# from classes.sql_class import Sql_class
from classes.sql_context_class import Sql_context_class


class Fraud_data_class:
    def __init__(self, user_id):
        self.user_id = user_id

    def get_order_data(self):
        # print(f'get_order_data self.user_id: {str(self.user_id)}')
        sql_fun = Sql_context_class()

        sql_raw = '''
			SELECT fd.user_id, fd.signup_time, fd.purchase_time, fd.device_id, fd.ip_address
			, (SELECT itc.country FROM fraud_data_extract.kaggle_d1_ipaddress_to_country itc WHERE fd.ip_address BETWEEN itc.lb_ip_address AND itc.ub_ip_address) AS ip_country
			, (SELECT m.value FROM fraud_data_extract.kaggle_d1_meta m WHERE m.user_id = fd.user_id AND m.name = "device_fingerprint_velocity") AS device_fingerprint_velocity
			, (SELECT m.value FROM fraud_data_extract.kaggle_d1_meta m WHERE m.user_id = fd.user_id AND m.name = "ip_address_velocity") AS ip_address_velocity
			, (SELECT m.value FROM fraud_data_extract.kaggle_d1_meta m WHERE m.user_id = fd.user_id AND m.name = "ip_history_fraudulent") AS ip_history_fraudulent
			, (SELECT m.value FROM fraud_data_extract.kaggle_d1_meta m WHERE m.user_id = fd.user_id AND m.name = "ip_history_total") AS ip_history_total
			, (SELECT m.value FROM fraud_data_extract.kaggle_d1_meta m WHERE m.user_id = fd.user_id AND m.name = "purchase_fingerprint_velocity") AS purchase_fingerprint_velocity
			, (SELECT m.value FROM fraud_data_extract.kaggle_d1_meta m WHERE m.user_id = fd.user_id AND m.name = "signup_purchase_diff_sec") AS signup_purchase_diff_sec
			FROM fraud_data_extract.kaggle_d1_fraud_data fd WHERE fd.user_id = :id
			'''
        results = sql_fun.raw_sql_execute(sql_raw, {'id': str(self.user_id)})
        return results
