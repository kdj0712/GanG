import pymysql

# 데이터베이스 연결 설정
conn = pymysql.connect(
    host='trainings.iptime.org',  # 컨테이너 이름 또는 IP
    port = 48009,
    user='cocolabhub',
    password='cocolabhub',
    db='python_mysql',  # 데이터베이스 이름
    charset='utf8mb4'
)


with conn.cursor() as cursor:
    sql = "SELECT COUNT(USER_ID) FROM USER"
    cursor.execute(sql)
    user_number = cursor.fetchall()
    user_number = int(user_number[0][0])

    USER_NAME = input("이름을 입력하세요 : ")
    name= '{}'.format(USER_NAME)
    sql = "INSERT INTO USER (USER_ID,`USER`) VALUES ('USER_%s',%s)"
    cursor.execute(sql,(user_number+1,name))
    conn.commit()