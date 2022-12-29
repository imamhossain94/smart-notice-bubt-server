import json
import time
import os.path
from io import BytesIO
import requests
from PIL import Image
from notice.notice import getAllNE
from cloud_firestore.cloud_firestore import uploadFile, uploadDocuments, checkNoticeExistence, checkEventExistence

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
    imageUrl = data['details']['images']
    # checking if image url is not null
    if imageUrl:
        # Download image from url
        response = requests.get(imageUrl)
        img = Image.open(BytesIO(response.content))
        x, y = img.size
        y = int(y / int(str(x)[0]))
        x = int(x / int(str(x)[0]))
        # Resize image url to reduce image size under 1MB
        image = img.resize((x, y), Image.ANTIALIAS)
        image = image.convert('RGB')
        # Save image as BytesIO
        output = BytesIO()

        image.save(output, format="JPEG", optimize=True)
        # Upload image into firebase storage and get image url
        imageUrl = uploadFile(buffer=output, data_type=data['type'])

    # if imageUrl is null then we will send title and body.
    notification = {
        'title': data['title'],
        'body': data['published_on'],
    } if not imageUrl else {
        'title': data['title'],
        'body': data['published_on'],
        'image': imageUrl  # imageUrl
    }

    body = {
        'notification': notification,
        'to': topic,  # topic deviceToken
        'priority': 'high',
        'data': data
    }
    print(imageUrl)

    # Sending notification
    requests.post("https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(body))

    # Uploading data in firebase storage
    uploadDocuments(data=data)


# Get scraped data and check if those data ware send
# as notification or not.
def prepareData():
    # get last notice scraped data
    noticeData = getAllNE(dType='notice', page=0, limit=3)
    # checking that data was send as notification or not
    if noticeData['status'] == 'success':
        for nd in noticeData['data']:
            if not checkNoticeExistence(nd):
                nd['type'] = 'notice'
                sendPushNotification(data=nd)
            else:
                print("No New Notice")
    else:
        print(noticeData['reason'])

    time.sleep(20)
    # get last event scraped data
    eventData = getAllNE(dType='event', page=0, limit=3)
    # checking that data was send as notification or not
    if eventData['status'] == 'success':
        for ed in eventData['data']:
            if not checkEventExistence(ed):
                ed['type'] = 'event'
                sendPushNotification(data=ed)
            else:
                print("No New Event")
    else:
        print(eventData['reason'])
