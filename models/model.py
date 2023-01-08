from extensions.database import db


class Kaggle_D1_Fraud_Data(db.Model):
    __tablename__ = 'kaggle_d1_fraud_data'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    signup_time = db.Column(db.DateTime, index=True)
    purchase_time = db.Column(db.DateTime, index=True)
    purchase_value = db.Column(db.Float)
    device_id = db.Column(db.String(20), index=True)
    source = db.Column(db.String(6), index=True)
    browser = db.Column(db.String(10), index=True)
    sex = db.Column(db.String(1))
    age = db.Column(db.Integer, index=True)
    ip_address = db.Column(db.Float, index=True)
    device_fingerprint = db.Column(db.String(35), index=True)
    purchase_fingerprint = db.Column(db.String(35), index=True)
    is_fraud = db.Column(db.Boolean)

    kaggle_d1_meta = db.relationship(
        'Kaggle_D1_meta', backref='meta', cascade="all, delete-orphan")

    def __repr__(self):
        return f"Id: {self.id}, user_id: {self.user_id}, Signup Time {self.signup_time}"


class Kaggle_D1_IpAddress_To_Country(db.Model):
    __tablename__ = 'kaggle_d1_ipaddress_to_country'

    lb_ip_address = db.Column(db.BIGINT, primary_key=True, autoincrement=True)
    ub_ip_address = db.Column(db.BIGINT, primary_key=True, default=0)
    country = db.Column(db.String(50))

    def __repr__(self):
        return f"Id: {self.id}, lb_ip: {self.lower_bound_ip_address}, ub_ip: {self.lower_bound_ip_address}, coutnry{self.country}"


class Kaggle_D1_meta(db.Model):
    __tablename__ = 'kaggle_d1_meta'

    user_id = db.Column(db.Integer, db.ForeignKey(
        'kaggle_d1_fraud_data.user_id'), primary_key=True, autoincrement=True)
    name = db.Column(db.String(75), primary_key=True, default='0')
    value = db.Column(db.String(255), index=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"Id: {self.id}, Name: {self.name}, Value: {self.value}"


# class Kaggle_D2_OnlineFraud(db.Model):
#     __tablename__ = 'kaggle_d2_onlinefraud'

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     step = db.Column(db.Integer, index=True)
#     type = db.Column(db.String(50), index=True)
#     amount = db.Column(db.Float)
#     name_orig = db.Column(db.String(50), index=True)
#     oldbalance_org = db.Column(db.Float, index=True)
#     newbalance_org = db.Column(db.Float, index=True)
#     name_dest = db.Column(db.String(50), index=True)
#     oldbalance_dest = db.Column(db.Float, index=True)
#     newbalance_dest = db.Column(db.Float, index=True)
#     is_fraud = db.Column(db.Boolean, index=True)
#     is_flagged_fraud = db.Column(db.Boolean)

#     def __repr__(self):
#         return f"Id: {self.id}, Step: {self.step}, Type: {self.type}, Name Orig: {self.name_orig}"


# Fraud_Data
# "user_id","signup_time","purchase_time","purchase_value","device_id","source",
# "browser","sex","age","ip_address","class"

# IpAddress_to_Country
# "lower_bound_ip_address","upper_bound_ip_address","country"

# onlinefraud
# step,type,amount,nameOrig,oldbalanceOrg,newbalanceOrig,nameDest,oldbalanceDest,
# newbalanceDest,isFraud,isFlaggedFraud
