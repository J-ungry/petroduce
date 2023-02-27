#데이터 베이스 실제 접속 소스코드 

import pymysql
from config import Config

def connect_db():
    conn = pymysql.connect(
        host = Config.MYSQL_HOST,
        user = Config.MYSQL_USER,
        password = Config.MYSQL_PASSWORD,
        db = Config.MYSQL_DB,
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn

def query_db(query,args=()):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query,args)
    result = cursor.fetchall()
    print('result',result)
    conn.commit()
    cursor.close()
    conn.close()

    return result

