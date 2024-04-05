

def scoring():
    import pymysql

    # 데이터베이스 연결 설정
    conn = pymysql.connect(
        host='trainings.iptime.org',  # 컨테이너 이름 또는 IP
        port = 48009,
        user='root',
        password='cocolabhub',
        db='QUIZS_DJKIM',  # 데이터베이스 이름
        charset='utf8mb4',
    )
    try:
        with conn.cursor() as cursor:
            sql = (
                    "SELECT "
                        "U.USERS_ID, "
                        "U.USERS AS USERS, "
                        "COALESCE(SUM(Q2.POINTS), 0) AS USER_SCORE "
                    "FROM USERS U "
                    "LEFT JOIN RESPOND R ON U.USERS_ID = R.USERS_ID "
                    "LEFT JOIN QUIZS Q ON R.PK_QUIZ_ID = Q.PK_QUIZ_ID "
                    "LEFT JOIN QUIZS AS Q2 ON Q.FK_QUIZ_ID = Q2.PK_QUIZ_ID AND Q.CORRECT IS NOT NULL "
                    "GROUP BY U.USERS_ID, U.USERS "
                    "ORDER BY CAST(SUBSTRING_INDEX(U.USERS_ID, '_', -1) AS UNSIGNED), U.USERS_ID"
                    )
            cursor.execute(sql)
            scores = cursor.fetchall()
            dict_user_scores = {}
            user_score_total = 0
            for row in scores:
                USERS_ID, USERS, USER_SCORE = row
                key = (USERS, USER_SCORE)  # 질문을 구분하는 키
                if key not in dict_user_scores: 
                    dict_user_scores[key] = {
                        'USER_NAME': USERS,
                        'USER_SCORE': USER_SCORE
                    }
                print(f'{USERS}', f'{USER_SCORE}점')
                
                user_score_total = user_score_total + USER_SCORE
            print("----------------------------------")
            
            # 전체 응시자 평균
            average = round(user_score_total/len(dict_user_scores))        
            print(f"전체 응시자 평균 : {average}점")
                
    finally:
        conn.close()
    
    return 

# scoring()