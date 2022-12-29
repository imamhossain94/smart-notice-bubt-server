# Smart Notice BUBT 

A smart solution of notice and event for the students of BUBT.

## Problem

There have no official app available in the app store that able to reach the important notices and events to the students and faculty members of BUBT until they visit the official website of BUBT. 

## Solution [Only For Android]

To solve this problem, One years ago my friend <a href="https://github.com/xaadu"> Abdullah Zayed.</a> developed an API script that can scrapped all the notice and event of the BUBT website. Now, I re-write the script and bring some extra feature on it.

like-
* Scheduled app run.
* Push notification. etc..


## Now this app is hosted on Mogenius Studio
* INSTANCE: 1
* CPU: 0.2 Core
* RAM: 256 MB
* TEMP STORAGE: 128 MB


## Library used

requirements.txt
```
APScheduler==3.9.1
beautifulsoup4==4.11.1
CacheControl==0.12.11
cachetools==5.0.0
certifi==2021.10.8
charset-normalizer==2.0.12
click==8.1.3
colorama==0.4.4
firebase-admin==5.2.0
Flask==2.1.2
google-api-core==2.7.2
google-api-python-client==2.46.0
google-auth==2.6.6
google-auth-httplib2==0.1.0
google-cloud-core==2.3.0
google-cloud-firestore==2.4.0
google-cloud-storage==2.3.0
google-crc32c==1.3.0
google-resumable-media==2.3.2
googleapis-common-protos==1.56.0
grpcio==1.44.0
grpcio-status==1.44.0
httplib2==0.20.4
idna==3.3
itsdangerous==2.1.2
Jinja2==3.1.2
MarkupSafe==2.1.1
msgpack==1.0.3
Pillow==9.1.0
proto-plus==1.20.3
protobuf==3.20.1
pyasn1==0.4.8
pyasn1-modules==0.2.8
pyparsing==3.0.8
python-dotenv==0.20.0
pytz==2022.1
pytz-deprecation-shim==0.1.0.post0
requests==2.27.1
rsa==4.8
six==1.16.0
soupsieve==2.3.2.post1
tzdata==2022.1
tzlocal==4.2
uritemplate==4.1.1
urllib3==1.26.9
Werkzeug==2.1.2
gunicorn==20.1.0
```


## API Example

* Type: [GET] https://bubt.onrender.com/bubt/v2/allNotice?page=0&limit=1

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


## 🧑 Author

#### Md. Imam Hossain

You can also follow my GitHub Profile to stay updated about my latest projects:

[![GitHub Follow](https://img.shields.io/badge/Connect-imamhossain94-blue.svg?logo=Github&longCache=true&style=social&label=Follow)](https://github.com/imamhossain94)

If you liked the repo then kindly support it by giving it a star ⭐!

Copyright (c) 2021 MD. IMAM HOSSAIN
