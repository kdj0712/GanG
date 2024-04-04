# function 호출
import making_test_yugyeongjo, solve_test_djkim, test_scoring_yugyeongjo

# 문제 출제
path = 'toy_ERDs/quiz.txt' # 문제 출처 db 사전제공
test_list, option_count = making_test_yugyeongjo.making_test_from_file(path)

# 출제한 문제 db저장
making_test_yugyeongjo.test_db_insert(test_list, option_count)

# 저장한 문제 db 불러와서 시험 응시 + 응시 내용 db 저장
solve_test_djkim.solve_quiz()

# 저장된 응시 db 기준으로 각 응시자별 점수 표시 + 전체 응시자 평균 표시
test_scoring_yugyeongjo.scoring()
