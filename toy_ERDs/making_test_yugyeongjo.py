import pymysql

# 데이터베이스 연결 설정
conn = pymysql.connect(
    host='192.168.10.236',  # 컨테이너 이름 또는 IP
    port = 3306,
    user='cocolabhub',
    password='cocolabhub',
    db='python_mysql',  # 데이터베이스 이름
    charset='utf8mb4'
)

def making_test():
    test_list = []
    question_count = int(input("출제할 문제 수를 입력해주세요 : "))
    option_count = int(input("문항 당 보기 수를 입력해주세요 : "))
    for i in range(question_count):
        dict_testlist = {}
        dict_testlist["question"] = input(f"문항 {i+1} : ")
        dict_testlist["option"] =[]
        for j in range(option_count):
            dict_testlist["option"].append(input(f"보기 {j+1}: "))
        dict_testlist["right"] = input("정답 :")
        dict_testlist["point"] = input("배점 :")
        test_list.append(dict_testlist)
    return test_list

making_test()

with conn.cursor() as cursor:
    # test시도를 위한 delete
    sql = "DELETE FROM TESTS WHERE pk_id=%s"
    cursor.execute(sql, (1,))
    conn.commit()
    
    sql = "INSERT INTO TESTS (pk_id,column1, column2) VALUES (%s, %s, %s)"
    cursor.execute(sql, (1, 'value1', 'value2'))
    conn.commit()