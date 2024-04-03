import pymysql

# 데이터베이스 연결 설정
def connect():
    conn = pymysql.connect(
        host='192.168.10.236',  # 컨테이너 이름 또는 IP
        port = 3306,
        user='cocolabhub',
        password='cocolabhub',
        db='python_mysql',  # 데이터베이스 이름
        charset='utf8mb4'
    )
    return conn

