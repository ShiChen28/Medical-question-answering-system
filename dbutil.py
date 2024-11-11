# 创建时间 2022-5-17
# 名称 数据库工具类
import mysql.connector as mysql_conn

# 获取连接
def database_conn():
    try:
        conn = mysql_conn.connect(host = '*******',
                                  database = '*******',
                                  user = '*******',
                                  password = '*******'
                                  )
        return conn
    except mysql_conn.Error:
        print('数据库连接异常')

# 关闭连接
def close_database_conn(conn, cursor):
    try:
        if cursor:
            cursor.close()
        if conn:s
            conn.close()
    except mysql_conn.Error:
        print('数据库关闭异常')
    finally:
        cursor.close()
        conn.close()
