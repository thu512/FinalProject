#-*- coding: utf-8 -*-
import sys
import os
import numpy as np
import cv2
from flask import Flask, request, jsonify, render_template
from werkzeug import secure_filename
from flask_socketio import SocketIO, emit, send
from datetime import datetime

reload(sys)
sys.setdefaultencoding('utf-8')
app = Flask(__name__)
app.config['DEBUG']=True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
engineio_logger=True

#아이디 중복체크
def idcheck(user_id):
    for root,dirs,files in os.walk("userlist"):
        for file in files:
            if user_id == file:
                return True
    return False

#id/pw 로그인
@app.route("/auth", methods=["GET", "POST"])
def auth():
    if request.method == 'POST':
        user_id = request.form["id"]
        user_pw = request.form["pw"]
        if user_id=="":
            return jsonify(id=user_id, pw=user_pw, status="id_blank")
        if user_pw=="":
            return jsonify(id=user_id, pw=user_pw, status="pw_blank")

        #로그인 시도한 아이디를 userlist에 저장된 아이디인지 확인
        if idcheck(user_id):
            #존재하는 아이디이면 내부파일에 저장된 비밀번호와 일치하는지 확인
            f=open("userlist\\"+user_id,'r')
            secure_pw = f.readline()
            if user_pw == secure_pw:
                return jsonify(id=user_id, pw=user_pw, status="yes")
            else:
                return jsonify(id=user_id, pw=user_pw, status="no_pw")
        else:
            return jsonify(id=user_id, pw=user_pw, status="no_id")
    return "아이디와 비밀번호를 post 방식으로 전송해주세요."


#얼굴이미지
face_dir="img"
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


#로그인시 사용한 이미지 임시저장 경로 - 로그아웃시 자동 삭제
app.config['loginTmp'] = "C:\\Users\\Changjoo\\PycharmProjects\\FinalProject\\static\\loginTmp"


#이미지를 통한 로그인
@app.route("/img", methods=["GET", "POST"])
def img_login():
    names = {}
    key = 0
    for (subdir, dirs, files) in os.walk(face_dir):
        for subdir in dirs:
            print(key, "=>", subdir)
            names[key] = subdir
            key += 1
    if request.method == 'POST':
        id = request.form['img_id']
        file = request.files['img']
        if id == "":
            return jsonify(id=id, status="blank_id")
        if idcheck(id):
            filename = secure_filename(id+'.jpg')
            file.save(os.path.join(app.config['loginTmp'], filename))

            # grayscale로 이미지 읽어오기
            img_original = cv2.imread(os.path.join(app.config['loginTmp'], filename), 0)
            # 얼굴검출
            faces = face_cascade.detectMultiScale(img_original, 1.3, 5)
            # 검출된 얼굴이 하나 일때
            if len(faces) == 1:
                # 검출된얼굴에 파란색 테두리
                for (x, y, w, h) in faces:
                    cv2.rectangle(img_original, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # 얼굴부분만 자르기
                img_crop = img_original[y:y + h, x:x + w]
                # 리사이징
                dim = (128, 128)

                img_resize = cv2.resize(img_crop, dim)
            else:
                return jsonify(id=id, status="no_face")
            model_eigenface = cv2.createEigenFaceRecognizer()
            model_eigenface.load("eigenface.xml")
            prediction_eigenface = model_eigenface.predict(img_resize)
            print(names[prediction_eigenface[0]])
            if names[prediction_eigenface[0]] == id:
                return jsonify(id=id, status="yes")
            else:
                os.remove(os.path.join(app.config['loginTmp'], id + '.jpg'))
                return jsonify(id=id, status="no")
        else:
            return jsonify(id=id, status="no_id")

#이미지 로그인시 아이디 체크
@app.route("/check", methods=['GET', 'POST'])
def check():
    if request.method == 'POST':
        id = request.form['id']
        if idcheck(id):
            return jsonify(id=id, status="no")
        else:
            return jsonify(id=id, status="yes")


#회원가입 시 사용자 내역 저장
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        files = request.files.getlist('file[]')
        id = request.form['id']
        pw = request.form['pw']
        #회원가입시 아이디명으로 파일생성 파일 내용은 비밀번호
        f = open("userlist\\"+id, 'w')
        f.write(pw);
        f.close()
        if files:
        #회원가입 폼에서 사진을 업로드하면 이름별로 폴더생성후 저장

            if not os.path.isdir("img\\" + id):
                os.mkdir("img\\" + id)

            #회원가입 사진 저장 경로
            app.config['UPLOAD_FOLDER'] = "C:\\Users\\Changjoo\\PycharmProjects\\FinalProject\\img\\"+id


            for file in files:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #저장한 사진들 인식용으로 변환
        for (subdir, dirs, files) in os.walk(face_dir):
            for subdir in dirs:
                # 디렉터리가 존재하지 않으면 생성하기
                if not os.path.isdir("crop\\" + subdir):
                    os.mkdir("crop\\" + subdir)
                img_path = os.path.join(face_dir, subdir)
                for fn in os.listdir(img_path):
                    # 이미지 파일
                    img_file = img_path + "\\" + fn
                    # grayscale로 이미지 읽어오기
                    img_original = cv2.imread(img_file, 0)
                    # 얼굴검출
                    faces = face_cascade.detectMultiScale(img_original, 1.3, 5)
                    # 검출된 얼굴이 하나 일때
                    if len(faces) == 1:
                        # 검출된얼굴에 파란색 테두리
                        for (x, y, w, h) in faces:
                            cv2.rectangle(img_original, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        # 얼굴부분만 자르기
                        img_crop = img_original[y:y + h, x:x + w]
                        # 리사이징
                        dim = (128, 128)
                        img_resizing = cv2.resize(img_crop, dim)
                        # 저장
                        cv2.imwrite("crop\\" + subdir + "\\" + fn, img_resizing)
        #모델 생성
        os.system("python learn.py &")
        return render_template('login.html')

    return render_template('login.html')

#로그인 성공시 채팅 창 연결
@app.route('/chat')
def chat():
    return render_template('chat.html')

# 사용자 목록
user_list = {}

# socketio 연결
@socketio.on('connect', namespace='/')
def on_connect():
    data = '[' + datetime.today().strftime('%Y-%m-%d %H:%M') + '] new client connected, socketid:' + request.sid + '\n'
    print (data)
    f = open("log.txt", 'a')
    f.write(data)
    f.close()
    emit('server, socketid', {'socketid': request.sid})


# 채팅방 퇴장
@socketio.on('client, disconnect', namespace='/')
def on_disconnect(data):
    name = user_list[request.sid]
    del user_list[data['socketid']]
    data2 = '[' + datetime.today().strftime('%Y-%m-%d %H:%M') + '] client disconnect, socketid: ' + request.sid + '\n'
    print (data2)
    f = open("log.txt", 'a')
    f.write(data2)
    f.close()
    emit('server, join chat', {'user_list': user_list}, broadcast=True)
    emit('server, disconnect', {'name': name}, broadcast=True)
    #로그인시 사용한 임시저장 사진 제거
    os.remove(os.path.join(app.config['loginTmp'], data['name']+'.jpg'))



# 채팅방 입장
@socketio.on('client, join chat', namespace='/')
def join_chat(data):
    user_list[request.sid] = data['name']
    data3 = '[' + datetime.today().strftime('%Y-%m-%d %H:%M') + '] client join chat, clientid: ' + user_list[
        request.sid] + ', socketid: ' + request.sid + '\n'
    print data3
    f = open("log.txt", 'a')
    f.write(data3)
    f.close()
    emit('server, join chat', {'user_list': user_list}, broadcast=True)
    emit('server, new client', {'name': data['name']}, broadcast=True)


# 대화 입력
@socketio.on('client, input message', namespace='/')
def join_chat12(data):
    data4 = '[' + datetime.today().strftime('%Y-%m-%d %H:%M') + '] client input message id: ' + data[
        'name'] + ', socketid: ' + request.sid + ', message: ' + data['message'] + '\n'
    print (data4)
    f = open("log.txt", 'a')
    f.write(data4)
    f.close()
    emit('server, input message', {'name': data['name'], 'message': data['message']}, broadcast=True)


if __name__ == '__main__':
    socketio.run(app)
