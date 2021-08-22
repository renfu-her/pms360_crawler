# 360pms.com 訂單的 API

雲掌櫃 https://www.360pms.com 底下沒有開放 API
只好寫個簡單的爬蟲出來，有如何的問題，歡迎在 issue 裏面提出來

## 使用方法，直接取得 json

用 order class 建立起來
```
# 登入系統
order = order('0922013171', 'Hezrid5')

# 呈現 2021-01-01 ~ 2021-08-31 的訂單
print(order.order_data(fromdate='2021-06-01', enddate='2021-08-31'))
```

想要的這裏也可以增加關鍵字的方式搜尋
```
print(order.order_data(fromdate='2021-06-01', enddate='2021-08-31', keywords='test'))
```

## changelog
- 2021-08-22 
  - 修改爬中間資料，有重覆的資料給拿掉
  - 增加 page 的分析

