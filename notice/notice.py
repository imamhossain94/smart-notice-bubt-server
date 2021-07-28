from flask import Blueprint, request, jsonify
from requests import get
from bs4 import BeautifulSoup

noticesURL = 'https://www.bubt.edu.bd/Home/all_notice'
eventsURL = 'https://www.bubt.edu.bd/Home/all_events'

notice = Blueprint('notice', __name__)


def getAllNE(dType):
    finalData = {
        'data': list()
    }

    try:
        url = noticesURL if dType == 'notice' else eventsURL
        NE_HTML = get(url).text
        NE_HTML = BeautifulSoup(str(NE_HTML), 'html.parser').find_all('table')[0]
        rows = BeautifulSoup(str(NE_HTML), 'html.parser').find_all('tr')[1:]
        for row in rows:
            cols = row.find_all('td')
            localData = {
                'title': cols[0].text.strip(),
                'published_on': cols[2 if dType == 'notice' else 1].text.strip(),
                'url': cols[0].a['href'].strip()
            }
            if dType == 'notice':
                localData['category'] = cols[1].text.strip()
            finalData['data'].append(localData)
        print(len(rows))
        with open('test.html', 'w', encoding='utf-8') as f:
            f.write(str(NE_HTML))
        finalData['status'] = 'success'
    except Exception as e:
        raise
        finalData = {'status': 'failed', 'reason': str(e)}

    return finalData


def getDetails(url):
    finalData = {
        'data': dict()
    }

    try:
        noticeHTML = get(url).text
        noticeHTML = BeautifulSoup(str(noticeHTML), 'html.parser').find('div', {'class': 'devs_history_body'})
        pubDate = noticeHTML.h3.span.text
        baseURL = 'https://www.bubt.edu.bd'
        finalData['data'] = {
            'title': noticeHTML.h3.text.replace(pubDate, '').strip(),
            'pubDate': pubDate.split(':')[-1].strip(),
            'description': noticeHTML.find('div', {'class': 'event-details'}).text.strip(),
            'images': [{'url': baseURL + u['src']} for u in noticeHTML.find_all('img')],
            'downloads': [{'url': u['href']} for u in noticeHTML.find_all('a')]
        }
        if len(finalData['data']['images']) == 0:
            finalData['data']['images'].append({'url': ''})
        if len(finalData['data']['downloads']) == 0:
            finalData['data']['downloads'].append({'url': ''})
        with open('test.html', 'w', encoding='utf-8') as f:
            f.write(str(noticeHTML))
        finalData['status'] = 'success'
    except Exception as e:
        raise
        finalData = {'status': 'failed', 'reason': str(e)}

    return finalData


@notice.route('/bubt/v1/<dataType>', methods=['GET'])
def dataBUBT(dataType):
    print(request.args)
    if dataType in ['allNotice', 'noticeDetails', 'allEvent', 'eventDetails', 'getResult']:
        if dataType == 'allNotice':
            data = getAllNE(dType='notice')
        elif dataType == 'allEvent':
            data = getAllNE(dType='event')
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
