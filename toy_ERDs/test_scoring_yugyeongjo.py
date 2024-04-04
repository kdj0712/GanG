import pymysql
from pymysql.cursors import DictCursor

# 데이터베이스 연결 설정
conn = pymysql.connect(
    host='trainings.iptime.org',  # 컨테이너 이름 또는 IP
    port = 48009,
    user='cocolabhub',
    password='cocolabhub',
    db='python_mysql',  # 데이터베이스 이름
    charset='utf8mb4',
)

try:
    with conn.cursor() as cursor:
        
        
finally:
    conn.close()