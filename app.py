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
import socket
import json

app = Flask(__name__) # Flask 애플리케이션 / __name__에 모듈명이 들어감

## 대화형 AI(챗봇) 엔진 구현 구분

# 엔진 서버와 연결하여 질문을 보내고, 반한된 답변을 받아오는 함수
def get_answer_from_engine(bottype, query): # query = 사용자가 입력한 질문, bottype = 챗봇의 종류
    host = "127.0.0.1" # 대화형 AI(챗봇) 엔진 서버 IP 지정
    port = 5050 # 대화형 AI(챗봇) 엔진 port = Homepage port

    # 대화형 AI(챗봇) 엔진 서버 연결
    # 소켓 = 프로세스 간 통신을 가능하게 해주는 운영체제의 네트워크 통신용 API,
    #   이를 사용하여 서로 다른 컴퓨터끼리 데이터를 주고 받을 수 있음.
    mySocket = socket.socket() # 소켓 객체 생성.
    mySocket.connect((host, port)) # 소켓과 서버의 연결.

    # 대화형 AI(챗봇) 엔진 질의 요청
    # JSON = 경량 데이터 교환 형식, 주로 웹 API에서 데이터를 주고 받을 때 사용
    json_data = {
        "Query" : query, # 입력받은 질의 문자열을 저장
        "BotType" : bottype # 입력받은 챗봇 타입을 저장
    }
    message = json.dumps(json_data) #json_data를 json.dumps()를 이용하여 json 문자열로 저장.
    mySocket.send(message.encode())
    # mySocket.send() 메서드를 사용하여 message 변수에 저장된 데이터를 소켓을 이용해 서버로 전송,
    # 문자열을 전송하기 위해 encode() 함수로 문자열을 바이트로 변환한다.
    

    # 대화형 AI(챗봇) 엔진 답변 출력 부분
    data = mySocket.recv(2048).decode() # 서버로부터 받은 데이터(json 형식)를 받기 위해, recv()함수를 사용하여 데이터를 받아옴
    ret_data = json.loads(data) # json 형식으로 된 문자열을 파이썬에서 사용하기 쉬운 딕셔너리 형식으로 변환

    mySocket.close() # 대화형 AI(챗봇) 엔진 서버 연결 소켓 닫기

    return ret_data # 딕셔너리 데이터 반환.

# Test sentence
@app.route('/') # 주소를 치고 갔을 경우 Test 하기 위한 부분 Home에서 
def hello_world():
    return "Hello, is this Worrrkkkrkrkrkrkrk?" # 이 문구가 출력이 되어야 함

# "/query/<bot_type>" 주소로 POST 요청이 들어오면 query 함수가 호출됨.
@app.route("/query/<bot_type>", methods = ["POST"])
def query(bot_type):
    body = request.get_json() # 바디에 포함된 json 형식의 데이터를 파이썬 객체로 디코딩하여,
    # 결과를 body 변수에 저장한다.

    try:
        if bot_type == "NORMAL": # 정의된 답변 이라면 답변이라면
            # 일반 질의 응답 API
            # get_answer_from_engine 함수를 호출하여 챗봇 엔진으로부터 응답을 받아와서
            ret = get_answer_from_engine(bottype = bot_type, query = body["query"])
            return jsonify(ret) # 받아온 데이터를 json 형식으로 반환한다.
        
        else: # 정의 되지 않은 bot type 라면 404 Eror 발생
            abort(404) # 에러 발생

    except Exception as ex:
        # 정의된 bot type 중 오류 발생시 500 Error 발생
        abort(500) # 에러 발생


## 실행 부분


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5022)
    # host = 서버가 바인딩할 IP 주소 지정, port = 앱이 실핼될 포트 번호를 지정.
    # 0.0.0.0은 현재 시스템에서 사용 가능한 모든 IP 주소를 나타낸다.
    print("Hello there") # 앱 실행을 확인하기 위한 간단한 문구.

@app.route("/hello", methods=["GET"]) # hello 경로로 이동시 index() 호출
def index():
    try: 
        # 안내 메세지를 실행한다.
        message = "안녕하세요, 조선대학교 챗봇입니다.\n" \
        "현재 다음 기능을 제공하고 있습니다.\n" \
        "1. 번호 안내 2. 장소 안내\n" \
        "사용예시 - (학과/트랙/기관명)번호 알려줘, (건물 이름)위치 알려줘\n)" \
        "사용예시2 - 컴퓨터공학부 번호 알려줘, 상담실 위치 알려줘\n" \
        "원하시는 업데이트를 적어주시면 빠르게 업데이트 하겠습니다."

        json_data = {
            "message" : message # "message"라는 키로 문자열을 값으로 갖는 json 데이터를 만듦.
        }
        message = json.dumps(json_data, ensure_ascii = False) #json.dumps() 함수로 문자열로 반환한다.
        #ensure_ascii = False : 한글 문자열을 그대로 유지하기 위해서
        message = json.loads(message) # json.loads() 함수를 이용해서 문자열을 json 형식의 데이터로 변환한다.

        return jsonify(message) # json 형식의 데이터(message)를 HTTP 응답으로 반환한다.

    except Exception as ex:
        abort(500) # 오류 발생시 500 Error 발생

@app.route("/query/<bot_type>", methods = ["GET", "POST"])
def query(bot_type):
    body = request.get_json() # POST 요청시 json data를 가져오는 함수.
    try:
        if bot_type == "NORMAL": # 정상적인 봇타입이라면
        #  일반 질의응답 API
            # ret 변수에 함수를 이용하여 body["query"]에 대한 답변을 반환한다.
            ret = get_answer_from_engine(bottype = bot_type, query = body["query"])

            return jsonify(ret) # json 형식의 데이터(message)를 HTTP 응답으로 반환한다.
        
        elif bot_type == "QUICK": # QUICK(미리 정의된 대화 주제나 키워드) 이라면
            # 해당 파일 경로로 들어가서 UTF-8 인코딩으로 디코딩하여 문자열을 읽어옴.
            with open("/home/chosun/python_chatbot/Chatbot4Univ/chatbot_api/static/json/quick_reply.json", "r", encoding = "utf-8") as json_file:
                jdata = json.load(json_file) # json.loads() 함수를 이용해서 문자열을 json 형식의 데이터로 변환한다.
                
                return jdata
            
        else:
            abort(404) # 정의되지 않은 bot type인 경우 404 Error

    except Exception as ex:
        abort(500) # 오류 발생시 500 Error 발생