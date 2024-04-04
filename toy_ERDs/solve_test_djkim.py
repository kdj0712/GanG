
# TESTS = 문제 테이블(`TESTS_ID`,`QUESTIONS`,`RIGHT`,`POINT`,`QUESTION_NUM`)
# OPTION = 보기 테이블(	`OPTION_ID`,`TESTS_ID`,`OPTION`,`CORRECT`,`OPTION_NUM`)
# USER = 응시자 테이블(`USER_ID`,`USER`)
# RESPOND = 응시 테이블(`RESPOND_ID`,`TESTS_ID`,`USER_ID`,`OPTION_ID`)
def solve_quiz():
    import pymysql

    # 데이터베이스 연결 설정
    conn = pymysql.connect(
        host='trainings.iptime.org',  # 컨테이너 이름 또는 IP
        port = 48009,
        user='cocolabhub',
        password='cocolabhub',
        db='python_mysql',  # 데이터베이스 이름
        charset='utf8mb4',
        # cursorclass = DictCursor
    )
    try:
        with conn.cursor() as cursor:
            while True:
                # USER 테이블의 레코드 수를 학인하고 그 숫자를 반환하도록 설정
                sql = "SELECT COUNT(USER_ID) FROM USER"
                cursor.execute(sql)
                user_number = cursor.fetchall()
                user_number = int(user_number[0][0])
                # 사용자의 이름을 입력받아,USER 테이블에 저장할 때 프라이머리 키에 아까 받아온 숫자를 적용하도록 설정
                USER_NAME = input("이름을 입력하세요 : ")
                name= '{}'.format(USER_NAME)
                sql = "INSERT INTO USER (USER_ID,`USER`) VALUES ('USER_%s',%s)"
                cursor.execute(sql,(user_number+1,name))
                conn.commit()
                # 문제 테이블과 보기 테이블에 있는 정보들을 필요한 내용을 갖고 오도록 SELECT 구문 사용
                sql = (
                            "SELECT TESTS.TESTS_ID, `OPTION`.OPTION_ID, QUESTIONS, QUESTION_NUM, `OPTION`, OPTION_NUM "
                            "FROM TESTS "
                            "INNER JOIN `OPTION` ON TESTS.TESTS_ID = `OPTION`.TESTS_ID "
                            "ORDER BY TESTS.TESTS_ID, "
                            "CAST(SUBSTRING_INDEX(`OPTION`.OPTION_ID, '_', -1) AS UNSIGNED), " # VARCHAR 타입 텍스트의 정렬을 가능하게 할 수 있도록 조건을 추가
                            "`OPTION`.OPTION_ID"
                        )
                cursor.execute(sql)
                quizs = cursor.fetchall()

                # 퀴즈 데이터를 질문 기준으로 그룹화
                quiz_dict = {} 
                for row in quizs: # 받아온 문제와 보기의 정보 딕셔너리를 for 구문으로 구분
                    TESTS_ID, OPTION_ID, QUESTIONS, QUESTION_NUM, OPTION, OPTION_NUM = row
                    key = (TESTS_ID, QUESTION_NUM)  # 질문을 구분하는 키
                    if key not in quiz_dict: 
                        quiz_dict[key] = {
                            'QUESTION_NUM': QUESTION_NUM,
                            'QUESTIONS': QUESTIONS,
                            'OPTIONS': []
                        }
                    quiz_dict[key]['OPTIONS'].append((OPTION_NUM, OPTION, OPTION_ID)) # 순차적으로 딕셔너리에 내용을 전달하는 구문을 반복 시킴

                # 질문과 보기 항목 출력
                previous_test_id = None # 문제 번호를 인식시킬 previous_test_id라는 변수 선언
                for key, value in quiz_dict.items(): # 딕셔너리의 내용을 키와 밸류로 각각 분류시키는 작업을 딕셔너리의 갯수만큼 반복하도록 함
                    TESTS_ID, QUESTION_NUM = key
                    if TESTS_ID != previous_test_id: # 이전 번호와 현재 갖고 온 문제 번호를 비교하여 동일하지 않을 경우
                        print(f"{value['QUESTION_NUM']}. {value['QUESTIONS']}") # 문제 번호와 문제 내용을 출력
                        previous_test_id = TESTS_ID                             # 현재 문제 번호를 previous_test_id로 선언
                    for option in sorted(value['OPTIONS'], key=lambda x: x[0]):  # 딕셔너리 안에 있는 보기의 번호 순으로 정렬
                        OPTION_NUM, OPTION, OPTION_ID  = option                  # option에 있는 내용을 분리
                        print(f'{OPTION_NUM}.{OPTION}')                          # 보기의 번호와 보기 내용을 출력

                    answer = int(input(" 답 : "))                                # 정답 입력 받기
                    chosen_option = value['OPTIONS'][answer-1]                   # 사용자가 입력한 답변으로 인덱스와 비교해서 보기 번호 선택
                    OPTION_NUM, OPTION,OPTION_ID = chosen_option                 # DB에 전달할 내용을 추출

                    # RESPOND 테이블의 레코드 수를 학인하고 그 숫자를 반환하도록 설정
                    sql = "SELECT COUNT(RESPOND_ID) FROM RESPOND"
                    cursor.execute(sql)
                    respond_number = cursor.fetchall()[0][0]
                    # 문제에 대해 답변한 내용과 RESPOND 테이블에 필요한 내용들과, 더해서 응답 내용을 RESPOND_ID 저장할 때 프라이머리 키에 아까 받아온 숫자를 적용하도록 설정
                    sql = "INSERT INTO RESPOND (`RESPOND_ID`,`TESTS_ID`,`USER_ID`,`OPTION_ID`) VALUES ('RESPOND_%s', %s,'USER_%s',%s)"
                    cursor.execute(sql, (respond_number+1,TESTS_ID,user_number+1,OPTION_ID))
                    conn.commit()
                print("")
                keepgoing = input("다음 응시자가 있나요? (계속: c, 종료: x):") 
                print("")
                if keepgoing == "c" :
                    continue
                elif keepgoing =='x' or keepgoing == 'X': 
                    print("----------" * 5)
                    print("프로그램이 종료되었습니다.")
                    break
    finally:
        conn.close()

# solve_quiz()