import datetime

import jwt
import requests
from django.contrib.auth.models import User
from django.http import HttpResponse

from cocognite.settings import ZOOM_API_KEY_JWT, ZOOM_API_SECRET_JWT


# COMPLETE AND WORKING
def get_jwt():
    payload = {
        'iss': ZOOM_API_KEY_JWT,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30)
    }
    token = jwt.encode(payload, ZOOM_API_SECRET_JWT).decode('utf-8')
    return token


# NOT WORKING
def o_auth_authorize():
    """
    https://zoom.us/oauth/authorize?response_type=code&client_id=7lstjK9NTyett_oeXtFiEQ&redirect_uri=https://yourapp.com
    help_page: https://marketplace.zoom.us/docs/guides/auth/oauth
    """
    url = 'https://zoom.us/oauth/authorize'
    headers = {
        'response_type': 'json',
        'client_id': '9718hiVcReaufC53hmezMg',
        'redirect_uri': 'https://marketplace.zoom.us/docs/oauth/callback/success',
    }
    response = requests.get(url, headers=headers)
    return response


# NOT WORKING
def o_auth_access_token():
    """
    https://zoom.us/oauth/token?grant_type=authorization_code&code=FROM_ABOVE_API&redirect_uri=REDIRECT_URL
    help: https://marketplace.zoom.us/docs/guides/auth/oauth
    """
    url = 'https://zoom.us/oauth/token'
    headers = {
        'response_type': 'code',
        'client_id': 'grjHMFaBR0aiGkHK9yCOZA',
        'redirect_uri': '',
    }
    response = requests.get(url, headers=headers)
    return response


def zoom_create_meeting(name, start_time, host):
    bearer_token = get_jwt()
    url = f"https://api.zoom.us/v2/users/{host}/meetings"

    payload = {
        "duration": 60,
        "host_id": host,
        "settings": {
            "alternative_hosts": "",
            "approval_type": 2,
            "audio": "both",
            "auto_recording": "local",
            "close_registration": False,
            "cn_meeting": False,
            "enforce_login": False,
            "enforce_login_domains": "",
            "global_dial_in_countries": [
            ],
            "global_dial_in_numbers": [
            ],
            "host_video": False,
            "in_meeting": False,
            "join_before_host": True,
            "mute_upon_entry": False,
            "participant_video": False,
            "registrants_confirmation_email": True,
            "use_pmi": False,
            "waiting_room": False,
            "watermark": False,
            "registrants_email_notification": True
        },
        "start_time": start_time,  # FORMAT 2019-09-05T16:54:14Z
        "status": "waiting",
        "timezone": "Asia/Calcutta",
        "topic": name,
        "type": 2,  # MEANS _ schedule meeting.
    }

    headers = {
        'content-type': "application/json",
        'authorization': f"Bearer {bearer_token}"
    }

    response = requests.post(url=url, json=payload, headers=headers)
    print(response.text)
    return response


def zoom_delete_meeting(meeting_id):
    bearer_token = get_jwt()
    url = f"https://api.zoom.us/v2/meetings/{meeting_id}"

    headers = {
        'authorization': f"Bearer {bearer_token}"
    }
    response = requests.delete(url=url, headers=headers)
    return response.status_code


def zoom_check_user(user='cocognito2020@gmail.com'):
    bearer_token = get_jwt()
    url = f"https://api.zoom.us/v2/users/{user}"
    headers = {
        'authorization': f"Bearer {bearer_token}"
    }
    response = requests.get(url, headers=headers)
    print(response.text)
    return response


def create_zoom_user(user: User):
    bearer_token = get_jwt()
    url = 'https://api.zoom.us/v2/users'
    headers = {
        'content-type': 'application/json',
        'authorization': f"Bearer {bearer_token}"
    }
    json = {
        'action': 'custCreate',
        'user_info': {
            'email': user.email,
            'type': 1,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
    }
    response = requests.post(url, headers=headers, json=json)
    print(response.text)
    return response.status_code == 201


def zoom(request):
    return HttpResponse()
