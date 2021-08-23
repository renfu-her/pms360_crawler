## 360pms.com 訂單的 API

雲掌櫃 https://www.360pms.com 底下沒有開放訂單的 API
寫個簡單的爬蟲出來，有如何的問題，歡迎在 issue 裏面提出來

- github: https://github.com/renfu-her/pms360_crawler

## 取得 hid

先登入 360pms 之後，以賬號：0922123456，密碼：Hezrid5 就可以看到
分店取得方式，如果使用的是 Chrome 以及 Edge 瀏覽器，可以用 F12 去查看自己的 hid 多少
以 0922013171 的方式，就可以得到 hid=7202，cookiekey=5ca7cc0e6a43da9887282f2fd36b7c5d

所以登入的時候還需要改一下
- hid=7202
- cookiekey=5ca7cc0e6a43da9887282f2fd36b7c5d

這樣就不會有問題

## 使用方法，直接取得 json

用 order class 建立起來
```
# 直接使用 cookle 就可以進入使用了
order = order(hid='7202', cookiekey='5ca7cc0e6a43da9887282f2fd36b7c5d')

# 呈現 2021-01-01 ~ 2021-08-31 的訂單
print(order.order_data(fromdate='2021-06-01', enddate='2021-08-31'))
```

想要的這裏也可以增加關鍵字的方式搜尋
```
print(order.order_data(fromdate='2021-06-01', enddate='2021-08-31', keywords='test'))
```

## bugfix

- ~~cookie 設定，分店采用 hid=xxx，所以不論那個賬號，只要可以登入都可以透過修改 hid 的方法去取得非自己的分店訂單資料~~

## changelog
- 2012-08-23
  - hid 以及 cookiekey 兩者要互相搭配，如果只有 cookiekey 就預設以開立的 hid 為主
- 2021-08-22 
  - 修改爬中間資料，有重覆的資料給拿掉
  - 增加 page 的分析