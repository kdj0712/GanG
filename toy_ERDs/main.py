# function 호출
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

import making_test_yugyeongjo, solve_test_djkim, test_scoring_yugyeongjo

# 문제 출제
path = 'toy_ERDs/quiz.txt' # 외부 파일인 시험 문제 텍스트 파일에서 시험 문제의 내용을 추출해서 리스트화
test_list, option_count = making_test_yugyeongjo.making_test_from_file(path)

# 출제한 문제 db저장
making_test_yugyeongjo.test_db_insert(test_list,option_count,conn)
# 저장한 문제 db 불러와서 시험 응시 + 응시 내용 db 저장
solve_test_djkim.solve_quiz()
# 저장된 응시 db 기준으로 각 응시자별 점수 표시 + 전체 응시자 평균 표시
test_scoring_yugyeongjo.scoring()
# conn.close()