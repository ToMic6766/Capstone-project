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

@app.route("/hello", methods=["GET"])
def index():
    try:
        message = "안녕하세요, 조선대학교 챗봇입니다.\n" \
        "현재 다음 기능을 제공하고 있습니다.\n" \
        "1. 번호 안내 2. 장소 안내\n" \
        "사용예시 - (학과/트랙/기관명)번호 알려줘, (건물 이름)위치 알려줘\n)" \
        "사용예시2 - 컴퓨터공학부 번호 알려줘, 상담실 위치 알려줘\n" \
        "원하시는 업데이트를 적어주시면 빠르게 업데이트 하겠습니다."

        json_data = {
            "message" : message
        }
        message = json.dumps(json_data, ensure_ascii = False)
        message = json.loads(message)

        return jsonify(message)

    except Exception as ex:
        abort(500) # 오류 발생시 500 Error 발생

@app.route("/query/<bot_type>", methods = ["GET", "POST"])
def query(bot_type):
    body = request.get_json()
    try:
        if bot_type == "NORMAL":
        #  일반 질의응답 API
            ret = get_answer_from_engine(bottype = bot_type, query = body["query"])

            return jsonify(ret)
        
        elif bot_type == "QUICK":
            with open("/home/hoseo420/python_chatbot/Chatbot4Univ/chatbot_api/static/json/quick_reply.json", "r", encoding = "utf-8") as json_file:
                jdata = json.load(json_file)
                
                return jdata
            
        else:
            abort(404) # 정의되지 않은 bot type인 경우 404 Error

    except Exception as ex:
        abort(500) # 오류 발생시 500 Error 발생
    















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
