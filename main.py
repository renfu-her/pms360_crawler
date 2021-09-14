import os
import re
import calendar
import settings

from ext import db
from flask import Flask, session, jsonify, render_template
from sqlalchemy import desc
from sqlalchemy.orm import scoped_session
from datetime import datetime, date, timedelta

from app.crawler import pms_360
from app.models import Pms360Order, Pms360Price

app = Flask(__name__)

# 將系統配置項Config類載入到app
app.config.from_object(settings.Config)
app.config['SECRET_KEY'] = "8q$5}EwyZBC}"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)

db.init_app(app)

# 這是雲掌櫃的測試賬號
cookie_key = '8bf8c5f6c48ab330c9ef25fb96ab67ab'
hotel_id = ['7225', '7226']

@app.route('/api/order', methods=['GET'])
def order_get():
    # 查詢當月的這裏
    to_date = datetime.now().date()
    fromdate = str(date(to_date.year, to_date.month, 1))
    enddate = str(date(to_date.year, to_date.month, calendar.monthrange(to_date.year, to_date.month)[1]))
    prices = Pms360Price.query.filter(Pms360Price.to_day >= datetime.strptime(fromdate, '%Y-%m-%d'),
                                      Pms360Price.to_day <= datetime.strptime(enddate, '%Y-%m-%d')).\
                                      order_by(Pms360Price.hotel_id, Pms360Price.order_id).all()

    result = []
    for price in prices:
        order = Pms360Order.query.filter_by(hotel_id=price.hotel_id, order_id=price.order_id).first()
        result.append({'hotel_id': price.hotel_id, 'order_id': price.order_id,
                       'room_id': order.room_id, 'room_name': order.room_name,
                       'channel_code': order.channel_code, 'channel_name': order.channel_name,
                       'to_day': price.to_day.strftime('%Y-%m-%d'), 'price': price.price})

    return jsonify({'status': 1, 'message': 'success', 'data': result})


@app.route('/api/hotel', methods=['GET'])
def hotel_get():
    result = []
    for hid in hotel_id:
        res = pms_360.order(hid, cookie_key)
        hotels = res.hotel_id()
        for hotel in hotels:
            hotelid = re.search('[0-9,]+', str(hotel))[0]
            hotel_name = re.search('<div[^>]*>([^<]+)</div>', str(hotel))[1]
            result.append({'hid': hotelid, 'hotel_name': hotel_name.strip()})

    res = []
    for i in result:
        if i not in res:
            res.append(i)

    return jsonify({"status": 0, "data": res})


@app.route('/api/room', methods=['GET'])
def room_get():
    result = []
    for hid in hotel_id:
        res = pms_360.order(hid, cookie_key)
        rooms = res.room_id()
        for room in rooms:
            roomid = re.search('roomid="[0-9,]+"', str(room)).group()
            room_id = re.search('[0-9,]+', roomid).group()
            roomtypename = re.search('roomtypename="[a-zA-Z0-9_()\u4e00-\u9fa5]+"', str(room)).group()
            room_type_name = re.search('"(.*)+"', roomtypename).group()
            room_type_name = room_type_name.replace('"', "")
            result.append({'hid': hid, 'roomid': room_id, 'roomtypename': room_type_name})

    return jsonify({'status': 0, 'data': result})


# space generators
@app.route('/api/space', methods=['GET'])
def space_get():
    to_date = datetime.now().date()
    fromdate = str(date(to_date.year, to_date.month, 1))
    enddate = str(date(to_date.year, to_date.month, calendar.monthrange(to_date.year, to_date.month)[1]))
    prices = Pms360Price.query.filter(Pms360Price.to_day >= datetime.strptime(fromdate, '%Y-%m-%d'),
                                      Pms360Price.to_day <= datetime.strptime(enddate, '%Y-%m-%d')).\
        order_by(Pms360Price.hotel_id, Pms360Price.order_id).all()

    result = []
    for price in prices:
        order = Pms360Order.query.filter_by(hotel_id=price.hotel_id, order_id=price.order_id).first()
        if order:
            # print(price.hotel_id, price.order_id)
            hotel_id = order.hotel_id
            order_id = order.order_id
            room_name = order.room_name
            result.append({'hotel_id': hotel_id, 'order_id': order_id, 'room_name': room_name,
                           'price': price.price, 'channel_name': order.channel_name,
                           'to_day': date.strftime(price.to_day, "%Y-%m-%d"), 'status': order.status})

    return jsonify({'status': 0, 'data': result})

@app.route('/report', methods=['GET'])
def dashboard():
    to_day = datetime.now().date()
    return render_template("report/index.html", to_day=to_day)


if __name__ == '__main__':
    app.run()