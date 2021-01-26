import base64
import json

import requests
from django.http import HttpResponse


def get_access_token():
    url = 'https://zoom.us/oauth/token?grant_type=client_credentials'
    credentials = base64.b64encode('grjHMFaBR0aiGkHK9yCOZA:EMaxCD10j9jlUn0z6gn8lroTxrUuqItZ'.encode('ascii'))
    headers = {
        'content-type': "application/json",
        'authorization': f"Basic Z3JqSE1GYUJSMGFpR2tISzl5Q09aQTpFTWF4Q0QxMGo5amxVbjB6NmduOGxyb1R4clV1cUl0Wg=="
    }
    response = requests.post(url, headers=headers)
    return json.loads(response.text)


def create_meeting():
    # access = get_access_token()
    # bearer_token = access['access_token']
    url = "https://api.zoom.us/v2/users/donald.duck0762@gmail.com/meetings"

    payload = {
        "created_at": "2019-09-05T16:54:14Z",
        "duration": 60,
        "host_id": "donald.duck0762@gmail.com",
        "id": 11000000,
        "join_url": "https://zoom.us/j/11000000",
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
            "use_pmi": True,
            "waiting_room": False,
            "watermark": False,
            "registrants_email_notification": True
        },
        "start_time": "2019-08-30T22:00:00Z",
        "start_url": "https://zoom.us/s/1100000?iIifQ.wfY2ldlb82SWo3TsR77lBiJjR53TNeFUiKbLyCvZZjw",
        "status": "waiting",
        "timezone": "America/New_York",
        "topic": "API Test",
        "type": 2,
        "uuid": "ng1MzyWNQaObxcf3+Gfm6A=="
    }

    headers = {
        'content-type': "application/json",
        'authorization': "Bearer eyJhbGciOiJIUzUxMiIsInYiOiIyLjAiLCJraWQiOiI4ZDliNmZiMC1jYzMwLTQ3ODAtYjBjNS1lMWVjMDg3ZGQ3OGIifQ.eyJ2ZXIiOjcsImF1aWQiOiI5Y2Y1YjdmMzBlOWQxMzYwZjA1ZDk1OTQyNjA0MDc1YSIsImNvZGUiOiJaNHdTM2VsWHhkXzFyaFotZThyUzdpR2xnRjV1WFVreXciLCJpc3MiOiJ6bTpjaWQ6Z3JqSE1GYUJSMGFpR2tISzl5Q09aQSIsImdubyI6MCwidHlwZSI6MCwidGlkIjowLCJhdWQiOiJodHRwczovL29hdXRoLnpvb20udXMiLCJ1aWQiOiIxcmhaLWU4clM3aUdsZ0Y1dVhVa3l3IiwibmJmIjoxNjExNjg0ODA1LCJleHAiOjE2MTE2ODg0MDUsImlhdCI6MTYxMTY4NDgwNSwiYWlkIjoidzZ0OFdOOVRTRXlNSWJ0dFE0WDQwZyIsImp0aSI6ImUzNjdlZjY4LTBjNDAtNGY0MS04OWFkLWE2YmQxMDk3ZGNjMyJ9.Jii17dzrI-tkLIWwtFcOnDo7bKNzMow32gHpsTTJ4X34t3hI7pEDUn3z-Y5IpQ3fdu9mzW8XcpbWOQqmnGZzjw"
    }

    response = requests.post(url=url, json=payload, headers=headers)
    print(response.text)
    return response


def delete_meeting():
    url = "https://api.zoom.us/v2/meetings/78193237508"
    headers = {
        'authorization': 'Bearer eyJhbGciOiJIUzUxMiIsInYiOiIyLjAiLCJraWQiOiI4ZDliNmZiMC1jYzMwLTQ3ODAtYjBjNS1lMWVjMDg3ZGQ3OGIifQ.eyJ2ZXIiOjcsImF1aWQiOiI5Y2Y1YjdmMzBlOWQxMzYwZjA1ZDk1OTQyNjA0MDc1YSIsImNvZGUiOiJaNHdTM2VsWHhkXzFyaFotZThyUzdpR2xnRjV1WFVreXciLCJpc3MiOiJ6bTpjaWQ6Z3JqSE1GYUJSMGFpR2tISzl5Q09aQSIsImdubyI6MCwidHlwZSI6MCwidGlkIjowLCJhdWQiOiJodHRwczovL29hdXRoLnpvb20udXMiLCJ1aWQiOiIxcmhaLWU4clM3aUdsZ0Y1dVhVa3l3IiwibmJmIjoxNjExNjg0ODA1LCJleHAiOjE2MTE2ODg0MDUsImlhdCI6MTYxMTY4NDgwNSwiYWlkIjoidzZ0OFdOOVRTRXlNSWJ0dFE0WDQwZyIsImp0aSI6ImUzNjdlZjY4LTBjNDAtNGY0MS04OWFkLWE2YmQxMDk3ZGNjMyJ9.Jii17dzrI-tkLIWwtFcOnDo7bKNzMow32gHpsTTJ4X34t3hI7pEDUn3z-Y5IpQ3fdu9mzW8XcpbWOQqmnGZzjw'}
    response = requests.delete(url=url, headers=headers)
    print(response)


def zoom(request):
    return HttpResponse(create_meeting())
