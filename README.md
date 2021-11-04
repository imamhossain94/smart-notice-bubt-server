# Smart Notice BUBT 

A smart solution of notice and event for the students of BUBT.

## Problem

There have no official app available in the app store that able to reach the important notices and events to the students and faculty members of BUBT until they visit the official website of BUBT. 

## Solution [Only For Android]

To solve this problem, One years ago my friend <a href="https://github.com/xaadu"> Abdullah Zayed.</a> developed an API script that can scrapped all the notice and event of the BUBT website. Now, I re-write the script and bring some extra feature on it.

like-
* Scheduled app run.
* Push notification. etc..


## Three server
* smart-notice-bubt [94]
* smart-notice-bubt-two [95*]
* smart-notice-bubt-three [96]



## Library used

requirements.txt
```
appdirs==1.4.4
APScheduler==3.7.0
beautifulsoup4==4.9.3
bs4==0.0.1
CacheControl==0.12.6
cachetools==4.2.2
certifi==2021.5.30
cffi==1.14.6
chardet==4.0.0
charset-normalizer==2.0.3
click==7.1.2
colorama==0.4.4
distlib==0.3.2
filelock==3.0.12
firebase-admin==5.0.1
Flask==1.1.2
google-api-core==1.31.1
google-api-python-client==2.15.0
google-auth==1.34.0
google-auth-httplib2==0.1.0
google-cloud-core==1.7.2
google-cloud-firestore==2.2.0
google-cloud-storage==1.41.1
google-crc32c==1.1.2
google-resumable-media==1.3.2
googleapis-common-protos==1.53.0
grpcio==1.39.0
gunicorn==20.0.4
httplib2==0.19.1
idna==2.10
imgkit==1.0.2
itsdangerous==2.0.1
Jinja2==2.11.3
MarkupSafe==1.1.1
msgpack==1.0.2
numpy==1.20.1
packaging==21.0
Pillow==8.3.1
proto-plus==1.19.0
protobuf==3.17.3
pyasn1==0.4.8
pyasn1-modules==0.2.8
pycparser==2.20
pyparsing==2.4.7
python-dotenv==0.19.0
pytz==2021.1
requests==2.25.1
rsa==4.7.2
six==1.15.0
soupsieve==2.2.1
tabula==1.0.5
tzlocal==2.1
uritemplate==3.0.1
urllib3==1.26.3
virtualenv==20.4.2
Werkzeug==1.0.1

```


## API Example

* Type: [GET] https://smart-notice-bubt.herokuapp.com/bubt/v2/allNotice?page=0&limit=1

```json
{
  "data": [
    {
      "category": "General",
      "details": {
        "description": "Please download the files.\nInternship Lists\nProject Lists",
        "images": ""
      },
      "id": 618,
      "published_on": "1 Aug 2021",
      "title": "List of eligible students of the Textile Engineering Department  to appear in the Industrial Training and Practice exam and Project defense exam of summer 2020",
      "url": "https://www.bubt.edu.bd/home/notice_details/618"
    }
  ],
  "status": "success",
  "type": "notice"
}
```


## Heroku Deployment

* add-on: <a href="https://kaffeine.herokuapp.com/">Kaffeine</a>
* web: gunicorn wsgi:app
* clock: python clock.py
* sleep-time: 12:00 AM - 6:00 AM 


## 🧑 Author

#### Md. Imam Hossain

You can also follow my GitHub Profile to stay updated about my latest projects:

[![GitHub Follow](https://img.shields.io/badge/Connect-imamhossain94-blue.svg?logo=Github&longCache=true&style=social&label=Follow)](https://github.com/imamhossain94)

If you liked the repo then kindly support it by giving it a star ⭐!

Copyright (c) 2021 MD. IMAM HOSSAIN
