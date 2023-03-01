from flask import Flask, render_template, session, redirect, url_for
from api import api_bp

app = Flask(__name__)
app.register_blueprint(api_bp)

# session 사용을 위한 시크릿키
app.config["SECRET_KEY"] = "sdjisnoafsada"

# 시작하면 로그인 화면 출력


@app.route('/')
def login():
    if session:
        return redirect(url_for('boardlist'))
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    return render_template('logout.html')


@app.route('/boardlist')
def boardlist():
    # 세션이 있는 경우 (로그인이 된 경우) => 게시판으로
    if session:
        return render_template('boardlist.html')
    # 그렇지 않은 경우 => 로그인 페이지로 이동
    else:
        return {"message": "에러에러"}


@app.route('/userdetail')
def userdetail():
    return render_template('userdetail.html')


@app.route('/user/<string:id>')
def modifyUser(id):
    return render_template('modifyuser.html', id=id)


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/content/<int:id>')
def contentList(id):
    return render_template('contentlist.html', id=id)


@app.route('/content/<int:boardid>/<int:contentId>')
def content(boardid, contentId):
    return render_template('content.html', boardid=boardid, contentId=contentId)


@app.route('/content/1/<int:boardid>/<int:contentId>')
def modifyContent(boardid, contentId):
    return render_template('modify.html', boardid=boardid, contentId=contentId)


@app.route('/password/1')
def findpassword():
    return render_template('findpassword.html')


@app.route('/password/2/<string:id>')
def changepassword(id):
    return render_template('changepassword.html', id=id)


if __name__ == '__main__':
    app.run()
