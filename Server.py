# 创建时间 2022-5-17
# 编写者 陈实
# 名称 服务端程序
import socket  # 网络通信库
from threading import Thread  # 多线程处理
import mysql.connector as mysql_conn
import json  # json数据传输
import gensim
import numpy as np
import jieba
import csv
from Robot import Chatbot
import datetime as dt

class Server:

    # 初始化方法
    def __init__(self):
        self.model = None
        self.add = ("localhost", 8000)  # 地址
        self.server = socket.socket()
        self.server.bind(self.add)
        self.server.listen(10)
        # 机器人
        self.robot = []
        # 所有的客户端
        self.clients = []
        # 用户标识与ip绑定信息
        self.clients_name_ip = {}
        self.load_robot()#运行机器人
        self.Conn_client()#开放连接

    # 开放连接客户端
    def Conn_client(self):
        print('服务器启动完成，现在开始开放连接 ... ...')
        while True:
            # 获得连接客户端信息
            client, address = self.server.accept()
            print(address)
            data = json.dumps("与服务器连接成功！")
            client.send(data.encode())
            # server 与 client通信 send() encode, recv() decode
            # 连接的用户添加到服务器用户列表中
            self.clients.append(client)
            # 服务器启动多个线程处理每个客户端的消息
            Thread(target=self.get_msg,
                   args=(client, self.clients, self.clients_name_ip, address)).start()

    # 运行机器人模型
    def load_robot(self):
        rb = Chatbot()
        rb.load_model()
        print('机器人模型加载ok啦！')
        rb.load_QA()
        print('语料库加载ok啦！')
        self.robot.append(rb)

    # 监听消息
    def get_msg(self, client, clients, clients_name_ip, address):
        while True:
            # 获取所有客户发送的消息
            try:
                recv_data = client.recv(1024)
                recv_data = json.loads(recv_data)
            except Exception as e:
                continue
            # 如果用户退出，输入Q
            if recv_data == "Q":
                break
            else:
                print(recv_data)
                self.Handle_request(recv_data, client)

    # 处理请求
    def Handle_request(self, recv_data, client):
        if recv_data[0] == 'request:登录信息':
            self.Handle_signin_request(recv_data, client)
        elif recv_data[0] == 'request:用户注册信息' or recv_data[0] == 'request:添加用户信息':
            self.Handle_user_regit_request(recv_data, client)
        elif recv_data[0] == 'request:专家入驻信息' or recv_data[0] == 'request:添加专家信息':
            self.Handle_expert_regit_request(recv_data, client)
        elif recv_data[0] == 'request:显示用户信息':
            self.Handle_show_request(client, '用户')
        elif recv_data[0] == 'request:显示专家信息':
            self.Handle_show_request(client, '专家')
        elif recv_data[0] == 'request:删除用户':
            self.Handle_delete_request(client, '用户', recv_data[1])
        elif recv_data[0] == 'request:删除专家':
            self.Handle_delete_request(client, '专家', recv_data[1])
        elif recv_data[0] == 'request:用户状态':
            self.Handle_activated_request(client, recv_data, '用户')
        elif recv_data[0] == 'request:专家状态':
            self.Handle_activated_request(client, recv_data, '专家')
        elif recv_data[0] == 'request:重置密码':
            self.Handle_resetpwd_request(client, recv_data)
        elif recv_data[0] == 'request:机器人问题':
            self.Handle_robot_request(client, recv_data)
        elif recv_data[0] == 'request:显示用户个人信息':
            self.Handle_showuser_request(client, recv_data)
        elif recv_data[0] == 'request:显示专家个人信息':
            self.Handle_showexpert_request(client, recv_data)
        elif recv_data[0] == 'request:修改信息':
            self.Handle_updateinf_request(client, recv_data)
        elif recv_data[0] == 'request:用户界面显示专家信息':
            self.Handle_userexpert_request(client)
        elif recv_data[0] == 'request:用户提问':
            self.Handle_userquestion_request(client, recv_data)
        elif recv_data[0] == 'request:用户邮箱问题刷新':
            self.Handle_useremailqu_request(client, recv_data)
        elif recv_data[0] == 'request:用户邮箱预约刷新':
            self.Handle_useremailap_request(client, recv_data)
        elif recv_data[0] == 'request:用户预约':
            self.Handle_userap_request(client, recv_data)
        elif recv_data[0] == 'request:显示用户问题':
            self.Handle_flushq_request(client, recv_data)
        elif recv_data[0] == 'request:问题内容':
            self.Handle_question_request(client, recv_data)
        elif recv_data[0] == 'request:预约内容':
            self.Handle_description_request(client,recv_data)
        elif recv_data[0] == 'request:专家回复':
            self.Handle_expertresponse_request(client, recv_data)
        elif recv_data[0] == 'request:显示用户预约':
            self.Handle_flusha_request(client, recv_data)
        elif recv_data[0] == 'request:接受预约':
            self.Handle_experthandleuserap_request(client, '接受', recv_data[1])
        elif recv_data[0] == 'request:拒绝预约':
            self.Handle_experthandleuserap_request(client, '拒绝', recv_data[1])
        elif recv_data[0] == 'request:专家预约邮箱':
            self.Handle_expertemailap_request(client, recv_data)
        elif recv_data[0] == 'request:专家问题邮箱':
            self.Handle_expertemailqu_request(client, recv_data)
        elif recv_data[0] == 'request:搜索专家':
            self.Handle_expertsearch_request(client, recv_data)

     # 处理登录请求
    def Handle_signin_request(self, recv_data, client):
        username = recv_data[1]
        password = recv_data[2]
        index = recv_data[3]
        if index == '0':
            inf = 'user_inf'
        elif index == '1':
            inf = 'expert_inf'
        else:
            inf = 'administrator_inf'
        conn = database_conn()
        cur = conn.cursor()
        resp = self.signin_request_check(username, password, inf, index, cur)
        if resp[1] == 'error':
            response = json.dumps(resp)
        else:
            response = json.dumps(resp)
        client.send(response.encode())
        close_database_conn(conn, cur)

    # 登录检查
    def signin_request_check(self, username, password, inf, index, cur):
        sql_username = "select password from %s where username = '%s'" % (inf, username)
        cur.execute(sql_username)
        data = cur.fetchall()
        if inf != 'administrator_inf':
            sql_username = "select active from %s where username = '%s'" % (inf, username)
            cur.execute(sql_username)
            active = cur.fetchall()
            if data:
                real_password = data[0][0]
                act = active[0][0]
                if real_password == password and act == '已激活':
                    response = ['response:登录信息', 'ok', index]
                elif act == '已激活':
                    response = ['response:登录信息', 'error', '密码输入错误,请检查输入']
                else:
                    response = ['response:登录信息', 'error', '未激活账号']
            else:
                response = ['response:登录信息', 'error', '用户名不存在，如需创建新用户请点击注册']
        else:
            if data:
                real_password = data[0][0]
                if real_password == password:
                    response = ['response:登录信息','ok', index]
                else:
                    response = ['response:登录信息', 'error', '密码输入错误,请检查输入']
            else:
                response = ['response:登录信息', 'error', '用户名不存在，如需创建新用户请点击注册']
        return response

    # 处理用户注册请求
    def Handle_user_regit_request(self, recv_data, client):
        # 收集数据
        username = recv_data[1]
        password = recv_data[2]
        email = recv_data[3]
        sex = recv_data[4]
        birthdate = recv_data[5]
        active = '已激活'
        # 连接数据库
        # 1.获取连接
        conn = database_conn()
        # 2.获取cursor
        cur = conn.cursor()
        check_message = self.user_regit_request_check(username, email, conn, cur)  # 检查提交的注册信息
        if check_message == 'ok':
            # 3.sql语句
            sql = "insert into user_inf(username, password, email, sex, birthdate, active) values(%s, %s, %s, %s, %s, %s)"
            # 4.执行语句
            cur.execute(sql, (username, password, email, sex, birthdate, active))
            # 5. insert、update\delete必须提交
            conn.commit()
            # 6. 关闭资源和发送消息
            close_database_conn(conn, cur)
            # 回复客户端
            if recv_data[0] == 'request:用户注册信息':
                response = json.dumps(['response:用户注册信息', 'ok'])
            else:
                response = json.dumps(['response:添加用户信息', 'ok'])
        else:
            close_database_conn(conn, cur)
            if recv_data[0] == '用户注册信息':
                response = json.dumps(['response:用户注册信息', 'error', check_message])
            else:
                response = json.dumps(['response:添加用户信息', 'error', check_message])
            client.send(response.encode())

        print(response)
        client.send(response.encode())
        close_database_conn(conn, cur)

    # 检查用户提交的注册信息是否有误,包括用户名和邮箱是否已经使用过
    def user_regit_request_check(self, username, email, conn, cur):
        sql_username = "select username from user_inf where username = '%s'" % username
        cur.execute(sql_username)
        username_check = cur.fetchall()
        if username_check:
            return '用户名已注册，请重新输入'
        sql_email = "select email from user_inf where email = '%s'" % email
        cur.execute(sql_email)
        email_check = cur.fetchall()
        if email_check:
            return '邮箱已注册，请重新输入'
        return 'ok'

    # 处理专家入驻请求
    def Handle_expert_regit_request(self, recv_data, client):
        # 收集数据
        username = recv_data[1]
        name = recv_data[2]
        password = recv_data[3]
        email = recv_data[4]
        sex = recv_data[5]
        birthdate = recv_data[6]
        organization = recv_data[7]
        department = recv_data[8]
        score = 10
        active = '未激活'
        # 连接数据库
        # 1.获取连接
        conn = database_conn()
        # 2.获取cursor
        cur = conn.cursor()
        check_message = self.expert_regit_request_check(username, email, cur)  # 检查提交的注册信息
        if check_message == 'ok':
            # 3.sql语句
            sql = \
                "insert into expert_inf(username, name, password, email, sex, birthdate," \
                " organization, department, score, active) " \
                "values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            # 4.执行语句
            cur.execute(sql, (username, name, password, email, sex, birthdate, organization, department, score, active))
            # 5. insert、update\delete必须提交
            conn.commit()
            # 6. 关闭资源和发送消息
            close_database_conn(conn, cur)
            # 回复客户端
            if recv_data[0] == 'response:专家入驻信息':
                response = json.dumps(['response:专家入驻信息', 'ok'])
            else:
                response = json.dumps(['response:添加专家信息', 'ok'])
        else:
            close_database_conn(conn, cur)
            if recv_data[0] == 'response:专家入驻信息':
                response = json.dumps(['response:专家入驻信息', 'error', check_message])
            else:
                response = json.dumps(['response:添加专家信息', 'error', check_message])
            client.send(response.encode())
        print(response)
        client.send(response.encode())
        close_database_conn(conn, cur)
    # 检查专家提交的注册信息是否有误,包括用户名和邮箱是否已经使用过
    def expert_regit_request_check(self, username, email, cur):
        sql_username = "select username from expert_inf where username = '%s'" % username
        cur.execute(sql_username)
        username_check = cur.fetchall()
        if username_check:
            return '用户名已注册，请重新输入'
        sql_email = "select email from expert_inf where email = '%s'" % email
        cur.execute(sql_email)
        email_check = cur.fetchall()
        if email_check:
            return '邮箱已注册，请重新输入'
        return 'ok'
    # 管理员界面信息处理
    # 处理显示用户\专家信息请求
    def Handle_show_request(self, client, iden):
        if iden == '用户':
            sql = "select id,username,email,sex,DATE_FORMAT(birthdate,'%Y-%m-%d') ,active from user_inf"
            response_head = 'response:显示用户信息'
        elif iden == '专家':
            sql = "select id,username,name,email,sex,DATE_FORMAT(birthdate,'%Y-%m-%d'),organization,department," \
                  "score,active from expert_inf"
            response_head = 'response:显示专家信息'
        conn = database_conn()
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        message = json.dumps([response_head, data])
        client.send(message.encode())
        close_database_conn(conn, cur)

    def Handle_userexpert_request(self, client):
        sql = "select id,username,name,email,sex,DATE_FORMAT(birthdate,'%Y-%m-%d'),organization,department," \
              "score,active from expert_inf"
        conn = database_conn()
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        message = json.dumps(['response:用户界面显示专家信息', data])
        client.send(message.encode())
        close_database_conn(conn, cur)

    # 管理员删除用户\专家信息
    def Handle_delete_request(self, client, ident, user_id):
        sql = "delete from user_inf where id = %s" % user_id
        response_head = 'response:删除用户'
        if ident == '专家':
            sql = "delete from expert_inf where id = %s" % user_id
            response_head = 'response:删除专家'
        print(sql)
        T_sql(sql)
        message = json.dumps([response_head])
        client.send(message.encode())

    # 管理员修改用户\专家状态信息
    def Handle_activated_request(self, client, req, iden):
        user_id = req[2]
        if iden == '用户':
            inf = 'user_inf'
        else:
            inf = 'expert_inf'
        if req[1] == '激活':
            sql = "update %s set active = '已激活' where id = '%s'" % (inf, user_id)
        else:
            sql = "update %s set active = '未激活' where id = '%s'" % (inf, user_id)

        T_sql(sql)
        message = json.dumps(['response:用户状态'])
        client.send(message.encode())

    # 处理重置密码请求
    def Handle_resetpwd_request(self, client, req):
        iden = req[2]
        md5_code = 'bdb8940a697ba5a2a8d1c5a491e5919c'  # 这是123456789的md5加密码，相对于将密码重置为123456789
        if req[1] == '用户':
            sql = "update user_inf set password = '%s' where id = %s" % (md5_code, iden)
        else:
            sql = "update expert_inf set password = '%s' where id = %s" % (md5_code, iden)
        T_sql(sql)
        message = json.dumps(['response:重置密码'])
        client.send(message.encode())


    def Handle_robot_request(self, client ,req):
        if req[2] == '儿科':
            rb = self.robot[0]
            ans = rb.answer(req[1])
            message = json.dumps(['response:机器人问题', ans])
            client.send(message.encode())


    # 处理信息修改请求
    def Handle_updateinf_request(self,client,recv_data):
        username = recv_data[4]
        resp = 'ok'
        if recv_data[1] == '用户':
            inf = 'user_inf'
        else:
            inf = 'expert_inf'
        if recv_data[2] == 'email':
            email = recv_data[3]
            sql_email = "select email from %s where email = '%s'" % (inf, email)
            conn = database_conn()
            cur = conn.cursor()
            cur.execute(sql_email)
            email_check = cur.fetchall()
            if email_check:
                resp = '邮箱已注册,修改失败'
        if resp == 'ok':
            sql = "update %s set %s = '%s' where username = '%s'" %(inf, recv_data[2], recv_data[3], username)
            T_sql(sql)
        message = json.dumps(['response:修改信息',resp])
        client.send(message.encode())


    # 处理用户个人信息界面刷新请求
    def Handle_showuser_request(self, client, req):
        usernn = req[1]
        sql = "select id,username,email,sex,DATE_FORMAT(birthdate,'%%Y-%%m-%%d') from user_inf where username = '%s'" % usernn
        response_head = 'response:显示用户个人信息'
        conn = database_conn()
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        message = json.dumps([response_head, data])
        print(message)
        client.send(message.encode())
        close_database_conn(conn, cur)

    # 处理用户专家信息界面刷新请求
    def Handle_showexpert_request(self, client, req):
        usernn = req[1]
        sql = "select id, username, name, email,sex,DATE_FORMAT(birthdate,'%%Y-%%m-%%d'),organization,department" \
              " from expert_inf where username = '%s'" % usernn
        response_head = 'response:显示专家个人信息'
        conn = database_conn()
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        message = json.dumps([response_head, data])
        print(message)
        client.send(message.encode())
        close_database_conn(conn, cur)


    def Handle_userquestion_request(self, client, recv_data):
        username = recv_data[1]
        userid = self.username2id(username,'user_inf')
        expertid = recv_data[2]
        question = recv_data[3]
        response = '未回复'
        Thedate = dt.datetime.now().strftime('%F')
        score = 10
        conn = database_conn()
        cur = conn.cursor()
        sql = "insert into qa(userid, expertid, question, response, Thedate, score)"\
                "values(%s, %s, %s, %s, %s, %s)"
        cur.execute(sql, (userid, expertid, question, response, Thedate, score))
        conn.commit()
        close_database_conn(conn, cur)
        response = json.dumps(['response:用户提问'])
        client.send(response.encode())
        close_database_conn(conn, cur)

    def Handle_userap_request(self, client, recv_data):
        username = recv_data[1]
        userid = self.username2id(username, 'user_inf')
        expertid = recv_data[2]
        description = recv_data[3]
        Thedate = recv_data[4]
        result = '未回复'
        conn = database_conn()
        cur = conn.cursor()
        sql = "insert into appointment(userid, expertid, description, thedate, result)" \
              "values(%s, %s, %s, %s, %s)"
        cur.execute(sql, (userid, expertid, description, Thedate, result))
        conn.commit()
        close_database_conn(conn, cur)
        response = json.dumps(['response:用户预约'])
        client.send(response.encode())
        close_database_conn(conn, cur)

    #用户名转id号
    def username2id(self,username,inf):
        sql = "select id from %s where username = '%s'" %(inf, username)
        conn = database_conn()
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        return data[0][0]
    def Handle_useremailqu_request(self, client, recv_data):
        username = recv_data[1]
        user_id = self.username2id(username,'user_inf')
        sql = "select id, userid, expertid, question, response, DATE_FORMAT(thedate,'%%Y-%%m-%%d'), score" \
              " from qa where userid = '%s'" %user_id
        conn = database_conn()
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        response = json.dumps(['response:用户邮箱问题刷新', data])
        print(response)
        client.send(response.encode())
        close_database_conn(conn, cur)

    def Handle_useremailap_request(self, client, recv_data):
        username = recv_data[1]
        user_id = self.username2id(username, 'user_inf')
        sql = "select id, userid, expertid, description, DATE_FORMAT(thedate,'%%Y-%%m-%%d'), result" \
              " from appointment where userid = '%s'" %user_id
        conn = database_conn()
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        response = json.dumps(['response:用户邮箱预约刷新', data])
        print(response)
        client.send(response.encode())
        close_database_conn(conn, cur)

    def Handle_flushq_request(self, client, recv_data):
        username = recv_data[1]
        e_id = self.username2id(username, 'expert_inf')
        sql = "select id, userid, DATE_FORMAT(thedate,'%%Y-%%m-%%d')" \
              " from qa where expertid = '%s'" % e_id
        conn = database_conn()
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        response = json.dumps(['response:显示用户问题', data])
        print(response)
        client.send(response.encode())
        close_database_conn(conn, cur)

    def Handle_flusha_request(self, client, recv_data):
        username = recv_data[1]
        e_id = self.username2id(username, 'expert_inf')
        sql = "select id, userid, DATE_FORMAT(thedate,'%%Y-%%m-%%d'), result" \
              " from appointment where expertid = '%s'" % e_id
        conn = database_conn()
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        response = json.dumps(['response:显示用户预约', data])
        print(response)
        client.send(response.encode())
        close_database_conn(conn, cur)

    def Handle_question_request(self, client, recv_data):
        qid = recv_data[1]
        sql = "select question from qa where id = '%s'" % qid
        conn = database_conn()
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        response = json.dumps(['response:问题内容', data])
        print(response)
        client.send(response.encode())
        close_database_conn(conn, cur)

    def Handle_description_request(self, client, recv_data):
        qid = recv_data[1]
        sql = "select description from appointment where id = '%s'" % qid
        conn = database_conn()
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        response = json.dumps(['response:预约内容', data])
        print(response)
        client.send(response.encode())
        close_database_conn(conn, cur)

    def Handle_expertresponse_request(self, client, recv_data):
        qa_id = recv_data[1]
        resp = recv_data[2]
        sql = "update qa set response = '%s' where id = '%s'" %(resp, qa_id)
        T_sql(sql)
        message = json.dumps(['response:专家回复'])
        client.send(message.encode())


    def Handle_experthandleuserap_request(self, client, result, theid):
        sql = "update appointment set result = '%s' where id = '%s'" % (result, theid)
        T_sql(sql)
        message = json.dumps(['response:专家处理预约'])
        client.send(message.encode())

    def Handle_expertemailqu_request(self, client, recv_data):
        username = recv_data[1]
        expertid = self.username2id(username,'expert_inf')
        sql = "select id,userid,DATE_FORMAT(thedate,'%%Y-%%m-%%d'),question,response,score from qa where expertid = '%s'" % expertid
        conn = database_conn()
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        response = json.dumps(['response:专家问题邮箱', data])
        print(response)
        client.send(response.encode())
        close_database_conn(conn, cur)

    def Handle_expertemailap_request(self, client, recv_data):
        username = recv_data[1]
        expertid = self.username2id(username,'expert_inf')
        sql = "select id,userid,DATE_FORMAT(thedate,'%%Y-%%m-%%d'), description, result from appointment where expertid = '%s'" % expertid
        conn = database_conn()
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        response = json.dumps(['response:专家预约邮箱', data])
        print(response)
        client.send(response.encode())
        close_database_conn(conn, cur)

    def Handle_expertsearch_request(self, client, recv_data):
        choose = recv_data[1]
        key_word = recv_data[2]
        if choose == '姓名':
            choose = 'name'
        elif choose == '单位':
            choose = 'organization'
        else:
            choose = 'department'
        sql = "select id,username,name,email,sex,DATE_FORMAT(birthdate,'%%Y-%%m-%%d'),organization,department," \
              "score,active from expert_inf where %s = '%s'" %(choose, key_word)
        conn = database_conn()
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        if data:
            message = json.dumps(['response:搜索专家', 'ok', data])
        else:
            message = json.dumps(['response:搜索专家', 'error', data])
        client.send(message.encode())
        close_database_conn(conn, cur)
# 获取数据库连接
def database_conn():
    try:
        conn = mysql_conn.connect(host='localhost',
                                  database='m_qa',
                                  user='root',
                                  password='1915200031'
                                  )
        return conn
    except mysql_conn.Error:
        print('数据库连接异常')


# 关闭数据库连接
def close_database_conn(conn, cursor):
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


# 数据库操作过程
def T_sql(sql):
    conn = database_conn()
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    close_database_conn(conn, cur)


if __name__ == '__main__':
    Server()
