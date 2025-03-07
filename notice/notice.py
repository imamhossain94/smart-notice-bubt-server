import os
from bs4 import BeautifulSoup
from flask import Blueprint, request, jsonify
from requests import get, compat
from dotenv import load_dotenv

load_dotenv()

baseURL = os.environ.get('BASE_URL', '')
noticesURL = os.environ.get('NOTICE_URL', '')
eventsURL = os.environ.get('EVENT_URL', '')

# Apps Blueprint
notice = Blueprint('notice', __name__)


# Scraped Notice or Event
def getAllNE(dType, page, limit):
    finalData = {
        'data': list()
    }
    try:
        url = noticesURL if dType == 'notice' else eventsURL
        NE_HTML = get(url, timeout=30).text
        NE_HTML = BeautifulSoup(str(NE_HTML), 'html.parser').find_all('table')[0]
        rows = BeautifulSoup(str(NE_HTML), 'html.parser').find_all('tr')[1:]

        items = len(rows)

        start = page * limit
        end = page * limit + limit

        if start > items:
            start = items
        if end > items:
            end = items

        for row in rows[int(start): int(end)]:
            cols = row.find_all('td')
            detailUrl = cols[0].a['href'].strip()
            details = getDetails(detailUrl)

            localData = {
                'id': int(detailUrl.split("/")[-1]),
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
        finalData['status'] = 'success'
        finalData['type'] = dType
    except Exception as e:
        finalData = {'status': 'failed', 'reason': str(e)}

    return finalData


# Get scrapped notice in detailed
def getDetails(url):
    finalData = {
        'data': dict()
    }
    try:
        noticeHTML = get(url, timeout=30).text
        noticeHTML = BeautifulSoup(str(noticeHTML), 'html.parser').find('div', {'class': 'devs_history_body'})
        images = noticeHTML.find_all('img')
        if len(images) != 0:
            imageUrl = compat.urljoin(baseURL, images[0]['src'])
        else:
            imageUrl = ''

        finalData['data'] = {
            'description': noticeHTML.find('div', {'class': 'event-details'}).text.strip(),
            'images': imageUrl
        }

    except Exception as e:
        print(e)
        finalData['data'] = {'description': 'none', 'images': ''}

    return finalData


# Main route
@notice.route('/bubt/v2/<dataType>', methods=['GET'])
def dataBUBT(dataType):
    print(request.args)
    if dataType in ['allNotice', 'noticeDetails', 'allEvent', 'eventDetails']:
        if dataType == 'allNotice':
            data = getAllNE(dType='notice', page=int(request.args.get('page')), limit=int(request.args.get('limit')))

        elif dataType == 'allEvent':
            data = getAllNE(dType='event', page=int(request.args.get('page')), limit=int(request.args.get('limit')))

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
