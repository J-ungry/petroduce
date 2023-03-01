from crypt import methods
import json
from unittest import result
from flask import Blueprint, request,session,redirect,url_for,render_template, jsonify
from flask_restful import Resource, Api
import pymysql.cursors
import cryptography
from sqlalchemy import false
from werkzeug.security import generate_password_hash,check_password_hash
from db import connect_db,query_db

# api_bp = Blueprint('api', __name__, url_prefix="/api")
api_bp = Blueprint('api', __name__,url_prefix="/api")
api = Api(api_bp)


#로그인 api
@api_bp.route('/login',methods=['POST'])
def login():
    print("Login work")
    data = request.get_json()
    id = data.get('id')

    sql = "SELECT * FROM USERS WHERE USR_ID=%s"
    try:
        result = query_db(sql,(id))
        password = check_password_hash(result[0]['USR_PW'],data.get('password'))
        
        if password is false:
            raise ValueError("Wrond password")
    except:
        return {"message":"EOORROROR"}
    finally:
        if password:
            session['id'] = id
            session['name'] = result[0]['USR_NAME']

            return jsonify(res=result),200
        else:
            return {"Message" : "Login Error"}, 400
 
#로그아웃
@api_bp.route('/logout',methods=['GET'])
def logout():
    print("logout work")
    try:
        session.clear()
        return {"message":"로그아웃 되었습니다"},200
    except:
        return {"message":"로그아웃 실패"},400

# 회원가입 
@api_bp.route('/signup', methods=['POST'])
def signup():
    print("signup work")
    # print(request)

    data = request.get_json()

    id = data.get('id')
    password =  generate_password_hash(data.get('password'))
    print(password)
    name = data.get('name')
    sql = "INSERT INTO USERS (USR_ID,USR_PW,USR_NAME) Values (%s,%s,%s);"

    try:
        query_db(sql,(id,password,name))
        return {"message":"회원가입 완료 !"}, 200
    except:
        return {"message":"회원가입 실패 (동일한 아이디가 있습니다)"},400

#아이디 중복확인
@api_bp.route('/user',methods=['POST'])
def checkId():
    data = request.get_json()

    id=data.get('USR_ID')

    sql = 'SELECT COUNT(*) FROM USERS WHERE USR_ID=%s'

    try:
        result = query_db(sql,(id))
    except:
        return {"message":"중복확인 실패"},400
    finally:
        if result:
            return jsonify(res=result),200
        else:
            {"message":"중복확인 실패"},400

#회원 정보 가져오기
@api_bp.route('/user/<string:id>',methods=["GET"])
def getUserInfo(id):
    print("get work !")
    sql = "SELECT * FROM USERS WHERE USR_ID=%s"

    try:
        result = query_db(sql,(id))
    except:
        return {"message":"회원 정보 가져오기에 실패했습니다"},400
    finally:
        if result:
            return jsonify(res=result),200
        else:
            return {"message":"회원 정보 가져오기에 실패했습니다"},400

#회원 정보 수정하기
@api_bp.route('/user',methods=["PETCH"])
def modifyUser():
    print("modify work")

    data = request.get_json()
    id = data.get('id')
    name = data.get('name')

    print(id)
    print(name)

    sql = "UPDATE USERS set USR_ID=%s, USR_NAME=%s WHERE USR_ID=%s"

    try:
        query_db(sql,(id,name,id))
        print('work')
        session['id'] = id
        session['name'] = name

        return {"message":"회원정보 수정 성공"},200
    except:
        return {"message":"회원정보 수정 실패 "},400

#회원 정보 확인
@api_bp.route('/user/password',methods=["POST"])
def checkUserInfo():
    print("post work !")

    data = request.get_json()
    id = data.get('USR_ID')
    name = data.get('USR_NAME')
    sql = "SELECT * FROM USERS WHERE USR_ID=%s AND USR_NAME=%s"

    try:
        result = query_db(sql,(id,name))
    except:
        return {"message":"회원 정보 가져오기에 실패했습니다"},400
    finally:
        if result:
            return jsonify(res=result),200
        else:
            return {"message":"회원 정보 가져오기에 실패했습니다"},400

#비밀번호 변경 
@api_bp.route('/user/password',methods=["PETCH"])
def changePassword():
    print("petch work !")

    data = request.get_json()

    id = data.get('USR_ID')
    password =  generate_password_hash(data.get('USR_PW'))

    print(id,password)
    sql = "UPDATE USERS set USR_PW=%s WHERE USR_ID=%s"

    try:
        query_db(sql,(password,id))
        return {"message":"비밀번호 변경 완료"},200
    except:
        return {"message":"비밀번호 변경 실패"},400


#회원 탈퇴 
@api_bp.route('/user/<string:id>',methods=["DELETE"])
def deleteUser(id):
    sql = "DELETE FROM USERS WHERE USR_ID=%s"

    try:
        query_db(sql,(id))
        session.clear()
        return {"message":"회원 탈퇴가 완료되었습니다. 감사합니다"},200
    except:
        return {"message":"회원 탈퇴에 실패했습니다."},400

#게시판 목록 출력 
@api_bp.route('/board',methods=["GET"])
def boards():
    sql = 'SELECT * FROM BOARD'
    try:
        result = query_db(sql)
    except:
        return {"message":"게시판 불러오기에 실패했습니다"}
    finally:
        if len(result)!=0:
            return jsonify(res=result),200
        elif len(result)==0:
            return jsonify(res=[]),200
        else:
            return {"message":"게시판 불러오기에 실패했습니다"},400

#게시판 등록하기 
@api_bp.route('/board',methods=["POST"])
def boardCreate():
    print("create Work")

    data = request.get_json()

    id = data.get('id')
    boardName = data.get('boardName')
    print(id)
    print(boardName)
    sql = "INSERT INTO BOARD (TITLE,USR_ID) values (%s,%s);"

    try:
        print("동작")
        query_db(sql,(boardName,id))
        
        return {"message":"성공적으로 생성했습니다"},200
    except:
        return {"message":"게시판 생성 실패"} ,400

#게시글 목록 출력
@api_bp.route('/content/<int:boardId>',methods=["GET"])
def contents(boardId):
    sql = 'SELECT * FROM CONTENT WHERE BRD_ID=%s'
    try:
        result = query_db(sql,(boardId))
    except:
        return {"message": "게시글 불러오기에 실패했습니다"}
    finally:
        if len(result)!=0:
            return jsonify(res=result),200
        elif len(result)==0:
            return jsonify(res=[]),200
        else:
            return {"message":"게시글 불러오기에 실패했습니다"},400

#게시글 등록하기
@api_bp.route('/content',methods=["POST"])
def contentCreate():
    print("create Work")

    data = request.get_json()

    boardid = data.get('boardid')
    id = data.get('id')
    contentTitle = data.get('contentTitle')
    contentText = data.get('contentText')
    print(id)

    sql = "INSERT INTO CONTENT (BRD_ID,USR_ID,TITLE,TEXT) values (%s,%s,%s,%s)"

    try:
        query_db(sql,(boardid,id,contentTitle,contentText))
        return {"message":"게시글 등록 성공"},200
    except:
        return {"message":"게시글 등록 실패"},400

#게시글 출력하기 
@api_bp.route('/content/<int:boardid>/<int:contentId>',methods=["GET"])
def readContent(boardid,contentId):
    sql = "SELECT * FROM CONTENT WHERE BRD_ID=%s AND IDX=%s"
    try:
        result = query_db(sql,(boardid,contentId))
    except:
        return {"message":"게시글 불러오기에 실패했습니다"}
    finally:
        if result:
            return jsonify(res=result),200
        else:
            return {"message":"게시글 불러오기에 실패했습니다"},400

#게시글 수정하기
@api_bp.route('/content/<int:boardid>/<int:contentId>',methods=["PETCH"])
def modiftContent(boardid,contentId):
    print("petch work")

    data = request.get_json()
    contentTitle = data.get('contentTitle')
    contentText = data.get('contentText')
    sql = "UPDATE CONTENT SET TITLE=%s, TEXT=%s WHERE BRD_ID=%s AND IDX=%s"

    try:
        query_db(sql,(contentTitle,contentText,boardid,contentId))
        return {"message":"수정 성공"},200
    except:
        return {"message":"수정 실패"},400

#게시글 삭제하기
@api_bp.route('/content/<int:boardid>/<int:contentId>',methods=["DELETE"])
def deleteContent(boardid,contentId):
    print("delete work")

    sql = "DELETE FROM CONTENT WHERE BRD_ID=%s AND IDX=%s"
    try:
        query_db(sql,(boardid,contentId))
        return {"message":"삭제 성공"},200
    except:
        return {"message":"삭제 실패"},400

#댓글 불러오기
@api_bp.route('/comment/<string:contentId>',methods=['GET'])
def getComment(contentId):
    print('get work')
    sql = 'SELECT * FROM COMMENT WHERE CNT_IDX=%s'

    try:
        result = query_db(sql,(contentId))
    except:
        return {"message":"댓글 불러오기 실패"}
    finally:
        if len(result)!=0:
            return jsonify(res=result),200
        elif len(result)==0:
            return jsonify(res=[]),200
        else:
            return {'message':"댓글 불러오기 실패"},400

#댓글 작성하기
@api_bp.route('/comment',methods=["POST"])
def postComment():
    print('post work')
    data = request.get_json()

    CNT_IDX = data.get('CNT_IDX')
    USR_ID = data.get('USR_ID')
    TEXT = data.get('TEXT'
    )
    sql = "INSERT INTO COMMENT (CNT_IDX,USR_ID,TEXT) VALUES (%s,%s,%s)"

    try:
        query_db(sql,(CNT_IDX,USR_ID,TEXT))
        return {"message":"댓글 등록 완료"},200
    except:
        return {"message":"댓글 등록 실패"},400

#     @api_bp.route('/content',methods=["POST"])
# def contentCreate():
#     print("create Work")

#     data = request.get_json()

#     boardid = data.get('boardid')
#     id = data.get('id')
#     contentTitle = data.get('contentTitle')
#     contentText = data.get('contentText')
#     print(id)

#     sql = "INSERT INTO content (boardid,id,contentTitle,contentText) values (%s,%s,%s,%s)"

#     try:
#         query_db(sql,(boardid,id,contentTitle,contentText))
#         return {"message":"게시글 등록 성공"},200
#     except:
#         return {"message":"게시글 등록 실패"},400

# #Login API
# class Login(Resource):
#     #로그인 확인 api
#     def post(self):
#         print('work')
#         id = request.form['id']
#         password = request.form['password']

#         sql = "SELECT * FROM users WHERE id=%s AND password=%s"
#         print('work')
#         result = query_db(sql,(id,password))

#         if result:
#             name = result[0]['name']
#             session['id']=id
#             session['name']=name
#             return redirect(url_for('boardlist'))
#         else:
#             return redirect(url_for('login'))

# #User Api (회원가입 , 정보수정, 탈퇴, 정보확인)
# class User(Resource):
#     def get(self):
#         return render_template("signup.html")
#     #회원가입
#     def post(self):
#         print("signup work")
#         id = request.form['id']
#         password = request.form['password']
#         name = request.form['name']

#         sql = "insert into users (id,password,name) Values (%s,%s,%s);"
#         result = query_db(sql,(id,password,name))

#         if result: #정상적으로 회원가입이 된 경우
#             print("result = ",result)
#             return redirect(url_for('login'))
#         else:
#             return {"message":"동일한 아이디가 있습니다"}




# api.add_resource(login, '/api/login')
# # api.add_resource(User,'/api/user')