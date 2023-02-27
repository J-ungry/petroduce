from crypt import methods
from unittest import expectedFailure, result
from flask import Blueprint, request,session,redirect,url_for,render_template, jsonify
from flask_restful import Resource, Api
import pymysql.cursors
import cryptography

from db import connect_db,query_db

api_bp = Blueprint('api', __name__,url_prefix="/api")
api = Api(api_bp)

#connect sql
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='duffufK123!',
    db='petroduce',
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor
)


#로그인 API
@api_bp.route('/login',methods=['POST'])
def login():
    print("Login work")
    id= request.form.get('id')
    password = request.form.get('password')

    sql = "SELECT * FROM users WHERE id=%s AND password=%s"
    result = query_db(sql,(id,password))

    if result:
        name = result[0]['name']
        session['id'] = id
        session['name'] = name
        return redirect(url_for('boardlist'))
    else:
        return redirect(url_for('login'))

#회원가입 API
@api_bp.route('/user',methods=['POST'])
def signup():
    print("signup Work")
    id = request.form.get('id')
    password = request.form.get('password')
    name = request.form.get('name')
    
    sql = "INSERT INTO users (id,password,name) Values (%s,%s,%s);"
    
    try:
        query_db(sql,(id,password,name))
        return redirect(url_for('login'))
    except:
        return {"message":"insert error"}

#회원 정보 불러오기 API
@api_bp.route('/user/<string:id>',methods=['POST'])
def getUserInfo(id):
    print(id)
    sql = "SELECT * FROM users WHERE id=%s"
    try:
        result = query_db(sql,(id))
        id = result[0]['id']
        password = result[0]['password']
        name = result[0]['name']

        return render_template('usermodify.html',id=id,password=password,name=name)
    except:
        return {"message":"select Error"}

# 회원 정보 수정 API
@api_bp.route('/user/modify/<string:id>',methods=['PUT'])
def usermodify(id):
    print("work")
    data = request.get_json()

    nowid=id
    newid=data.get('newid')
    newpw=data['newpw']
    newname=data['newname']


    print(newid,newpw,newname,newid)
    sql = "UPDATE users SET id=%s, password=%s, name=%s where id=%s"

    try:
        print("result: ",newid,newpw,newname)
        query_db(sql,(newid,newpw,newname,nowid))

        #session 수정해주기
        session['id'] = newid
        session['name'] =newname
        return session

    except:
        return {"message":"update Error"}


            


#게시판 호출 API
@api_bp.route('/board',methods=["GET"])
def boards():
    sql = "SELECT * FROM board"
    try:
        result = query_db(sql)
        return result
    except:
        return {"message":"select Error"}

#게시판 추가 API
@api_bp.route('/board',methods=["POST"])
def insertboards():
    boardname = request.form.get('boardName')
    id = request.form.get('id')
    sql = "INSERT INTO board (boardname,id) values (%s,%s);"
    try:
        query_db(sql,(boardname,id))
        return redirect(url_for('boardlist'))
    except:
        return {"message" : "insert Error"}

#게시글 호출 API
@api_bp.route('/contentlist/<int:boardId>',methods=["GET"])
def content(boardId):
    sql = "SELECT * FROM content where boardid=%s"
    try:
        result = query_db(sql,(boardId))
        print("결과: ",result)
        return render_template('contentlist.html',result=result,boardId=boardId)
    except:
        return {"message": "select Error"}


#게시글 등록 API
@api_bp.route('/content/<int:boardId>',methods=['POST'])
def writecontent(boardId):
    id = request.form.get('id')
    contentTitle = request.form.get('contentTitle')
    contentText = request.form.get('contentText')

    print(boardId,id,contentTitle,contentText)
    sql = "INSERT into content (boardid,id,contentTitle,contentText) values (%s,%s,%s,%s);"

    try:
        query_db(sql,(boardId,id,contentTitle,contentText))
        redirect_url = 'api/content/'+boardId
        print(redirect_url)
        return redirect(url_for(redirect_url,_method="GET"))

    except:
        return {"message":"insert Error"}


    

    # try:
    #     query_db(sql,(boardid))
    # except:
    #     return {"message":"select Error"}
# @api.bp.route()

# NOTE: /api/user로 POST 요청이 들어오면 해당 signup 함수 실행
# @api_bp.route('/user', methods=['POST'])
# def signup():
#     print("signup work")
#     # print(request)
#     id = request.form.get('id')
#     password = request.form.get('password')
#     name = request.form.get('name')
#     sql = "insert into users (id,password,name) Values (%s,%s,%s);"
#     result = query_db(sql,(id,password,name))

#     if result: #정상적으로 회원가입이 된 경우
#         print("result = ",result)
#         return redirect(url_for('login'))
#     else:
#         return {"message":"동일한 아이디가 있습니다"}

