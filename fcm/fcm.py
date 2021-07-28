import json
import time
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from bs4 import BeautifulSoup
from flask import Blueprint, request, jsonify
from requests import get

serverToken = ''
deviceToken = ''

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'key=' + serverToken,
}


def sendPush(time):
    body = {
        'notification': {'title': 'Sending push form python script',
                         'body': 'New Message' + time
                         },
        'to':
            deviceToken,
        'priority': 'high',
        #   'data': dataPayLoad,
    }
    response = requests.post("https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(body))
    print(response.status_code)

    print(response.json())


def print_date_time(lal):
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
    sendPush(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

