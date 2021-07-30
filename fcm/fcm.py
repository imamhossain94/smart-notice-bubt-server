import json
import os.path
from io import BytesIO
import firebase_admin
import requests
from PIL import Image
from firebase_admin import credentials, storage
from notice.notice import *

# Auth google admin sdk
cred = credentials.Certificate('key.json')

# Initialize firebase app with storage bucket
firebase_admin.initialize_app(cred, {
    'storageBucket': 'smart-notice-bubt.appspot.com'
})

# Directory information
baseDirectory = 'resources'
noticeFile = baseDirectory + '/latestNotice.json'
eventFile = baseDirectory + '/latestEvent.json'
imageFile = baseDirectory + '/photo.jpg'

# Cloud messaging instance
serverToken = os.environ.get('FCM_SERVER_TOKEN', '')
deviceToken = os.environ.get('FCM_DEVICE_TOKEN', '')
topic = os.environ.get('FCM_TOPIC', '')

# Header for fcm
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'key=' + serverToken,
}


# Upload file in firebase storage
def upload_blob():
    bucket = storage.bucket()
    # File will be save in storage with this name
    blob = bucket.blob('image.jpg')
    # Browse file to upload
    blob.upload_from_filename(imageFile)
    # Making file url public
    blob.make_public()
    # Getting file url and retuning
    return blob.public_url


# Create push notification payload an send.
def sendPushNotification(nType, data):
    # get image url
    imageUrl = data['data'][0]['details']['images']

    # checking if image url is not null
    if imageUrl:
        # Download image from url
        response = requests.get(imageUrl)
        img = Image.open(BytesIO(response.content))
        # Resize image url 1000px * 500px to reduce image size under 1MB
        img = img.resize((1000, 500), Image.ANTIALIAS)
        # Save image in file
        img.save(imageFile, 'JPEG')
        # Upload image into firebase storage and get image url
        imageUrl = upload_blob()

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

    # Saving last send notification data
    with open(noticeFile if nType == 'notice' else eventFile, 'w+') as f:
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
    noticeData = getAllNE(dType='notice', page=1, limit=1)
    # check this data was send as notification or not
    if localData(objData=noticeData, filename=noticeFile):
        sendPushNotification(nType='notice', data=noticeData)
    else:
        print("No New Notification")

    # get last event scraped data
    eventData = getAllNE(dType='event', page=0, limit=1)
    # check this data was send as notification or not
    if localData(objData=eventData, filename=eventFile):
        sendPushNotification(nType='event', data=eventData)
    else:
        print("No New Event")
