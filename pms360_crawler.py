import calendar
from app.crawler import pms_360
from sqlalchemy import Column, Integer, String, Date, DateTime, Float, Text, \
                       ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker, joinedload
from datetime import datetime, date, timedelta

# For this example we will use an in-memory sqlite 
# Let's also configure it to echo everything it does to the screen.
engine = create_engine('mysql+pymysql://root:hezrid5@localhost/pms360')

# The base class which our objects will be defined on.
Base = declarative_base()


# 建立資料表
class Pms360Order(Base):
    __tablename__ = 'pms360_orders'
    id = Column(Integer, primary_key=True)
    hotel_id = Column(Integer)
    order_id = Column(String(255), nullable=False)
    room_id = Column(String(255), nullable=False)
    room_name = Column(String(255), nullable=False)
    channel_code = Column(String(255), nullable=False)
    channel_name = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    total_price = Column(Float, nullable=False)
    start_end_days = Column(Integer, nullable=False)
    memo = Column(Text)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


# 處理 360pms 每一天的金額
class Pms369Price(Base):
    __tablename__ = 'pms360_prices'
    id = Column(Integer, primary_key=True)
    hotel_id = Column(Integer)
    order_id = Column(String(255), nullable=False)
    to_day = Column(Date, nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

# 建立 session
Session = sessionmaker(bind=engine)
session = Session()

# cookie 產生的
# cookiekey=[賬號以及密碼通過會產生的唯一值]; hid=[旅館]
cookie_key = '8bf8c5f6c48ab330c9ef25fb96ab67ab'
hotel_id = ['7225', '7226']

def space_get_all():
    to_day = datetime.now().date()
    fromdate = str(date(to_day.year, to_day.month, 1))
    enddate = str(date(to_day.year, to_day.month, calendar.monthrange(to_day.year, to_day.month)[1]))
    today_fromdate = fromdate
    today_enddate = enddate
    last_fromdate = str(date(to_day.year, to_day.month - 1, 1))
    last_enddate = str(date(to_day.year, to_day.month - 1, calendar.monthrange(to_day.year, to_day.month - 1)[1]))
    keywords = ''

    fromdate_list = [last_fromdate, fromdate]

    for val in fromdate_list:
        if val == last_fromdate:
            fromdate = last_fromdate
            enddate = last_enddate
        else:
            fromdate = today_fromdate
            enddate = today_enddate

        for hid in hotel_id:
            res = pms_360.order(hid, cookie_key)
            result = res.order_data(fromdate, enddate, keywords)
            for res in result:
                channel_code = res['channelcode']
                channel_name = res['channelname']
                order_id = res['checkoutinfo']['orderinfo'][0]['id']
                room_id = res['orderlist'][0]['roomid']
                room_name = res['checkoutinfo']['orderinfo'][0]['roomtypename']
                start_date = res['arrivedate']
                end_date = res['enddate']
                total_price = float(res['checkoutinfo']['orderinfo'][0]['totalprice'])
                memo = res['checkoutinfo']['orderinfo'][0]['remark']
                status = res['orderstatus']
                datetime_start_date = datetime.strptime(start_date, '%Y-%m-%d')
                datetime_end_date = datetime.strptime(end_date, '%Y-%m-%d')
                start_end_days = datetime_end_date - datetime_start_date
                # print(order_id, start_end_days.days)
                chk = session.query(Pms360Order).filter_by(order_id=order_id).first()
                if chk is None:
                    pms = Pms360Order(hotel_id=hid, order_id=order_id, room_id=room_id,
                                      channel_code=channel_code, channel_name=channel_name,
                                      room_name=room_name, start_date=start_date, end_date=end_date,
                                      total_price=total_price, memo=memo, status=status,
                                      start_end_days=start_end_days.days
                                      )
                    session.add(pms)
                    session.commit()
                    # 展開每天的金額

    orders = session.query(Pms360Order).all()
    for hotel in hotel_id:
        for order in orders:
            chk = session.query(Pms369Price).filter_by(order_id=order.order_id, hotel_id=hotel).first()
            # print(order.order_id, hotel, chk)
            if chk is None:
                start_date = order.start_date
                start_days = order.start_end_days
                if order.total_price == 0:
                    price = 0
                else:
                    if order.start_end_days == 0:
                        price = order.total_price
                    else:
                        price = order.total_price / order.start_end_days

                result = []
                for idx in range(0, start_days):
                    step_days = (start_date + timedelta(days=idx)).strftime('%Y-%m-%d')
                    result.append(Pms369Price(hotel_id=order.hotel_id, order_id=order.order_id,
                                              to_day=step_days, price=price))
                    # print(order.order_id, start_days, price, step_days)

                session.add_all(result)
                session.commit()

    res = session.query(Pms360Order).all()
    result = []
    for r in res:
        result.append({'hotel_id': r.hotel_id, 'order_id': r.order_id,
                       'channel_name': r.channel_name, 'channel_code': r.channel_code,
                       'room_id': r.room_id, 'room_name': r.room_name,
                       'start_date': date.strftime(r.end_date, '%Y-%m-%d'), 'end_date': date.strftime(r.end_date, '%Y-%m-%d'),
                       'status': r.status, 'total_price': r.total_price, 'memo': r.memo})

    print(result)


space_get_all()
