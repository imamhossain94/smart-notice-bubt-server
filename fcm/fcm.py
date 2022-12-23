import json
import time
import os.path
from io import BytesIO
import requests
from PIL import Image
from notice.notice import getAllNE
from cloud_firestore.cloud_firestore import uploadFile, uploadDocuments, checkNotificationExistence, checkEventExistence

# Cloud messaging instance
serverToken = os.environ.get('FCM_SERVER_TOKEN', '')
deviceToken = os.environ.get('FCM_DEVICE_TOKEN', '')
topic = os.environ.get('FCM_TOPIC', '')

# Header for fcm
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'key=' + serverToken,
}


# Create push notification payload an send.
def sendPushNotification(data):
    # get image url
    imageUrl = data['data'][0]['details']['images']
    # checking if image url is not null
    if imageUrl:
        # Download image from url
        response = requests.get(imageUrl)
        img = Image.open(BytesIO(response.content))
        x, y = img.size
        y = int(y / int(str(x)[0]))
        x = int(x / int(str(x)[0]))
        # Resize image url to reduce image size under 1MB
        img = img.resize((x, y), Image.ANTIALIAS)
        # Save image as BytesIO
        img_str = BytesIO
        img.save(img_str, 'jpg')
        # Upload image into firebase storage and get image url
        imageUrl = uploadFile(buffer=img_str, data_type=data['type'])

    # if imageUrl is null then we will send title and body.
    notification = {
        'title': data['data'][0]['title'],
        'body': data['data'][0]['published_on'],
    } if not imageUrl else {
        'title': data['data'][0]['title'],
        'body': data['data'][0]['published_on'],
        'image': imageUrl  # imageUrl
    }

    body = {
        'notification': notification,
        'to': topic,  # topic deviceToken
        'priority': 'high',
        'data': data['data'][0]
    }

    # Sending notification
    requests.post("https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(body))

    # Uploading data in firebase storage
    uploadDocuments(data=data)


# Get scraped data and check if those data ware send
# as notification or not.
def prepareData():
    # get last notice scraped data
    noticeData = getAllNE(dType='notice', page=0, limit=5)
    # checking that data was send as notification or not
    for nd in noticeData:
        if not checkNotificationExistence(noticeData):
            sendPushNotification(data=noticeData)
        else:
            print("No New Notification")

    time.sleep(20)
    # get last event scraped data
    eventData = getAllNE(dType='event', page=0, limit=5)
    # checking that data was send as notification or not
    for ed in eventData:
        if not checkEventExistence(eventData):
            sendPushNotification(data=eventData)
        else:
            print("No New Event")
