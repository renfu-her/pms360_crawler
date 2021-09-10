# 匯入db
import pytz
from ext import db
from datetime import date, datetime


# 房間
class Pms360Order(db.Model):
    __tablename__ = 'pms360_orders'
    id = db.Column(db.Integer, primary_key=True)
    hotel_id = db.Column(db.Integer)
    order_id = db.Column(db.String(255), nullable=False)
    room_id = db.Column(db.String(255), nullable=False)
    room_name = db.Column(db.String(255), nullable=False)
    channel_code = db.Column(db.String(255), nullable=False)
    channel_name = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    start_end_days = db.Column(db.Integer, nullable=False)
    memo = db.Column(db.Text)
    status = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


# 處理 360pms 每一天的金額
class Pms360Price(db.Model):
    __tablename__ = 'pms360_prices'
    id = db.Column(db.Integer, primary_key=True)
    hotel_id = db.Column(db.Integer)
    order_id = db.Column(db.String(255), nullable=False)
    to_day = db.Column(db.Date, nullable=False)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
