from flask import Blueprint
from classes.seeder_class import Kaggle_D1_IpAddress_To_Country_Seeder

seeder = Blueprint('seeder', __name__)


@seeder.route("/seeder")
def index():
    # Kaggle_D1_IpAddress_To_Country_Seeder.run()
    # return 'Done'
    seeder_d1_ip = Kaggle_D1_IpAddress_To_Country_Seeder()
    results = seeder_d1_ip.run()
    return results
