# 数据库的工具类
import mysql.connector as mysql_conn

# 获取连接
def get_conn():
    try:
        conn = mysql_conn.connect(host = 'localhost',
                                  database = 'm_qa',
                                  user = 'root',
                                  password = '1915200031'
                                  )
        return conn
    except mysql_conn.Error:
        print('数据库连接异常')

# 关闭连接
def close_conn(conn, cursor):
    try:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    except mysql_conn.Error:
        print('数据库关闭异常')
    finally:
        cursor.close()
        conn.close()

def show_author():
    conn = get_conn()
    cur = conn.cursor()
    Zpao = 'Zha0dapao'
    sql = "select username from user_inf "
    cur.execute(sql)
    d0 = cur.fetchall()
    sql = "select username from user_inf  where username = '%s'" % Zpao
    cur.execute(sql)
    d1 = cur.fetchall()
    return d0,d1

a,b = show_author()
print(a[0][0])
print(b)
if a:
    print(1)
if b:
    print(1)