from flask import Flask, render_template,session,redirect,url_for
from api import api_bp
import os

app = Flask(__name__)
app.register_blueprint(api_bp)

#session 사용을 위한 시크릿키
app.config["SECRET_KEY"]="sdjisnoafsada" 

#시작하면 로그인 화면 출력
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/boardlist')
def boardlist():
    #세션이 있는 경우 (로그인이 된 경우) => 게시판으로 
    if session:
        return render_template('boardlist.html')
    #그렇지 않은 경우 => 로그인 페이지로 이동
    else:
        return {"message":"에러에러"}


if __name__ == '__main__':
    app.run()
    