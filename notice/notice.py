import os
from bs4 import BeautifulSoup
from flask import Blueprint, request, jsonify
from requests import get
from dotenv import load_dotenv

load_dotenv()

noticesURL = os.environ.get('NOTICE_URL', 'lal')
eventsURL = os.environ.get('EVENT_URL', 'lal')

notice = Blueprint('notice', __name__)


# Shut down the scheduler when exiting the app
# atexit.register(lambda: scheduler.shutdown())


def getAllNE(dType, startLimit, endLimit):
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(func=print_date_time(), trigger="interval", seconds=15)
    # scheduler.start()

    # sendPush()
    finalData = {
        'data': list()
    }
    try:
        url = noticesURL if dType == 'notice' else eventsURL
        NE_HTML = get(url).text
        NE_HTML = BeautifulSoup(str(NE_HTML), 'html.parser').find_all('table')[0]
        rows = BeautifulSoup(str(NE_HTML), 'html.parser').find_all('tr')[1:]
        for row in rows[int(startLimit): int(endLimit)]:
            cols = row.find_all('td')

            details = getDetails(cols[0].a['href'].strip())

            print(details)

            localData = {
                'title': cols[0].text.strip(),
                'published_on': cols[2 if dType == 'notice' else 1].text.strip(),
                'url': cols[0].a['href'].strip(),
                'details': details.get('data'),
            }
            if dType == 'notice':
                localData['category'] = cols[1].text.strip()
            else:
                localData['category'] = "Event"

            finalData['data'].append(localData)
        print(len(rows))

        finalData['status'] = 'success'
    except Exception as e:
        finalData = {'status': 'failed', 'reason': str(e)}

    return finalData


def getDetails(url):
    finalData = {
        'data': dict()
    }
    try:
        noticeHTML = get(url).text
        noticeHTML = BeautifulSoup(str(noticeHTML), 'html.parser').find('div', {'class': 'devs_history_body'})
        baseURL = 'https://www.bubt.edu.bd'

        finalData['data'] = {
            'description': noticeHTML.find('div', {'class': 'event-details'}).text.strip(),
            'images': baseURL + noticeHTML.find_all('img')[0]['src'],
        }
        if len(finalData['data']['images']) == 0:
            finalData['data']['images'].append({'url': ''})

    except Exception as e:
        print(e)
        finalData['data'] = {'description': 'none', 'images': ''}

    return finalData


@notice.route('/bubt/v1/<dataType>', methods=['GET'])
def dataBUBT(dataType):
    print(request.args)
    if dataType in ['allNotice', 'noticeDetails', 'allEvent', 'eventDetails', 'getResult']:
        if dataType == 'allNotice':
            data = getAllNE(dType='notice', startLimit=request.args.get('sl'), endLimit=request.args.get('el'))
        elif dataType == 'allEvent':
            data = getAllNE(dType='event', startLimit=request.args.get('sl'), endLimit=request.args.get('el'))
        elif dataType == 'noticeDetails' or dataType == 'eventDetails':
            url = request.args.get('url')
            if url is not None:
                data = getDetails(url)
            else:
                data = {'status': 'failed', 'reason': 'No URL Provided!'}
        else:
            data = {'status': 'failed', 'reason': 'No URL Provided!'}
    else:
        data = {'status': 'failed', 'reason': 'No URL Provided!'}
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
