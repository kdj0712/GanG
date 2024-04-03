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
# TESTS = 문제 테이블(`TESTS_ID`,`QUESTIONS`,`RIGHT`,`POINT`,`QUESTION_NUM`)
# OPTION = 보기 테이블(	`OPTION_ID`,`TESTS_ID`,`OPTION`,`CORRECT`,`OPTION_NUM`)
# USER = 응시자 테이블(`USER_ID`,`USER`)
# RESPOND = 응시 테이블(`RESPOND_ID`,`TESTS_ID`,`USER_ID`,`OPTION_ID`)
def solve_quiz():

    try:
        with conn.cursor() as cursor:
            # Create
            sql = "INSERT INTO TableName (pk_id,column1, column2) VALUES (%s, %s, %s)"
            cursor.execute(sql, (1, 'value1', 'value2'))
            conn.commit()

            # Read
            sql = "SELECT * FROM TableName"
            cursor.execute(sql)
            data = cursor.fetchall()
            for row in data:
                print(row)  # 각 행 출력

            # Update
            sql = "UPDATE TableName SET column1=%s WHERE pk_id=%s"
            cursor.execute(sql, ('newvalue1', 1))
            conn.commit()

            # Delete
            sql = "DELETE FROM TableName WHERE pk_id=%s"
            cursor.execute(sql, (1,))
            conn.commit()

    finally:
        conn.close()

        while True:
            sql = "SELECT COUNT(USER_ID) FROM USER"
            cursor.execute(sql)
            user_number = cursor.fetchall()
            user_number = int(user_number[0][0])

            USER_NAME = input("이름을 입력하세요 : ")
            name= '{}'.format(USER_NAME)
            sql = "INSERT INTO USER (USER_ID,`USER`) VALUES ('USER_%s',%s)"
            cursor.execute(sql,(user_number+1,name))
            conn.commit()