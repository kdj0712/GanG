
# 외부 파일인 시험 문제 텍스트 파일에서 시험 문제의 내용을 추출해서 리스트화
def making_test_from_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        lines = file.readlines()  # 시험 문제 텍스트 파일의 모든 줄을 읽어 리스트로 저장
        
    test_list = []
    current_line = 0  # 현재 처리 중인 줄의 인덱스

    question_count = int(lines[current_line].rstrip('\n'))  # 첫 번째 줄에서 출제할 문제 수를 읽음
    current_line += 1
    option_count = int(lines[current_line].rstrip('\n'))  # 두 번째 줄에서 문항 당 보기 수를 읽음
    current_line += 1

    for i in range(question_count):  # 입력 된 출제 문항 수 만큼 반복문 동작
        dict_testlist = {"question": None, "option": [], "correct": [], "point": None} # 문제 딕셔너리의 구조 선언
        
        # 문제 읽기
        dict_testlist["question"] = lines[current_line].rstrip('\n') or None
        current_line += 1
        
        # 보기 및 정답 여부 읽기
        for j in range(option_count): # 입력 된 문항 당 보기 수 만큼 반복문 동작
            option_line = lines[current_line].rstrip('\n')
            dict_testlist["option"].append(option_line or None)   # 보기를 옵션 리스트로 전송
            current_line += 1

            correct_line = lines[current_line].rstrip('\n')
            dict_testlist["correct"].append(correct_line if correct_line == 'O' else None) # 정답 여부에 대한 내용이 채워진 값이 있는 경우와 아닌 경우를 구분하여 정답 리스트에 전송
            current_line += 1
        
        # 배점 읽기
        dict_testlist["point"] = int(lines[current_line].rstrip('\n')) # 입력된 배점을 숫자형 정수로 변환한 뒤 점수 리스트에 전송
        current_line += 1
        
        test_list.append(dict_testlist) # 모든 내용을 점수 리스트에 전송
    
    return test_list, option_count

path = 'toy_ERDs/quiz.txt'
test_list, option_count = making_test_from_file(path)

# def making_test():
#     test_list = []
#     question_count = int(input("출제할 문제 수를 입력해주세요 : "))
#     option_count = int(input("문항 당 보기 수를 입력해주세요 : "))
#     for i in range(question_count):
#         dict_testlist = {}
#         dict_testlist["question"] = input(f"문항 {i+1} : ")
#         dict_testlist["option"] =[]
#         dict_testlist["correct"] = []
#         for j in range(option_count):
#             dict_testlist["option"].append(input(f"보기 {j+1}: "))
#             dict_testlist["correct"].append(input(f"정답 {j+1}:"))
#         dict_testlist["point"] = int(input("배점 :"))
#         test_list.append(dict_testlist)
#     return test_list, option_count

# test_list, option_count = making_test()

# 출제받은 문제 DB에 넣기
def test_db_insert(test_list, option_count): # 앞서 실행 된 making_test_from_file 펑션의 리턴값인 문제 리스트와, 문항 당 보기 수를 매개변수로 동작 선언
    import pymysql
    # 데이터베이스 연결 설정
    conn = pymysql.connect(
    host='192.168.10.236',  # 컨테이너 이름 또는 IP
    port = 3307,
    user='cocolabhub',
    password='cocolabhub',
    db='python_mysql',  # 데이터베이스 이름
    charset='utf8mb4'   
    )
    try:
        with conn.cursor() as cursor:
            # test시도를 위한 delete
            sql = "DELETE FROM RESPOND WHERE RESPOND_ID IS NOT NULL"
            cursor.execute(sql)
            conn.commit()
            sql = "DELETE FROM `OPTION` WHERE OPTION_ID IS NOT NULL"
            cursor.execute(sql)
            conn.commit()
            sql = "DELETE FROM TESTS WHERE TESTS_ID IS NOT NULL"
            cursor.execute(sql)
            conn.commit()
            sql = "DELETE FROM `USER` WHERE USER_ID IS NOT NULL"
            cursor.execute(sql)
            conn.commit()

            # 매개 변수로 받은 시험 문제와 보기의 리스트를 DB에 입력하는 반복문 실행
            for i in range(len(test_list)): # 리스트 내 딕셔너리 갯수 만큼 반복문 실행
                sql = "INSERT INTO TESTS (`TESTS_ID`, `QUESTIONS`, `POINT`, `QUESTION_NUM`) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (f"TEST_{i+1}", test_list[i]["question"], test_list[i]["point"], i+1))
                conn.commit()
                for j in range(option_count):  # 매개 변수로 받은 보기 문항 갯수 만큼 반복문 실행
                    # PK_OPTION_ID 이전 DB 갯수 파악해서 다음 숫자부터 마킹해주기
                    sql = "SELECT COUNT(OPTION_ID) FROM `OPTION`"
                    cursor.execute(sql)
                    option_number = cursor.fetchall()
                    option_number = int(option_number[0][0])
                    
                    sql = "INSERT INTO `OPTION` (`OPTION_ID`, `TESTS_ID`, `OPTION`, `CORRECT`, `OPTION_NUM`) VALUES ('OPTION_%s', %s, %s, %s, %s)"
                    cursor.execute(sql, (option_number+1, f"TEST_{i+1}", test_list[i]["option"][j], test_list[i]["correct"][j], j+1))
                    conn.commit()               
    finally:
        conn.close()       
        
    return
test_db_insert(test_list, option_count)
    