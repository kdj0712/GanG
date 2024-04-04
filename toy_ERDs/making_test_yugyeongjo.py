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
        dict_testlist["correct"] = []
        for j in range(option_count):
            dict_testlist["option"].append(input(f"보기 {j+1}: "))
            dict_testlist["correct"].append(input(f"정답 {j+1}:"))
        dict_testlist["point"] = int(input("배점 :"))
        test_list.append(dict_testlist)
    return test_list, option_count

test_list, option_count = making_test()

# 출제받은 문제 DB에 넣기
<<<<<<< HEAD
with conn.cursor() as cursor:
    # test시도를 위한 delete
    sql = "DELETE FROM TESTS WHERE TESTS_ID IS NOT NULL"
    cursor.execute(sql)
    conn.commit()
    
    for i in range(len(test_list)):
        sql = "INSERT INTO TESTS (`TESTS_ID`, `QUESTIONS`, `POINT`, `QUESTION_NUM`) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (f"TEST_{i+1}", test_list[i]["question"], test_list[i]["point"], i+1))
        conn.commit()
        for j in range(option_count):
            sql = "INSERT INTO `OPTION` (`OPTION_ID`, `TESTS_ID`, `OPTION`, `CORRECT`, `OPTION_NUM`) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (f"OPTION_{j+1}", f"TEST_{i+1}", test_list[i]["option"][j], test_list[i]["correct"][j], j+1))
            conn.commit()            
=======
def test_db_insert(test_list, option_count):
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
            sql = "DELETE FROM USER WHERE USER_ID IS NOT NULL"
            cursor.execute(sql)
            conn.commit()
            
            sql = "SELECT COUNT(OPTION_ID) FROM `OPTION`"
            cursor.execute(sql)
            option_number = cursor.fetchall()
            option_number = int(option_number[0][0])
            
            for i in range(len(test_list)):
                sql = "INSERT INTO TESTS (`TESTS_ID`, `QUESTIONS`, `POINT`, `QUESTION_NUM`) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (f"TEST_{i+1}", test_list[i]["question"], test_list[i]["point"], i+1))
                conn.commit()
                for j in range(option_count):
                    sql = "INSERT INTO `OPTION` (`OPTION_ID`, `TESTS_ID`, `OPTION`, `CORRECT`, `OPTION_NUM`) VALUES ('OPTION_%s', %s, %s, %s, %s)"
                    cursor.execute(sql, (option_number, f"TEST_{i+1}", test_list[i]["option"][j], test_list[i]["correct"][j], j+1))
                    conn.commit()               
    finally:
        conn.close()       
        
    return
test_db_insert(test_list, option_count)
>>>>>>> 0f0358b376526b6c7b644434d427c2273cdb36b0
    