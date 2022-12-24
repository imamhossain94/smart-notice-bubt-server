import os
import time
from firebase_admin import storage, firestore
from notice.notice import getAllNE
import firebase_admin
from firebase_admin import credentials

firebase_credentials = {
    "type": os.environ.get("TYPE"),
    "project_id": os.environ.get("PROJECT_ID"),
    "private_key_id": os.environ.get("PRIVATE_KEY_ID"),
    "private_key": os.environ.get("PRIVATE_KEY").replace(r'\n', '\n'),
    "client_email": os.environ.get("CLIENT_EMAIL"),
    "client_id": os.environ.get("CLIENT_ID"),
    "auth_uri": os.environ.get("AUTH_URI"),
    "token_uri": os.environ.get("TOKEN_URI"),
    "auth_provider_x509_cert_url": os.environ.get("AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.environ.get("CLIENT_X509_CERT_URL")
}

# Auth google admin sdk
cred = credentials.Certificate(firebase_credentials)


# Initialize firebase app with storage bucket
firebase_admin.initialize_app(cred, {'storageBucket': 'smart-notice-bubt.appspot.com'})

db = firestore.client()

# Collection name
noticeRef = db.collection('notice')
eventsRef = db.collection('events')


def checkNoticeExistence(data):
    try:
        docRef = noticeRef.document(str(data['id'])).get()
        return True if docRef.exists else False
    except Exception as e:
        print("Error Checking Documents (Notice): " + str(e))
        return False


def checkEventExistence(data):
    try:
        docRef = eventsRef.document(str(data['id'])).get()
        return True if docRef.exists else False
    except Exception as e:
        print("Error Checking Documents (Events): " + str(e))
        return False


def uploadDocuments(data):
    try:
        docRef = noticeRef if data['type'] == 'notice' else eventsRef
        if 'type' in data:
            data.pop('type')
        docRef.document(str(data['id'])).set(data)
        print(data['type'] + " uploaded: " + str(data['id']))
    except Exception as e:
        print("Error Uploading Documents: " + str(e))


def uploadFile(buffer, data_type):
    try:
        bucket = storage.bucket()
        blob = bucket.blob('noticeImage' if 'notice' in data_type else 'eventImage')
        blob.upload_from_string(buffer.getvalue(), content_type='image/jpeg')
        blob.make_public()
        return blob.public_url
    except Exception as e:
        print("Error Uploading Image :" + str(e))
        return ""


def uploadDocIfNotExist():
    collection = noticeRef.get()
    if not collection:
        print('Uploading Notice')
        noticeData = getAllNE(dType='notice', page=0, limit=521)
        uploadDocuments(data=noticeData)

    time.sleep(20)
    collection = eventsRef.get()
    if not collection:
        print('Uploading Events')
        eventData = getAllNE(dType='event', page=0, limit=12)
        uploadDocuments(data=eventData)

