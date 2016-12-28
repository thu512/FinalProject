# FinalProject
python flask를 이용한 채팅 웹 , opencv기반 얼굴인식 로그인 서비스
WebServiceComputing

1. 환경

1.1 Anaconda 2.7
https://www.continuum.io/downloads#windows

1.2 OpenCV 2.4.11
Anaconda Prompt에서 실행
conda install -c menpo opencv=2.4.11

1.3 Pycharm 설치
https://www.jetbrains.com/pycharm-edu/download/

1.4 인터프리터 확인
Pycharm을 이용하여 프로젝트를 생성할 때 인터프리터를 확인하기

2. FaceDetection-ex01
로컬에 있는 이미지(lena.png)에서 얼굴 검출 후 보여주기

3. FaceDetection-ex02
Flask 기반 웹 서버에서 로컬에 있는 이미지(lena.png) 얼굴 검출 후 보여주기

4. FaceDetection-ex03
Flask 기반 웹 서버에서 파일 업로드를 이용하여 얼굴 검출 후 보여주기

5. FaceRecognition-ex01
얼굴 이미지 학습(step01.py) 후 얼굴 인식 테스트(step02.py)
eigenfaces
fisherfaces
lbph

6. FaceRecognition-ex02
얼굴 이미지 학습(train.py)
웹에서 얼굴 인식 테스트(app.py)
eigenfaces
fisherfaces
lbph

7. FaceRecognition-ex03
얼굴 이미지 학습(train.py)
웹에서 얼굴 인식 테스트(app.py)
인식한 이미지를 보여주기

8. FaceRecognition-ex04

8.1 얼굴 이미지 검출(step01.py)
얼굴 검출
얼굴 자르기
얼굴 저장

8.2 얼굴 이미지 학습(step02.py)
eigenfaces
fisherfaces
lbph

8.3 학습한 데이터 검증(step03.py)
eigenfaces
fisherfaces
lbph
