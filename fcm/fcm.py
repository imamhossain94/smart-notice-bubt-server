import json
import time
import os.path
from io import BytesIO
import requests
from PIL import Image
from notice.notice import getAllNE
from cloud_firestore.cloud_firestore import uploadFile, uploadDocuments

# Directory information
baseDirectory = 'resources'
noticeFile = baseDirectory + '/latestNotice.json'
eventFile = baseDirectory + '/latestEvent.json'
noticeImageFile = baseDirectory + '/noticePhoto.jpg'
eventImageFile = baseDirectory + '/eventPhoto.jpg'

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
        # Save image in file
        imageFileName = noticeImageFile if data['type'] == 'notice' else eventImageFile
        img.save(imageFileName)
        # Upload image into firebase storage and get image url
        imageUrl = uploadFile(filename=imageFileName)

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

    # Saving last send notification data
    dataFileName = noticeFile if data['type'] == 'notice' else eventFile
    with open(dataFileName, 'w+') as f:
        f.write(json.dumps(data))


# Checking directory are exists or not
# If exists read file inside of it and compare
# newly scraped data with file data
# If data are matched it return false otherwise return true
def localData(objData, filename):
    # Checking that the directory are exists or not
    dir_exists = os.path.exists(baseDirectory)
    file_exists = os.path.exists(filename)

    if not dir_exists:
        # Making directory
        os.makedirs(baseDirectory)
    if file_exists:
        with open(filename, 'r') as f:
            data = json.loads(f.read())
    else:
        data = {}
    return True if objData != data else False


# Get scraped data and check if those data ware send
# as notification or not.
def prepareData():
    # get last notice scraped data
    noticeData = getAllNE(dType='notice', page=0, limit=1)
    # check this data was send as notification or not
    if localData(objData=noticeData, filename=noticeFile):
        sendPushNotification(data=noticeData)
    else:
        print("No New Notification")

    time.sleep(20)

    # get last event scraped data
    eventData = getAllNE(dType='event', page=0, limit=1)
    # check this data was send as notification or not
    if localData(objData=eventData, filename=eventFile):
        sendPushNotification(data=eventData)
    else:
        print("No New Event")
