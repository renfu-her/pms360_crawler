## 雲掌櫃 360pms.com 的 API

雲掌櫃 https://www.360pms.com 底下沒有開放訂單、房間、旅館的名稱以及 hid 的 API
參照基本的 order 去寫出來實際的爬蟲

# SQL 以及登入的 cookie 寫進去

初始值，請先跑一遍 pms360.sql

修改 main.py
- cookie_key = '你的 cookiekey'
- hotel_id = ['你的旅館的 hid']

如何取得的方式，請參照下圖
![](https://renfu-her.github.io/repo-images/website/360pms.png)

## API 說明

旅館
- curl -v -X GET http://localhost:5000/hotel

訂單
- curl -v -X GET http://localhost:5000/order

房間 
- curl -v -X GET http://localhost:5000/room

有如何的問題，歡迎在 issue 裏面提出來

- github: https://github.com/renfu-her/pms360_crawler

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
- 2021-09-10
  - 整個大改，基本是旅館、房間、訂單的資料的 API
- 2012-08-23
  - hid 以及 cookiekey 兩者要互相搭配，如果只有 cookiekey 就預設以開立的 hid 為主
- 2021-08-22 
  - 修改爬中間資料，有重覆的資料給拿掉
  - 增加 page 的分析