class Config:
    # 設定mysql pymysql的連線
    # oracle
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:hezrid5@localhost/pms360'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/line-api'
    # 關閉資料追蹤
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 開啟提交
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
