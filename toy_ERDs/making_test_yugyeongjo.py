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