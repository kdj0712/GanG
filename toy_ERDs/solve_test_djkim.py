# QUIZS = 문제 및 보기 문항 테이블(`PK_QUIZ_ID`,`CONTENT`,`POINTS`,`CORRECT`,`NUMBERS`,'FK_QUIZ_ID')
# USERS = 응시자 테이블(`USERS_ID`,`USERS`)
# RESPOND = 응시 테이블(`RESPOND_ID`,`PK_QUIZ_ID`,`USERS_ID`)
def solve_quiz():
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
            while True:
            # USER 테이블의 레코드 수를 학인하고 그 숫자를 반환하도록 설정
                sql = "SELECT COUNT(USERS_ID) FROM USERS"
                cursor.execute(sql)
                user_number = cursor.fetchall()
                user_number = int(user_number[0][0])
                # 사용자의 이름을 입력받아,USER 테이블에 저장할 때 프라이머리 키에 아까 받아온 숫자를 적용하도록 설정
                USER_NAME = input("이름을 입력하세요 : ")
                sql = "INSERT INTO USERS (USERS_ID, USERS) VALUES (%s, %s)"
                cursor.execute(sql, (f'USERS_{user_number+1}', USER_NAME))
                conn.commit()
                # 문제 테이블과 보기 테이블에 있는 정보들을 필요한 내용을 갖고 오도록 SELECT 구문 사용
                sql = (
                    "SELECT PK_QUIZ_ID, CONTENT, POINTS, CORRECT, NUMBERS, FK_QUIZ_ID "
                    "FROM QUIZS "
                    "ORDER BY CAST(SUBSTRING_INDEX(PK_QUIZ_ID, '_', -1) AS UNSIGNED), PK_QUIZ_ID"
                )
                cursor.execute(sql)
                quizs = cursor.fetchall()

                                # 퀴즈 데이터를 질문 기준으로 그룹화
                # 받아온 문제와 보기 정보를 담을 딕셔너리 초기화
                quiz_dict = {}

                # 받아온 문제와 보기의 정보 딕셔너리를 for 구문으로 구분
                for row in quizs:
                    PK_QUIZ_ID, CONTENT, POINTS, CORRECT, NUMBERS, FK_QUIZ_ID = row
                    
                    # 문제인 경우 (문제는 FK_QUIZ_ID가 NULL임을 가정)
                    if FK_QUIZ_ID == PK_QUIZ_ID:
                        # 문제를 quiz_dict에 추가
                        quiz_dict[PK_QUIZ_ID] = {
                            'PK_QUIZ_ID': PK_QUIZ_ID,
                            'CONTENT': CONTENT,
                            'NUMBERS': NUMBERS,
                            'POINTS': POINTS,
                            'OPTIONS': []  # 문제에 대한 옵션을 저장할 리스트
                        }
                    # 옵션인 경우
                    else:
                        # 옵션을 해당 문제의 'OPTIONS' 리스트에 추가
                        option = {
                            'PK_QUIZ_ID': PK_QUIZ_ID,
                            'CONTENT': CONTENT,
                            'CORRECT': CORRECT,
                            'NUMBERS': NUMBERS,
                            'FK_QUIZ_ID':FK_QUIZ_ID
                        }
                        quiz_dict[FK_QUIZ_ID]['OPTIONS'].append(option)


                # 결과 테스트 출력
                for quiz_id, quiz_info in quiz_dict.items():
                    print(f"{quiz_info['NUMBERS']} : {quiz_info['CONTENT']}")
                    for option in quiz_info['OPTIONS']:
                        print(f"{option['NUMBERS']}.{option['CONTENT']}")
                    # RESPOND 테이블의 레코드 수를 학인하고 그 숫자를 반환하도록 설정
                    selected_option_id = None
                    while selected_option_id is None:
                        answer = int(input(" 답 : "))  # 정답 입력 받기
                        for option in quiz_info['OPTIONS']:
                            if option['NUMBERS'] == answer:
                                selected_option_id = option['PK_QUIZ_ID']  # 옵션에 대한 고유 ID 또는 식별자를 가정합니다.
                                break

                        if selected_option_id is None:
                            print("잘못 입력하셨습니다.")

                    sql = "SELECT COUNT(RESPOND_ID) FROM RESPOND"
                    cursor.execute(sql)
                    respond_number = cursor.fetchall()[0][0]
                    # 문제에 대해 답변한 내용과 RESPOND 테이블에 필요한 내용들과, 더해서 응답 내용을 RESPOND_ID 저장할 때 프라이머리 키에 아까 받아온 숫자를 적용하도록 설정
                    sql = "INSERT INTO RESPOND (RESPOND_ID, PK_QUIZ_ID, USERS_ID) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (f"RESPOND_{respond_number+1}",selected_option_id,f"USERS_{user_number+1}"))
                    conn.commit()
                print("")
                keepgoing = input("다음 응시자가 있나요? (계속: c, 종료: x): ")
                while keepgoing.lower() not in ['c', 'x']:
                    print("잘못된 입력입니다. 다시 입력해주세요.")
                    keepgoing = input("다음 응시자가 있나요? (계속: c, 종료: x): ")
                if keepgoing.lower() == 'c':
                    continue
                elif keepgoing.lower() == 'x':
                    print("-----------------" * 5)
                    print("프로그램이 종료되었습니다.")
                    break

    except:
        conn.close()  # 연결을 닫는 코드를 finally 블록으로 이동

# solve_quiz(conn)