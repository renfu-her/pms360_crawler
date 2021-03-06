## 雲掌櫃 360pms.com 的 API

雲掌櫃 https://www.360pms.com 底下沒有開放訂單、房間、旅館的名稱以及 hid 的 API
參照基本的 order 去寫出來實際的爬蟲

## SQL 以及登入的 cookie 寫進去

初始值，請先跑一遍 pms360.sql

修改 main.py
- cookie_key = '你的 cookiekey'
- hotel_id = ['你的旅館的 hid']

如何取得的方式，請參照下圖
![參照圖](https://renfu-her.github.io/repo-images/website/360pms.png)

## API 說明

旅館
- curl -v -X GET http://localhost:5000/api/hotel

房間 
- curl -v -X GET http://localhost:5000/api/room

訂單
- curl -v -X GET http://localhost:5000/api/order
  - 這裏只有本月 + 上一個月份的資料會撈進來

訂單 & 房間的呈現的 API
- curl -v -X GET http://localhost:5000/api/space

## 

## 獨立跑 order 的資料

主要是它跑的時間可能約 1~6 分鐘不等的時間，所以獨立寫 order
pms360_crawler.py

- python pms360_crawler.py
- 這個功能可以用 cron 定時去跑

## 取得 hid

先登入 360pms 之後，以賬號：0922admin，密碼：123456 登入
使用的是 Chrome 以及 Edge 瀏覽器，可以用 F12 去查看自己的 hid 多少
登入後，直接看 cookie 就會得到 hid=7225，cookiekey=8bf8c5f6c48ab330c9ef25fb96ab67ab

所以登入的時候還需要改一下
- hid=7225
- cookie_key=8bf8c5f6c48ab330c9ef25fb96ab67ab

這樣就不會有問題了，畢竟是測試賬號

## bugfix

## changelog
- 2021-09-14
  - 修改 api
- 2021-09-10
  - 整個大改，基本是旅館、房間、訂單的資料的 API
- 2012-08-23
  - hid 以及 cookiekey 兩者要互相搭配，如果只有 cookiekey 就預設以開立的 hid 為主
- 2021-08-22 
  - 修改爬中間資料，有重覆的資料給拿掉
  - 增加 page 的分析

### 有如何的問題，歡迎在 issue 裏面提出來

- github: [pms360_crawler github](https://github.com/renfu-her/pms360_crawler)
