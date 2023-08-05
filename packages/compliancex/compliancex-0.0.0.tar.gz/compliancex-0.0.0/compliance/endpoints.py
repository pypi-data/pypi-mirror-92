import requests

from compliance.Constant import *
from compliance.bcolor import *


def health_check():
    try:
        res = requests.get(COMPLIANCEX_URL)
        if res.status_code == 200:
            date_time_str = res.text.replace('"', '')
            print(f"{bcolors.OKGREEN}HealthCheck status is passed.{date_time_str} {bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL} Unhealthy Service{bcolors.ENDC}")

    except Exception as err:
        print(f"{bcolors.FAIL} Unhealthy Service {bcolors.ENDC}")
