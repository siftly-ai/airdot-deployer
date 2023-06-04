from airdot.collection.collections import authentication
import requests
from datetime import datetime
from airdot import URL, VERIFY


def get_authentication_token(auth_: authentication):
    r = requests.get(f"{URL}get_auth_token", verify=VERIFY)

    if r.status_code == 200:
        auth_.refresh_token = r.content.decode()
        auth_.token_time = datetime.now()


def verify_user(auth_: authentication):
    json = {"auth_session_token": auth_.refresh_token}
    r = requests.post(f"{URL}check_authentication", verify=VERIFY, json=json)
    if r.status_code == 200:
        if r.content.decode() == "false":
            return False
        return True


def user_login(auth_: authentication):
    get_authentication_token(auth_=auth_)
    json = {"auth_session_token": auth_.refresh_token}
    r = requests.post(f"{URL}login", verify=VERIFY, json=json)
    if r.status_code == 200:
        return r.content.decode()
    else:
        return None


def get_user_function(auth_: authentication):
    json = {"auth_session_token": auth_.refresh_token}
    r = requests.post(f"{URL}get_my_functions", verify=VERIFY, json=json)
    if r.status_code == 200:
        return r.content.decode()
    else:
        return None


def get_function_status(payload: dict):
    r = requests.post(f"{URL}check_function_status", verify=VERIFY, json=payload)
    if r.status_code == 200:
        return r.content.decode()
    else:
        return None


def get_gcs_signed_token(auth_: authentication):
    json = {"auth_session_token": auth_.refresh_token}

    r = requests.post(f"{URL}get_gcs_token", verify=VERIFY, json=json)
    if r.status_code == 200:
        return r.content.decode()
    else:
        return None


def push_refreshed_objects(json_dict):
    r = requests.post(f"{URL}update_objects", verify=VERIFY, json=json_dict)
    if r.status_code == 200:
        return r.content.decode()
    else:
        return None
