import time
from firebase_admin import storage, firestore
from notice.notice import getAllNE
import firebase_admin
from firebase_admin import credentials

# Auth google admin sdk
cred = credentials.Certificate('key.json')

# Initialize firebase app with storage bucket
firebase_admin.initialize_app(cred, {'storageBucket': 'smart-notice-bubt.appspot.com'})


db = firestore.client()

# Collection name
noticeRef = db.collection('events')
eventsRef = db.collection('events')


def uploadDocuments(data):
    try:
        docRef = noticeRef if data['type'] == 'notice' else eventsRef
        for item in data['data']:
            docRef.document(str(item['id'])).set(item)
            print("Uploaded: " + str(item['id']))
    except Exception as e:
        print("Error Uploading Documents: " + str(e))


def uploadFile(filename):
    try:
        bucket = storage.bucket()
        blob = bucket.blob('noticeImage' if 'notice' in filename else 'eventImage')
        blob.upload_from_filename(filename)
        blob.make_public()
        return blob.public_url
    except Exception as e:
        print("Error Uploading Image :" + str(e))
        return ""


def uploadDocIfNotExist():
    # collection = noticeRef.get()
    # if not collection:
    #     print('Uploading Notice')
    #     noticeData = getAllNE(dType='notice', page=0, limit=521)
    #     uploadDocuments(data=noticeData)
    #
    # time.sleep(20)
    collection = eventsRef.get()
    if not collection:
        print('Uploading Events')
        eventData = getAllNE(dType='event', page=0, limit=12)
        uploadDocuments(data=eventData)
