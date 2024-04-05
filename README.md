## 시험 문제 출제, 문제 풀이 및 점수 산정 프로그램 제작

### 프로젝트 개요
|구분|내용|
|--|--|
|기간|2024.04.02 ~ 2024.04.04|
|인원|조유경, 김덕재|
|내용|시험 문제와 보기 문항을 입력받아 DB에 저장한 다음, <br> 사용자 이름을 입력받아 사용자가 응시한 정보를 저장하여, <br> 그 정보를 기반으로 점수와 응시자 평균 점수를 출력하는 프로그램의 제작|
|담당|조유경 : 시험 문제 입력 및 저장, 응시자 별 점수 출력 및 응시자 전체 평균 산출 <br> 김덕재 : 시험 문제 출력 및 응시 정보 저장, 영상 제작|
|결과영상|[Youtube Link](https://www.youtube.com/watch?v=RyOrkZEqAyM&ab_channel=DeokJaeKim)|

### 사용 툴

### 프로젝트 결과물

## Setting
<details>ad
<summary>Click!</summary>

#### Main package
- java:17
- mysql:8

#### CLI with Dockerfile and compose.xml : duration 150.4s
```
# --project-name is docker container name

Docker installation command copied
~$ docker-compose --project-name python__mysql up -d --build

Docker reinstallation command copied
~$ docker-compose --project-name python__mysql build --no-cache
~$ docker-compose --project-name python__mysql up -d
```
#### samples
- [samples/python_mysql.py](./samples/python_mysql.py)

#### database infors
+ user='cocolabhub',
+ password='cocolabhub',
+ db='python_mysql'
</details>