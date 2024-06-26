-- 문제 테이블과 보기 문항 테이블의 내용을 가져와 문제 가져오기
SELECT 'TESTS_ID','OPTION_ID',QUESTIONS,`POINT`,QUESTION_NUM,`OPTION`,OPTION_NUM
FROM TESTS INNER JOIN `OPTION` 
ON TESTS.TESTS_ID = `OPTION`.TESTS_ID
ORDER BY TESTS.TESTS_ID,OPTION_ID;

-- 위의 구문에서 OPTION.OPTION_ID의 숫자를 기준으로 정렬하여 값을 가지고 오도록 조건을 추가
-- # VARCHAR 타입 텍스트의 정렬을 가능하게 할 수 있도록 조건을 추가
SELECT TESTS.TESTS_ID, `OPTION`.OPTION_ID, QUESTIONS, QUESTION_NUM, `OPTION`, OPTION_NUM 
FROM TESTS 
INNER JOIN `OPTION` ON TESTS.TESTS_ID = `OPTION`.TESTS_ID 
ORDER BY TESTS.TESTS_ID, 
CAST(SUBSTRING_INDEX(`OPTION`.OPTION_ID, '_', -1) AS UNSIGNED), `OPTION`.OPTION_ID
;                            