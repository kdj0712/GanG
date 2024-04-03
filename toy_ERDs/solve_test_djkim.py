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
    # cursorclass = DictCursor
)
# TESTS = 문제 테이블(`TESTS_ID`,`QUESTIONS`,`RIGHT`,`POINT`,`QUESTION_NUM`)
# OPTION = 보기 테이블(	`OPTION_ID`,`TESTS_ID`,`OPTION`,`CORRECT`,`OPTION_NUM`)
# USER = 응시자 테이블(`USER_ID`,`USER`)
# RESPOND = 응시 테이블(`RESPOND_ID`,`TESTS_ID`,`USER_ID`,`OPTION_ID`)
def solve_quiz():
    try:
        with conn.cursor() as cursor:
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

                sql = "SELECT TESTS.TESTS_ID, `OPTION`.OPTION_ID, QUESTIONS, `POINT`, QUESTION_NUM, `OPTION`, OPTION_NUM FROM TESTS INNER JOIN `OPTION` ON TESTS.TESTS_ID = `OPTION`.TESTS_ID ORDER BY TESTS.TESTS_ID,`OPTION`.OPTION_ID"
                cursor.execute(sql)
                quizs = cursor.fetchall()

                # 퀴즈 데이터를 질문 기준으로 그룹화
                quiz_dict = {}
                for row in quizs:
                    TESTS_ID, OPTION_ID, QUESTIONS, POINT, QUESTION_NUM, OPTION, OPTION_NUM = row
                    key = (TESTS_ID, QUESTION_NUM)  # 질문을 구분하는 키
                    if key not in quiz_dict:
                        quiz_dict[key] = {
                            'QUESTION_NUM': QUESTION_NUM,
                            'QUESTIONS': QUESTIONS,
                            'OPTIONS': []
                        }
                    quiz_dict[key]['OPTIONS'].append((OPTION_NUM, OPTION))

                # 질문과 옵션 출력
                previous_test_id = None
                for key, value in quiz_dict.items():
                    TESTS_ID, QUESTION_NUM = key
                    if TESTS_ID != previous_test_id:
                        print(f"{value['QUESTION_NUM']}. {value['QUESTIONS']}")
                        previous_test_id = TESTS_ID
                    for option in sorted(value['OPTIONS'], key=lambda x: x[0]):  # 옵션 번호 순으로 정렬
                        OPTION_NUM, OPTION = option
                        print(f'{OPTION_NUM}.{OPTION}')

                    answer = int(input(" 답 : "))
                    
                    chosen_option = value['OPTIONS'][answer-1]  # 사용자가 입력한 답변으로 옵션 선택
                    OPTION_NUM, OPTION = chosen_option

                    sql = "SELECT COUNT(RESPOND_ID) FROM RESPOND"
                    cursor.execute(sql)
                    respond_number = cursor.fetchall()
                    respond_number = int(respond_number[0][0])
                            # Create
                    sql = "INSERT INTO RESPOND (`RESPOND_ID`,`TESTS_ID`,`USER_ID`,`OPTION_ID`) VALUES ('RESPOND_%s', %s,'USER_%s',%s)"
                    cursor.execute(sql, (respond_number+1,TESTS_ID,user_number+1,OPTION_ID))
conn.commit()













                # cursor.execute(sql)
                # quizs = cursor.fetchall()
                # max_key = max(quizs, key=lambda k:k[6])[6]

                # previous_test_id = None
                # for row in quizs:
                #     TESTS_ID,OPTION_ID,QUESTIONS,POINT,QUESTION_NUM,OPTION,OPTION_NUM  = row
                #     if TESTS_ID != previous_test_id:
                #         print(f"{QUESTION_NUM}. {QUESTIONS}")
                #         previous_test_id = TESTS_ID
                #         for x in range(int(max_key)):
                #             print(f'{OPTION_NUM}.{OPTION}')        

                #     answer = int(input(" 답 : "))                               # 답의 입력값은 answer라는 변수로 지정한다.
                #     # Answer_input.insert_one( {'User_id' : names_id , 'Questions_id' : questions['_id'] ,  'Answers' : answer}) 


                print("")
                keepgoing = input("다음 응시자가 있나요? (계속: c, 종료: x):")      # "다음 응시자가 있나요?" (계속: c, 종료: x)
                print("")
                if keepgoing == "c" :
                    continue
                elif keepgoing =='x' : 
                    print("----------" * 5)
                    print("프로그램이 종료되었습니다.")
                    break
    finally:
        conn.close()

solve_quiz()