# 360pms.com crawler
import time, json
import pytz
import requests
import re
from bs4 import BeautifulSoup as bs

class order:

    def __init__(self, hid, cookiekey):
        self.hid = hid
        self.cookiekey = cookiekey
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Cookie': 'language=zh-tw; currency=NT%24; hid=' + hid + '; cookiekey=' + cookiekey,
            'Host': 'www.360pms.com',
            'Referer': 'https://www.360pms.com/Order/allorder/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.73'
        }

    def order_data(self, fromdate, enddate, keywords=''):
        headers = self.headers
        headers['Referer'] = 'https://www.360pms.com/book/index.html'

        session = requests.Session()

        # 參數
        url_query = f"?datetype=2&channel=allchannel&status=allstatus&fromdate={fromdate}&enddate={enddate}&keywords={keywords}"

        goto_next = True
        page_number = 1

        result = []
        while page_number > 0:
            response = session.get('https://www.360pms.com/Order/allorder' + url_query + f'&p={page_number}',
                                   headers=headers)
            soup = bs(response.text, 'html.parser')

            rows = soup.find('table', 'table').tbody.find_all('tr')

            page_max = 0
            for row in rows:
                all_tds = row.find_all('td')
                oid = ''
                rid = ''
                oid_result = ''
                rid_result = ''

                if len(all_tds) == 8:
                    page_max += 1
                    tds = str(all_tds[7])
                    # 以下采用 regex 的方法
                    oid = re.search('oid="[0-9]+"', tds).group()
                    oid_result = re.search('[0-9]+', oid).group()
                    rid = re.search('rid="[0-9]+"', tds).group()
                    rid_result = re.search('[0-9]+', rid).group()

                elif len(all_tds) == 4:
                    page_max += 1
                    tds = str(all_tds[3])
                    oid = re.search('oid="[0-9]+"', tds).group()
                    oid_result = re.search('[0-9]+', oid).group()
                    rid = re.search('rid="[0-9]+"', tds).group()
                    rid_result = re.search('[0-9]+', rid).group()

                if oid != '':
                    payload = {
                        'orderid': oid_result,
                        'rid': rid_result
                    }
                    response = session.post('https://www.360pms.com/Book/checkindetail?t=429', data=payload, headers=headers)
                    # print(json.loads(response.text))
                    res = json.loads(response.text)
                    result.append(res['orderdata'])

            if page_max < 30:
                break

            page_number += 1

        return result

    def hotel_id(self):
        hid = self.hid
        headers = self.headers
        headers['Referer'] = 'https://www.360pms.com/book/index.html'

        session = requests.Session()

        response = session.get('https://www.360pms.com/book/index.html?hid=' + hid, headers=headers)
        soup = bs(response.text, 'html.parser')

        row = soup.find_all("div", {"class": "item", "url": True})

        return row

    def room_id(self):
        hid = self.hid
        headers = self.headers
        headers['Referer'] = 'https://www.360pms.com/book/index.html'

        session = requests.Session()

        response = session.get('https://www.360pms.com/RoomType/index?hid=' + hid, headers=headers)
        soup = bs(response.text, 'html.parser')
        row = soup.find_all('tr', {"roomid": True, "roomtypename": True})

        return row


    def hotel_data(self):
        headers = self.headers
        headers['Referer'] = 'https://www.360pms.com/book/index.html'

        session = requests.Session()

        hotel_id = ['5225', '5263']

        for hid in hotel_id:
            response = session.get('https://www.360pms.com/Book/index?hid=' + hid, headers=headers)
            soup = bs(response.text, 'html.parser')

