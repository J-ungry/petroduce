from crypt import methods
from flask import Blueprint, request,session, jsonify
from flask_restful import Resource, Api
import cryptography
from sqlalchemy import false
from werkzeug.security import generate_password_hash,check_password_hash
from db import connect_db,query_db

# api_bp = Blueprint("api", __name__, url_prefix="/api")
api_bp = Blueprint("api", __name__,url_prefix="/api")
api = Api(api_bp)


#로그인 api
@api_bp.route("/login",methods=["POST"])
def login():
    data = request.get_json()
    id = data.get("id")

    sql = "SELECT * FROM USERS WHERE USR_ID=%s"
    try:
        result = query_db(sql,(id))
        password = check_password_hash(result[0]["USR_PW"],data.get("password"))
        
        if password is false:
            raise ValueError("Wrond password")
    except:
        return {"message":"EOORROROR"}
    finally:
        if password:
            session["id"] = id
            session["name"] = result[0]["USR_NAME"]

            return jsonify(res=result),200
        else:
            return {"Message" : "Login Error"}, 400
 
#로그아웃
@api_bp.route("/logout",methods=["GET"])
def logout():
    try:
        session.clear()
        return {"message":"로그아웃 되었습니다"},200
    except:
        return {"message":"로그아웃 실패"},400

# 회원가입 
@api_bp.route("/signup", methods=["POST"])
def signup():

    data = request.get_json()

    id = data.get("id")
    password =  generate_password_hash(data.get("password"))
    name = data.get("name")
    sql = "INSERT INTO USERS (USR_ID,USR_PW,USR_NAME) Values (%s,%s,%s);"

    try:
        query_db(sql,(id,password,name))
        return {"message":"회원가입 완료 !"}, 200
    except:
        return {"message":"회원가입 실패 (동일한 아이디가 있습니다)"},400

#아이디 중복확인
@api_bp.route("/user",methods=["POST"])
def checkId():
    data = request.get_json()

    id=data.get("USR_ID")

    sql = "SELECT COUNT(*) FROM USERS WHERE USR_ID=%s"

    try:
        result = query_db(sql,(id))
    except:
        return {"message":"중복확인 실패"},400
    finally:
        if result:
            return jsonify(res=result),200
        else:
            {"message":"중복확인 실패"},400


#회원 정보 수정하기
@api_bp.route("/user",methods=["PETCH"])
def modifyUser():

    data = request.get_json()
    id = data.get("id")
    name = data.get("name")

    sql = "UPDATE USERS set USR_ID=%s, USR_NAME=%s WHERE USR_ID=%s"

    try:
        query_db(sql,(id,name,id))
        session["id"] = id
        session["name"] = name

        return {"message":"회원정보 수정 성공"},200
    except:
        return {"message":"회원정보 수정 실패 "},400

#회원 정보 가져오기 => 
@api_bp.route("/user/<string:id>",methods=["GET"])
def getUserInfo(id):
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

#회원 탈퇴 
@api_bp.route("/user/<string:id>",methods=["DELETE"])
def deleteUser(id):
    sql = "DELETE FROM USERS WHERE USR_ID=%s"

    try:
        query_db(sql,(id))
        session.clear()
        return {"message":"회원 탈퇴가 완료되었습니다. 감사합니다"},200
    except:
        return {"message":"회원 탈퇴에 실패했습니다."},400

#회원 정보 확인
@api_bp.route("/user/password",methods=["POST"])
def checkUserInfo():
    data = request.get_json()
    id = data.get("USR_ID")
    name = data.get("USR_NAME")
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
@api_bp.route("/user/password",methods=["PETCH"])
def changePassword():

    data = request.get_json()

    id = data.get("USR_ID")
    password =  generate_password_hash(data.get("USR_PW"))

    sql = "UPDATE USERS set USR_PW=%s WHERE USR_ID=%s"

    try:
        query_db(sql,(password,id))
        session.clear()
        return {"message":"비밀번호 변경 완료"},200
    except:
        return {"message":"비밀번호 변경 실패"},400        

#게시판 목록 출력 
@api_bp.route("/board",methods=["GET"])
def boards():
    sql = "SELECT * FROM BOARD"
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
@api_bp.route("/board",methods=["POST"])
def boardCreate():

    data = request.get_json()

    id = data.get("id")
    boardName = data.get("boardName")
    sql = "INSERT INTO BOARD (TITLE,USR_ID) values (%s,%s);"

    try:
        query_db(sql,(boardName,id))
        
        return {"message":"성공적으로 생성했습니다"},200
    except:
        return {"message":"게시판 생성 실패"} ,400

#게시글 목록 출력
@api_bp.route("/content/<int:boardId>",methods=["GET"])
def contents(boardId):
    sql = "SELECT * FROM CONTENT WHERE BRD_ID=%s"
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
@api_bp.route("/content",methods=["POST"])
def contentCreate():

    data = request.get_json()

    boardid = data.get("boardid")
    id = data.get("id")
    contentTitle = data.get("contentTitle")
    contentText = data.get("contentText")

    sql = "INSERT INTO CONTENT (BRD_ID,USR_ID,TITLE,TEXT) values (%s,%s,%s,%s)"

    try:
        query_db(sql,(boardid,id,contentTitle,contentText))
        return {"message":"게시글 등록 성공"},200
    except:
        return {"message":"게시글 등록 실패"},400

#게시글 출력하기 
@api_bp.route("/content/<int:boardid>/<int:contentId>",methods=["GET"])
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
@api_bp.route("/content/<int:boardid>/<int:contentId>",methods=["PETCH"])
def modiftContent(boardid,contentId):

    data = request.get_json()
    contentTitle = data.get("contentTitle")
    contentText = data.get("contentText")
    sql = "UPDATE CONTENT SET TITLE=%s, TEXT=%s WHERE BRD_ID=%s AND IDX=%s"

    try:
        query_db(sql,(contentTitle,contentText,boardid,contentId))
        return {"message":"수정 성공"},200
    except:
        return {"message":"수정 실패"},400

#게시글 삭제하기
@api_bp.route("/content/<int:boardid>/<int:contentId>",methods=["DELETE"])
def deleteContent(boardid,contentId):
    sql = "DELETE FROM CONTENT WHERE BRD_ID=%s AND IDX=%s"
    try:
        query_db(sql,(boardid,contentId))
        return {"message":"삭제 성공"},200
    except:
        return {"message":"삭제 실패"},400

#댓글 불러오기
@api_bp.route("/comment/<string:contentId>",methods=["GET"])
def getComment(contentId):
    sql = "SELECT * FROM COMMENT WHERE CNT_IDX=%s"

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
            return {"message":"댓글 불러오기 실패"},400

#댓글 작성하기
@api_bp.route("/comment",methods=["POST"])
def postComment():
    data = request.get_json()

    CNT_IDX = data.get("CNT_IDX")
    USR_ID = data.get("USR_ID")
    TEXT = data.get("TEXT"
    )
    sql = "INSERT INTO COMMENT (CNT_IDX,USR_ID,TEXT) VALUES (%s,%s,%s)"

    try:
        query_db(sql,(CNT_IDX,USR_ID,TEXT))
        return {"message":"댓글 등록 완료"},200
    except:
        return {"message":"댓글 등록 실패"},400
