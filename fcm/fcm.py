import json
import time
import requests
import os.path
from notice.notice import *

noticeFile = 'latestNotice.json'
eventFile = 'latestEvent.json'
serverToken = os.environ.get('FCM_SERVER_TOKEN', '')
deviceToken = os.environ.get('FCM_DEVICE_TOKEN', '')
topic = os.environ.get('FCM_TOPIC', '')

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'key=' + serverToken,
}


def sendPushNotification(nType, data):
    imageUrl = data['data'][0]['details']['images']

    notification = {
        'title': data['data'][0]['title'],
        'body': data['data'][0]['published_on'],
    } if not imageUrl else {
        'title': data['data'][0]['title'],
        'body': data['data'][0]['published_on'],
        'image': imageUrl
    }

    body = {
        'notification': notification,
        'to': deviceToken, # topic
        'priority': 'high',
        'data': data['data'][0]
    }
    response = requests.post("https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(body))

    with open(noticeFile if nType == 'notice' else eventFile, 'w+') as f:
        f.write(json.dumps(data))

    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
    print(response.status_code)
    print(response.json())


def localData(objData, filename):
    file_exists = os.path.exists(filename)
    if file_exists:
        with open(filename, 'r') as f:
            data = json.loads(f.read())
    else:
        data = {}
    return True if objData != data else False


def prepareData():
    noticeData = getAllNE(dType='notice', page=0, limit=1)

    if localData(objData=noticeData, filename=noticeFile):
        sendPushNotification(nType='notice', data=noticeData)
    else:
        print("No New Notification")

    eventData = getAllNE(dType='event', page=0, limit=1)
    if localData(objData=eventData, filename=eventFile):
        sendPushNotification(nType='event', data=eventData)
    else:
        print("No New Event")

