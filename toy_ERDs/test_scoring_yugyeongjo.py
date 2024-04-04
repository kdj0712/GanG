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

def scoring():
    try:
        with conn.cursor() as cursor:
            sql = (
                    "SELECT `USER`.`USER`,`USER`.USER_ID, SUM(CORRECT_ANSWER.POINT) "
                    "FROM `USER` "
                    "INNER JOIN ("
                    "    SELECT RESPOND.USER_ID, RESPOND.OPTION_ID, OPTION_CORRECT.CORRECT, TESTS.`POINT` "
                    "    FROM RESPOND "
                    "    INNER JOIN ("
                    "        SELECT * "
                    "        FROM `OPTION` "
                    "        WHERE CORRECT IS NOT NULL "
                    "    ) AS OPTION_CORRECT "
                    "    ON OPTION_CORRECT.OPTION_ID = RESPOND.OPTION_ID "
                    "    INNER JOIN TESTS ON TESTS.TESTS_ID = RESPOND.TESTS_ID) AS CORRECT_ANSWER "
                    "    ON CORRECT_ANSWER.USER_ID = `USER`.USER_ID "
                    "GROUP BY USER_ID "
                    "ORDER BY USER_ID, CAST(SUBSTRING_INDEX(`USER`.USER_ID, '_', -1) AS UNSIGNED) "
                    )
            cursor.execute(sql)
            scores = cursor.fetchall()
            dict_user_scores = {}
            user_score_total = 0
            for row in scores:
                USER_NAME, USER_ID, USER_SCORE = row
                key = (USER_NAME, USER_SCORE)  # 질문을 구분하는 키
                if key not in dict_user_scores: 
                    dict_user_scores[key] = {
                        'USER_NAME': USER_NAME,
                        'USER_SCORE': USER_SCORE
                    }
                print(f'{USER_NAME}', f'{USER_SCORE}점')
                
                user_score_total = user_score_total + USER_SCORE
            print("----------------------------------")
            
            # 전체 응시자 평균
            average = round(user_score_total/len(dict_user_scores))        
            print(f"전체 응시자 평균 : {average}점")
                
    finally:
        conn.close()
    
    return 

scoring()