from extensions.database import db
# from classes.sql_class import Sql_class
from classes.sql_context_class import Sql_context_class


class Fraud_data_class:
    def __init__(self, id):
        self.id = id

    def get_order_data(self):
        # print(f'get_order_data self.id: {str(self.id)}')
        sql_fun = Sql_context_class()

        sql_raw = '''
			SELECT fd.id, fd.signup_time, fd.purchase_time, fd.purchase_value
            , fd.device_id, fd.ip_address, fd.source, fd.browser
            , fd.sex, fd.age, fd.device_fingerprint, fd.purchase_fingerprint, fd.is_fraud
			, (SELECT itc.country FROM fraud_data_extract.kaggle_d1_ipaddress_to_country itc WHERE fd.ip_address BETWEEN itc.lb_ip_address AND itc.ub_ip_address) AS ip_country
			, (SELECT m.value FROM fraud_data_extract.kaggle_d1_meta m WHERE m.id = fd.id AND m.name = "device_fingerprint_velocity") AS device_fingerprint_velocity
			, (SELECT m.value FROM fraud_data_extract.kaggle_d1_meta m WHERE m.id = fd.id AND m.name = "ip_address_velocity") AS ip_address_velocity
			, (SELECT m.value FROM fraud_data_extract.kaggle_d1_meta m WHERE m.id = fd.id AND m.name = "ip_history_fraudulent") AS ip_history_fraudulent
			, (SELECT m.value FROM fraud_data_extract.kaggle_d1_meta m WHERE m.id = fd.id AND m.name = "ip_history_total") AS ip_history_total
			, (SELECT m.value FROM fraud_data_extract.kaggle_d1_meta m WHERE m.id = fd.id AND m.name = "purchase_fingerprint_velocity") AS purchase_fingerprint_velocity
			, (SELECT m.value FROM fraud_data_extract.kaggle_d1_meta m WHERE m.id = fd.id AND m.name = "signup_purchase_diff_sec") AS signup_purchase_diff_sec
			FROM fraud_data_extract.kaggle_d1_fraud_data fd WHERE fd.id = :id
			'''
        results = sql_fun.raw_sql_execute(sql_raw, {'id': str(self.id)})
        return results

        # https://www.digitalocean.com/community/tutorials/how-to-query-tables-and-paginate-data-in-flask-sqlalchemy
        # 	names = ['Mary', 'Alex', 'Emily']
        # employees = Employee.query.filter(Employee.firstname.in_(names)).all()
        # 	print(employees)
