#python3 -m venv(여기는 가상환경 명령어?) venv(여기는 Dir 이름)로 가상 환경 구축
#source venv/bin/activate ㄱㅏ상 환경 설치된 것을 활성화(update) 시킴
#pip install flask flask 설치

#flask 오류 발생시 pip show flask 검색후
#comm+shift+p 눌러서 파이썬 버전 변경

#VSCode에서 flask-snippets 설치 필요

#환경변수 설정도 해야함.
#export FLASK_APP=My_Flask.py
#?export FLASK_APP=/Users/kim-young-woong/Desktop/Capstone/Git_dir/My_Flask.py
#export FLASK_ENV=development



from flask import Flask, request, jsonify, abort, render_template
# from flask import Flask
import socket
import json

app = Flask(__name__) # Flask 애플리케이션 / __name__에 모듈명이 들어감

# 대화형 AI(챗봇) 엔진 구현 구분
def get_answer_from_engine(bottype, query):
    host = "127.0.0.1" # 대화형 AI(챗봇) 엔진 서버 IP
    port = 5050 # 대화형 AI(챗봇) 엔진 port = Homepage port

    # 대화형 AI(챗봇) 엔진 서버 연결
    mySocket = socket.socket()
    mySocket.connect((host, port))

    # 대화형 AI(챗봇) 엔진 질의 요청
    json_data = {
        "Query" : query,
        "BotType" : bottype
    }
    message = json.dumps(json_data)
    mySocket.send(message.encode())

    # 대화형 AI(챗봇) 엔진 답변 출력 부분
    data = mySocket.recv(2048).decode()
    ret_data = json.loads(data)

    mySocket.close() # 대화형 AI(챗봇) 엔진 서버 연결 소켓 닫기

    return ret_data

# Test sentence
@app.route('/') # 주소를 치고 갔을 경우 Test 하기 위한 부분 Home에서 
def hello_world():
    return "Hello, Is this working?" # 이 문구가 출력이 되어야 함


@app.route("/query/<bot_type>", methods = ["POST"])
def query(bot_type):
    body = request.get_json()

    try:
        if bot_type == "NORMAL": # 정의된 답변 이라면 답변이라면
            # 일반 질의 응답 API
            ret = get_answer_from_engine(bottype = bot_type, query = body["query"]) # 
            return jsonify(ret)
        
        else: # 정의 되지 않은 bot type 라면 404 Eror 발생
            abort(404)

    except Exception as ex:
        # 정의된 bot type 중 오류 발생시 500 Error 발생
        abort(500)

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5022)
    print("Hello there")





# app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'hello, is this working?'

# if __name__ == '__main__':
#     app.run('0.0.0.0', port=5050, debug=True)

#export FLASK_APP=My_Flask.py
#?export FLASK_APP=/Users/kim-young-woong/Desktop/Capstone/Git_dir/My_Flask.py
#export FLASK_ENV=development
# from flask import Flask

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return 'Hello, World!'

# from flask import Flask

# app = Flask(__name__)

# @app.route('/')
# def home():
#     return 'This is home!'

# if __name__ == '__main__':
#     app.run('0.0.0.0', port=5050, debug=True)
