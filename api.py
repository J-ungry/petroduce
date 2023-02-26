from flask import Blueprint, request,session,redirect,url_for,render_template
from flask_restful import Resource, Api
import pymysql.cursors
import cryptography
from db import connect_db,query_db

api_bp = Blueprint('api', __name__)
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


#Login API
class Login(Resource):
    #로그인 확인 api
    def post(self):
        print('work')
        id = request.form['id']
        password = request.form['password']

        sql = "SELECT * FROM users WHERE id=%s AND password=%s"
        print('work')
        result = query_db(sql,(id,password))

        if result:
            name = result[0]['name']
            session['id']=id
            session['name']=name
            return redirect(url_for('boardlist'))
        else:
            return redirect(url_for('login'))

#User Api (회원가입 , 정보수정, 탈퇴, 정보확인)
class User(Resource):
    def get(self):
        return render_template("signup.html")
    #회원가입
    def post(self):
        print("signup work")
        id = request.form['id']
        password = request.form['password']
        name = request.form['name']

        sql = "insert into users (id,password,name) Values (%s,%s,%s);"
        result = query_db(sql,(id,password,name))

        if result: #정상적으로 회원가입이 된 경우
            print("result = ",result)
            return redirect(url_for('login'))
        else:
            return {"message":"동일한 아이디가 있습니다"}




api.add_resource(Login, '/api/login')
api.add_resource(User,'/api/user')