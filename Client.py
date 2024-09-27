# 创建时间 2022-5-17
# 名称 客户端程序
import json
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate
import socket
from threading import Thread
from PyQt5.uic import loadUiType
from qt_material import QtStyleTools
import hashlib


ui, _ = loadUiType('main_win_0508.ui')#加载UI文件

class Client_window(QMainWindow, QtStyleTools,ui):
    #定义构造方法
    def __init__(self):
        QMainWindow.__init__(self)
        #窗口初始化
        self.status = '用户' #用来记录客户的身份
        self.username = 0 #用来标记用户
        self.setupUi(self)
        self.tabWidget.tabBar().setVisible(False)#选项卡标签隐藏
        self.RegitTabWidget.tabBar().setVisible(False)
        self.tabWidget.setCurrentIndex(0)#初始化为登录界面
        self.RegitTabWidget.setCurrentIndex(0)  # 注册界面初始化为用户注册
        self.User_TabWidget.setCurrentIndex(0)  # 用户界面初始化为个人信息
        self.Expert_TabWidget.setCurrentIndex(0) # 专家界面初始化为个人信息
        self.Admin_TabWidget.setCurrentIndex(0) # 管理员界面初始化为用户管理
        self.apply_stylesheet(self, theme='light_cyan_500.xml', invert_secondary=True)#主题初始化为默认主题
        self.user_inf_table.setEditTriggers(QAbstractItemView.NoEditTriggers)#设置表格不可编辑
        self.user_inf_table.setSelectionBehavior(QAbstractItemView.SelectRows)#设置表格一次选择整行
        self.user_inf_table.setSelectionMode(QAbstractItemView.SingleSelection)#设置表格不可多选
        self.expert_inf_table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置表格不可编辑
        self.expert_inf_table.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置表格一次选择整行
        self.expert_inf_table.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置表格不可多选
        self.user_expert_table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置表格不可编辑
        self.user_expert_table.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置表格一次选择整行
        self.user_expert_table.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置表格不可多选
        self.user_expertap_table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置表格不可编辑
        self.user_expertap_table.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置表格一次选择整行
        self.user_expertap_table.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置表格不可多选
        self.expert_userq.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置表格不可编辑
        self.expert_userq.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置表格一次选择整行
        self.expert_userq.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置表格不可多选
        self.expert_usera.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置表格不可编辑
        self.expert_usera.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置表格一次选择整行
        self.expert_usera.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置表格不可多选
        # 按钮功能与设置
        self.bottn()#部分按钮功能
        self.DayButton.setChecked(True)#初始化单选项为默认模式
        self.RegitUserButton.setChecked(True)
        self.user_regit_birthdate.setMaximumDate(QDate.currentDate().addDays(1))#设置日期按钮的最大日期
        self.expert_regit_birthdate.setMaximumDate(QDate.currentDate().addDays(1))
        self.admin_expert_add_birthdate.setMaximumDate(QDate.currentDate().addDays(1))
        # 允许弹出日历
        self.user_regit_birthdate.setCalendarPopup(True)
        self.expert_regit_birthdate.setCalendarPopup(True)
        self.admin_user_add_birthdate.setCalendarPopup(True)
        self.user_apdate.setCalendarPopup(True)
        self.user_apdate.setMinimumDate(QDate.currentDate().addDays(1))
        # 设置日期格式
        self.user_regit_birthdate.setDisplayFormat('yyyy-MM-dd')
        self.expert_regit_birthdate.setDisplayFormat('yyyy-MM-dd')
        self.admin_user_add_birthdate.setDisplayFormat('yyyy-MM-dd')
        self.admin_expert_add_birthdate.setDisplayFormat('yyyy-MM-dd')
        #多线程
        self.work_thread()
        #连接服务器
        self.add = ("localhost", 8000) #地址
        self.client = socket.socket()
        self.client.connect(self.add)

    #部分按钮功能
    def bottn(self):
        #注册按钮
        self.RegitPushButton.clicked.connect(self.to_regit)
        #样式按钮
        self.DayButton.toggled.connect(self.theme_day)
        self.DarkButton.toggled.connect(self.theme_dark)
        #退出登录按钮
        self.ExitPushButton.clicked.connect(self.exit_login)

    #一键清楚所有LineEdit内容
    def Clear_LineEdit(self):
        self.UsernameLineEdit.setText('')
        self.PasswordLineEdit.setText('')
        self.user_regit_username.setText('')
        self.user_regit_password.setText('')
        self.user_regit_passwordag.setText('')
        self.user_regit_email.setText('')
        self.expert_regit_username.setText('')
        self.expert_regit_name.setText('')
        self.expert_regit_password.setText('')
        self.expert_regit_passwordag.setText('')
        self.Regit_Error.setText('')
        self.admin_user_add_message.setText('')
        self.robot_message.clear()
        self.user_question.clear()
        self.user_ap.clear()

    #清空表格内容
    def Clear_widget(self):
        self.user_inf_table.setRowCount(0)
        self.user_inf_table.clearContents()
        self.expert_inf_table.setRowCount(0)
        self.expert_inf_table.clearContents()
        self.user_expert_table.setRowCount(0)
        self.user_expert_table.clearContents()
        self.user_expertap_table.setRowCount(0)
        self.user_expertap_table.clearContents()
        self.expert_userq.setRowCount(0)
        self.expert_userq.clearContents()
        self.expert_usera.setRowCount(0)
        self.expert_usera.clearContents()


    #注册按钮页面跳转
    def to_regit(self):
        self.Clear_LineEdit()
        self.tabWidget.setCurrentIndex(4)  # 切换到注册界面

    def regituser_win(self):
        if self.RegitUserButton.isChecked():
            self.Clear_LineEdit()
            self.RegitTabWidget.setCurrentIndex(0)#切换到用户注册
    def regitexpert_win(self):
        if self.RegitExpertButton.isChecked():
            self.Clear_LineEdit()
            self.RegitTabWidget.setCurrentIndex(1)#切换到专家入驻

    #注册界面按钮
    def btn_regit(self):
        self.user_regit_go.clicked.connect(self.user_regit)
        self.expert_regit_go.clicked.connect(self.expert_regit)
        self.RegitUserButton.toggled.connect(self.regituser_win)
        self.RegitExpertButton.toggled.connect(self.regitexpert_win)

    #注册信息处理按钮:用户
    def user_regit(self):
        self.Regit_Error.setText('')
        if self.user_regit_handle_client():#客户端注册信息检测
            username = self.user_regit_username.text().strip()
            password = self.user_regit_password.text().strip()
            password = md5_code(password)  # 对密码进行加密处理
            email = self.user_regit_email.text().strip()
            sex = self.user_regit_sex.currentText()
            birthdate = self.user_regit_birthdate.dateTime().toString("yyyy-MM-dd")
            user_regit_inf = ['request:用户注册信息', username, password, email, sex, birthdate]
            print(user_regit_inf)
            message = json.dumps(user_regit_inf)
            self.client.send(message.encode())

    #客户端注册信息检查:用户
    def user_regit_handle_client(self):
        if self.user_regit_password.text() != self.user_regit_passwordag.text():
            self.Regit_Error.setText('两次密码输入不一样，请检查')
            self.user_regit_passwordag.setText('')
            return 0
        if len(self.user_regit_password.text().strip()) < 8:
            self.Regit_Error.setText('密码需要至少8位，建议包含字母、数字和特殊字符')
            self.user_regit_password.setText('')
            self.user_regit_passwordag.setText('')
            return 0
        if self.user_regit_username.text().strip() == '':
            self.Regit_Error.setText('用户名不可以为空')
            return 0
        if self.user_regit_email.text().strip() == '':
            self.Regit_Error.setText('邮箱不可以为空')
            return 0
        email = self.user_regit_email.text().strip()
        if email[-4:] != '.com' and email[-3:] != '.en':
            self.Regit_Error.setText('邮箱格式无效')
            return 0
        return 1

    # 注册信息处理按钮:专家
    def expert_regit(self):
        self.Regit_Error.setText('')
        if self.expert_regit_handle_client():#客户端注册信息检测
            username = self.expert_regit_username.text().strip()
            name = self.expert_regit_name.text().strip()
            password = self.expert_regit_password.text().strip()
            password = md5_code(password)  # 对密码进行加密处理
            email = self.expert_regit_email.text().strip()
            sex = self.expert_regit_sex.currentText()
            birthdate = self.expert_regit_birthdate.dateTime().toString("yyyy-MM-dd")
            organization = self.expert_regit_organization.text().strip()
            department = self.expert_regit_department.currentText()
            expert_regit_inf = ['request:专家入驻信息', username, name, password, email, sex, birthdate, organization, department]
            print(expert_regit_inf)
            message = json.dumps(expert_regit_inf)
            self.client.send(message.encode())

    # 客户端注册信息检查:专家
    def expert_regit_handle_client(self):
        if self.expert_regit_password.text() != self.expert_regit_passwordag.text():
            self.Regit_Error.setText('两次密码输入不一样，请检查')
            self.expert_regit_passwordag.setText('')
            return 0
        if len(self.expert_regit_password.text().strip()) < 8:
            self.Regit_Error.setText('密码需要至少8位，建议包含字母、数字和特殊字符')
            self.expert_regit_password.setText('')
            self.expert_regit_passwordag.setText('')
            return 0
        if self.expert_regit_username.text().strip() == '':
            self.Regit_Error.setText('用户名不可以为空')
            return 0
        if self.expert_regit_email.text().strip() == '':
            self.Regit_Error.setText('邮箱不可以为空')
            return 0
        email = self.expert_regit_email.text().strip()
        if email[-4:] != '.com' and email[-3:] != '.cn':
            self.Regit_Error.setText('邮箱格式无效')
            return 0
        if self.expert_regit_organization.text().strip() == '':
            self.Regit_Error.setText('所在单位不可以为空')
            return 0
        return 1

    #登录按钮功能实现
    def btn_login(self):
        self.LoginPushButton.clicked.connect(self.signin)
        self.PasswordLineEdit.returnPressed.connect(self.signin)

    #登录功能
    def signin(self):
        #发送用户名，密码
        username = self.UsernameLineEdit.text().strip()
        password = self.PasswordLineEdit.text().strip()
        password = md5_code(password)
        index = str(self.LoginComboBox.currentIndex())
        self.username = username
        message = json.dumps(['request:登录信息', username, password, index])
        self.client.send(message.encode('utf-8'))
        #清空窗口
        self.UsernameLineEdit.setText('')
        self.PasswordLineEdit.setText('')
        self.Login_Error.setText('')

    #样式切换按钮功能实现
    def theme_day(self):
        if self.DayButton.isChecked():
            self.apply_stylesheet(self, theme = 'light_cyan_500.xml',invert_secondary=True)

    def theme_dark(self):
        if self.DarkButton.isChecked():
            self.apply_stylesheet(self, theme = 'dark_cyan.xml')

    #退出登录按钮功能
    def exit_login(self):
        self.Clear_LineEdit()
        self.tabWidget.setCurrentIndex(0)#切换到登录界面

    # 切换到机器人页面
    def goto_rb(self):
        self.tabWidget.setCurrentIndex(5)

    def exit_rb(self):
        if self.status == '用户':
            self.tabWidget.setCurrentIndex(1)
        elif self.status == '专家':
            self.tabWidget.setCurrentIndex(2)
        else:
            self.tabWidget.setCurrentIndex(3)
        # 机器人界面

    def bth_robot(self):
        self.expert_robot.clicked.connect(self.goto_rb)
        self.user_robot.clicked.connect(self.goto_rb)
        self.exit_robot.clicked.connect(self.exit_rb)
        self.send_robot.clicked.connect(self.robot_send)
        self.reset_robot.clicked.connect(self.reset)

    #多线程加速处理
    def work_thread(self):
        Thread(target=self.btn_login).start()
        Thread(target=self.btn_regit).start()
        Thread(target=self.bth_admin).start()
        Thread(target=self.recv_message).start()
        Thread(target=self.bth_robot).start()
        Thread(target=self.bth_user).start()
        Thread(target=self.bth_expert).start()

    #用户界面
    #用户界面按钮设置
    def bth_user(self):
        self.user_flush.clicked.connect(self.user_flush_request)
        self.user_updatesex.clicked.connect(self.user_updatesex_request)
        self.user_updateem.clicked.connect(self.user_updateem_request)
        self.user_updatepw.clicked.connect(self.user_updatepw_request)
        self.user_updatebd.clicked.connect(self.user_updatebd_request)
        self.user_expertflush.clicked.connect(self.user_expertflush_request)
        self.user_expertflushap.clicked.connect(self.user_expertflush_request)
        self.user_expertsend.clicked.connect(self.user_expertsend_request)
        self.user_resetquestion.clicked.connect(self.reset)
        self.user_emailflushqu.clicked.connect(self.user_emailflushqu_request)
        self.user_emailflushap.clicked.connect(self.user_emailflushap_request)
        self.user_apreset.clicked.connect(self.reset)
        self.user_apsend.clicked.connect(self.user_apsend_request)
        self.user_searchexpertqu.clicked.connect(self.user_searchexpertqu_request)
        self.user_searchexpertap.clicked.connect(self.user_searchexpertap_request)

    #根据关键词搜索专家
    def user_searchexpertqu_request(self):
        keywordchoose = self.user_choosekeywordqu.currentText()
        key_word = self.user_keywordqu.text().strip()
        message = json.dumps(['request:搜索专家', keywordchoose, key_word])
        self.client.send(message.encode())

    def user_searchexpertap_request(self):
        keywordchoose = self.user_choosekeywordap.currentText()
        key_word = self.user_keywordap.text().strip()
        message = json.dumps(['request:搜索专家', keywordchoose, key_word])
        self.client.send(message.encode())

    def user_searchexpert_response(self, response):
        if response[1] == 'ok':
            self.user_expertflush_response(response[2])
        else:
            self.Regit_Error.setText('返回结果为空，请检查输入~')

    #发送预约
    def user_apsend_request(self):
        selectItem = self.user_expertap_table.selectedItems()
        if selectItem:
            expert_id = selectItem[0].text()
            user_ap = self.user_ap.toPlainText()
            thedate = self.user_apdate.dateTime().toString("yyyy-MM-dd")
            message = json.dumps(['request:用户预约', self.username, expert_id, user_ap, thedate])
            self.client.send(message.encode())
            self.reset()

    def user_flush_request(self):
        message = json.dumps(['request:显示用户个人信息',self.username,self.status])
        self.client.send(message.encode('utf-8'))

    def user_flush_response(self,data):
        theid = data[0][0]
        username = data[0][1]
        email = data[0][2]
        sex = data[0][3]
        birthdate = data[0][4]
        text = '用户id:%s \n用户名:%s \n邮箱:%s \n性别:%s \n出生日期: %s' % (theid, username, email, sex, birthdate)
        self.user_inf_label.setText(text)

    def user_updatesex_request(self):
        sex = self.user_update_sex.currentText()
        message = json.dumps(['request:修改信息', self.status, 'sex', sex, self.username])
        self.client.send(message.encode())

    def user_updateem_request(self):
        email = self.user_update_email.text().strip()
        if len(email) < 1:
            self.Regit_Error.setText('请检查是否输入为空')
        else:
            message = json.dumps(['request:修改信息', self.status, 'email',email, self.username])
        self.client.send(message.encode())

    def user_updatepw_request(self):
        pw = self.user_update_password.text().strip()
        if len(pw) < 8:
            self.Regit_Error.setText('密码至少8位')
        else:
            message = json.dumps(['request:修改信息', self.status, 'password', pw, self.username])
        self.client.send(message.encode())

    def user_updatebd_request(self):
        bd = self.user_update_birthdate.dateTime().toString("yyyy-MM-dd")
        message = json.dumps(['request:修改信息', self.status, 'birthdate', bd, self.username])
        self.client.send(message.encode())

    def update_response(self,rev):
        if rev[1] == 'ok':
            self.Regit_Error.setText('信息修改成功')
            self.user_flush_request()
            self.expert_flush_request()
        else:
            self.Regit_Error.setText(rev[1])

    def user_expertflush_request(self):
        message = json.dumps(['request:用户界面显示专家信息'])
        print(message)
        self.client.send(message.encode('utf-8'))

    def user_expertflush_response(self, data):
        self.user_expert_table.setRowCount(0)
        self.user_expert_table.insertRow(0)
        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.user_expert_table.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1
            row_position = self.user_expert_table.rowCount()
            self.user_expert_table.insertRow(row_position)
        self.user_expertap_table.setRowCount(0)
        self.user_expertap_table.insertRow(0)
        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.user_expertap_table.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1
            row_position = self.user_expertap_table.rowCount()
            self.user_expertap_table.insertRow(row_position)

    def user_expertsend_request(self):
        selectItem = self.user_expert_table.selectedItems()
        if selectItem:
            expert_id = selectItem[0].text()
            user_question = self.user_question.toPlainText()
            message = json.dumps(['request:用户提问', self.username, expert_id,user_question])
            self.client.send(message.encode())
            self.reset()

    def user_expertsend_response(self):
        self.Regit_Error.setText('发送成功!')

    def user_emailflushqu_request(self):
        message = json.dumps(['request:用户邮箱问题刷新', self.username])
        print(message)
        self.client.send(message.encode())

    def user_emailflushqu_response(self,data):
        self.user_emailqu_table.setRowCount(0)
        self.user_emailqu_table.insertRow(0)
        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.user_emailqu_table.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1
            row_position = self.user_emailqu_table.rowCount()
            self.user_emailqu_table.insertRow(row_position)

    def user_emailflushap_request(self):
        message = json.dumps(['request:用户邮箱预约刷新', self.username])
        print(message)
        self.client.send(message.encode('utf-8'))

    def user_emailflushap_response(self,data):
        self.user_emailap_table.setRowCount(0)
        self.user_emailap_table.insertRow(0)
        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.user_emailap_table.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1
            row_position = self.user_emailap_table.rowCount()
            self.user_emailap_table.insertRow(row_position)

    #专家界面
    #专家界面按钮设置
    def bth_expert(self):
        self.expert_flush.clicked.connect(self.expert_flush_request)
        self.expert_updatesex.clicked.connect(self.expert_updatesex_request)
        self.expert_updateem.clicked.connect(self.expert_updateem_request)
        self.expert_updatepw.clicked.connect(self.expert_updatepw_request)
        self.expert_updatebd.clicked.connect(self.expert_updatebd_request)
        self.expert_updateor.clicked.connect(self.expert_updateor_request)
        self.expert_updatede.clicked.connect(self.expert_updatede_request)
        self.expert_flushq.clicked.connect(self.expert_flushq_request)
        self.expert_flusha.clicked.connect(self.expert_flusha_request)
        self.expert_showq.clicked.connect(self.expert_showq_request)
        self.expert_showa.clicked.connect(self.expert_showa_request)
        self.expert_responsereset.clicked.connect(self.reset)
        self.expert_response.clicked.connect(self.expert_response_request)
        self.expert_accept.clicked.connect(self.expert_accept_request)
        self.expert_reject.clicked.connect(self.expert_reject_request)
        self.expert_qutable.clicked.connect(self.expert_qutable_request)
        self.expert_aptable.clicked.connect(self.expert_aptable_request)



    def expert_response_request(self):
        selectItem = self.expert_userq.selectedItems()
        if selectItem:
            qa_id = selectItem[0].text()
            resp = self.expert_responsesend.toPlainText()
            message = json.dumps(['request:专家回复', qa_id, resp])
            self.client.send(message.encode())

    def expert_response_response(self):
        self.Regit_Error.setText('回复成功!感想您的解惑~')

    def expert_showq_request(self):
        selectItem = self.expert_userq.selectedItems()
        if selectItem:
            qa_id = selectItem[0].text()
            message = json.dumps(['request:问题内容', qa_id])
            self.client.send(message.encode())

    def expert_showq_response(self,data):
        ans = data[0][0]
        self.expert_userquestion.setText(str(ans))

    def expert_showa_request(self):
        selectItem = self.expert_usera.selectedItems()
        if selectItem:
            qa_id = selectItem[0].text()
            message = json.dumps(['request:预约内容', qa_id])
            self.client.send(message.encode())

    def expert_showa_response(self,data):
        ans = data[0][0]
        self.expert_description.setText(str(ans))

    def expert_flushq_request(self):
        message = json.dumps(['request:显示用户问题',self.username])
        self.client.send(message.encode())

    def expert_flushq_response(self, data):
        self.expert_userq.setRowCount(0)
        self.expert_userq.insertRow(0)
        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.expert_userq.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1
            row_position = self.expert_userq.rowCount()
            self.expert_userq.insertRow(row_position)

    def expert_flusha_request(self):
        message = json.dumps(['request:显示用户预约',self.username])
        self.client.send(message.encode())

    def expert_flusha_response(self, data):
        self.expert_usera.setRowCount(0)
        self.expert_usera.insertRow(0)
        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.expert_usera.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1
            row_position = self.expert_usera.rowCount()
            self.expert_usera.insertRow(row_position)

    def expert_flush_request(self):
        message = json.dumps(['request:显示专家个人信息', self.username, self.status])
        print(message)
        self.client.send(message.encode('utf-8'))

    def expert_flush_response(self, data):
        theid = data[0][0]
        username = data[0][1]
        name = data[0][2]
        email = data[0][3]
        sex = data[0][4]
        birthdate = data[0][5]
        organization = data[0][6]
        department = data[0][7]
        text = '用户id:%s \n用户名:%s \n姓名:%s \n邮箱:%s \n性别:%s \n出生日期:%s \n单位:%s \n科室:%s'\
               %(theid, username, name, email, sex, birthdate, organization, department)
        print(text)
        self.expert_inf_label.setText(text)

    def expert_updatesex_request(self):
        sex = self.expert_update_sex.currentText()
        message = json.dumps(['request:修改信息', self.status, 'sex', sex, self.username])
        self.client.send(message.encode())

    def expert_updatede_request(self):
        department = self.expert_update_de.currentText()
        message = json.dumps(['request:修改信息', self.status, 'department', department, self.username])
        self.client.send(message.encode())

    def expert_updateor_request(self):
        organization = self.expert_update_or.text().strip()
        if len(organization) < 1:
            self.Regit_Error.setText('请检查是否输入为空')
        else:
            message = json.dumps(['request:修改信息', self.status, 'organization', organization, self.username])
        self.client.send(message.encode())

    def expert_updateem_request(self):
        email = self.expert_update_email.text().strip()
        if len(email) < 1:
            self.Regit_Error.setText('请检查是否输入为空')
        else:
            message = json.dumps(['request:修改信息', self.status, 'email', email, self.username])
        self.client.send(message.encode())

    def expert_updatepw_request(self):
        pw = self.expert_update_password.text().strip()
        if len(pw) < 8:
            self.Regit_Error.setText('密码至少8位')
        else:
            message = json.dumps(['request:修改信息', self.status, 'password', pw, self.username])
        self.client.send(message.encode())

    def expert_updatebd_request(self):
        bd = self.expert_update_birthdate.dateTime().toString("yyyy-MM-dd")
        message = json.dumps(['request:修改信息', self.status, 'birthdate', bd, self.username])
        self.client.send(message.encode())

    def expert_accept_request(self):
        selectItem = self.expert_usera.selectedItems()
        if selectItem:
            qa_id = selectItem[0].text()
            message = json.dumps(['request:接受预约', qa_id])
            self.client.send(message.encode())

    def expert_reject_request(self):
        selectItem = self.expert_usera.selectedItems()
        if selectItem:
            qa_id = selectItem[0].text()
            message = json.dumps(['request:拒绝预约', qa_id])
            self.client.send(message.encode())

    def expert_accept_and_reject(self):
        self.Regit_Error.setText('处理成功!')

    def expert_qutable_request(self):
        message = json.dumps(['request:专家问题邮箱', self.username])
        self.client.send(message.encode('utf-8'))

    def expert_qutable_response(self, data):
        self.expert_emailqu.setRowCount(0)
        self.expert_emailqu.insertRow(0)
        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.expert_emailqu.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1
            row_position = self.expert_emailqu.rowCount()
            self.expert_emailqu.insertRow(row_position)


    def expert_aptable_request(self):
        message = json.dumps(['request:专家预约邮箱', self.username])
        self.client.send(message.encode('utf-8'))

    def expert_aptable_response(self, data):
        self.expert_emailap.setRowCount(0)
        self.expert_emailap.insertRow(0)
        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.expert_emailap.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1
            row_position = self.expert_emailqu.rowCount()
            self.expert_emailap.insertRow(row_position)

   #管理员界面
    #管理员界面按钮设置
    def bth_admin(self):
        self.user_inf_flush.clicked.connect(self.show_user_request)
        self.admin_user_add_button.clicked.connect(self.add_user_request)
        self.user_delete_button.clicked.connect(self.user_delete_request)
        self.user_activation_button.clicked.connect(self.user_active_request)
        self.user_banned_button.clicked.connect(self.user_freeze_request)
        self.user_resetpwd_botton.clicked.connect(self.user_resetpwd_request)
        self.expert_inf_flush.clicked.connect(self.show_expert_request)
        self.admin_expert_add_button.clicked.connect(self.add_expert_request)
        self.expert_delete_button.clicked.connect(self.expert_delete_request)
        self.expert_activation_button.clicked.connect(self.expert_active_request)
        self.expert_banned_button.clicked.connect(self.expert_freeze_request)
        self.expert_resetpwd_botton.clicked.connect(self.expert_resetpwd_request)

    #显示用户信息
    def show_user_request(self):
        message = json.dumps(['request:显示用户信息'])
        self.client.send(message.encode('utf-8'))

    def show_user_response(self, data):
        self.user_inf_table.setRowCount(0)
        self.user_inf_table.insertRow(0)
        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.user_inf_table.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1
            row_position = self.user_inf_table.rowCount()
            self.user_inf_table.insertRow(row_position)

    #发送添加用户信息请求
    def add_user_request(self):
        self.admin_user_add_message.setText('')
        if self.admin_user_add_handle_client():  # 客户端注册信息检测
            username = self.admin_user_add_username.text().strip()
            password = self.admin_user_add_password.text().strip()
            password = md5_code(password)  # 对密码进行加密处理
            email = self.admin_user_add_email.text().strip()
            sex = self.admin_user_add_sex.currentText()
            birthdate = self.admin_user_add_birthdate.dateTime().toString("yyyy-MM-dd")
            user_regit_inf = ['request:添加用户信息', username, password, email, sex, birthdate]
            print(user_regit_inf)
            message = json.dumps(user_regit_inf)
            self.client.send(message.encode())

    #客户端注册信息检查
    def admin_user_add_handle_client(self):
        if self.admin_user_add_password.text() != self.admin_user_add_passwordag.text():
            self.admin_user_add_message.setText('两次密码输入不一样，请检查')
            self.admin_user_add_passwordag.setText('')
            return 0
        if len(self.admin_user_add_password.text().strip()) < 8:
            self.admin_user_add_message.setText('密码需要至少8位，建议包含字母、数字和特殊字符')
            self.admin_user_add_password.setText('')
            self.admin_user_add_passwordag.setText('')
            return 0
        if self.admin_user_add_username.text().strip() == '':
            self.admin_user_add_message.setText('用户名不可以为空')
            return 0
        if self.admin_user_add_email.text().strip() == '':
            self.admin_user_add_message.setText('邮箱不可以为空')
            return 0
        email = self.admin_user_add_email.text().strip()
        if email[-4:] != '.com' and email[-3:] != '.en':
            self.admin_user_add_message.setText('邮箱格式无效')
            return 0
        return 1

    #处理添加用户信息请求结果
    def add_user_response(self, response):
        if response[1] == 'ok':
            print(response)
            self.admin_user_add_message.setText('添加信息成功!')
            self.show_user_request()
        else:
            self.admin_user_add_message.setText(response[2])

    #管理员发送删除用户请求
    def user_delete_request(self):
        selectItem = self.user_inf_table.selectedItems()
        if selectItem:
            user_id = selectItem[0].text()
            message = json.dumps(['request:删除用户',user_id])
            self.client.send(message.encode())

    #处理删除用户请求结果
    def user_delete_response(self):
        self.show_user_request()
        self.Regit_Error.setText('删除成功')

    #用户状态设置请求:激活与冻结
    def user_active_request(self):
        selectItem = self.user_inf_table.selectedItems()
        print(selectItem[0])
        if selectItem:
            user_id = selectItem[0].text()
            message = json.dumps(['request:用户状态', '激活', user_id])
            self.client.send(message.encode())

    def user_freeze_request(self):
        selectItem = self.user_inf_table.selectedItems()
        print(selectItem[0])
        if selectItem:
            user_id = selectItem[0].text()
            message = json.dumps(['request:用户状态', '冻结', user_id])
            self.client.send(message.encode())

    #重置用户密码
    def user_resetpwd_request(self):
        selectItem = self.user_inf_table.selectedItems()
        print(selectItem[0])
        if selectItem:
            user_id = selectItem[0].text()
            message = json.dumps(['request:重置密码', '用户', user_id])
            self.client.send(message.encode())

    #显示专家信息
    def show_expert_request(self):
        message = json.dumps(['request:显示专家信息'])
        print(message)
        self.client.send(message.encode('utf-8'))

    def show_expert_response(self, data):
        self.expert_inf_table.setRowCount(0)
        self.expert_inf_table.insertRow(0)
        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.expert_inf_table.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1
            row_position = self.expert_inf_table.rowCount()
            self.expert_inf_table.insertRow(row_position)

    #发送添加专家信息请求
    def add_expert_request(self):
        self.Regit_Error.setText('')
        if self.admin_expert_add_handle_client():  # 客户端注册信息检测
            username = self.admin_expert_add_username.text().strip()
            name = self.admin_expert_add_name.text().strip()
            password = self.admin_expert_add_password.text().strip()
            password = md5_code(password)  # 对密码进行加密处理
            email = self.admin_expert_add_email.text().strip()
            sex = self.admin_expert_add_sex.currentText()
            birthdate = self.admin_expert_add_birthdate.dateTime().toString("yyyy-MM-dd")
            organization = self.admin_expert_add_organization.text().strip()
            department = self.admin_expert_add_department.currentText()
            expert_regit_inf = ['request:添加专家信息', username, name, password, email, sex, birthdate, organization, department]
            print(expert_regit_inf)
            message = json.dumps(expert_regit_inf)
            self.client.send(message.encode())

    #客户端注册信息检查
    def admin_expert_add_handle_client(self):
        if self.admin_expert_add_password.text() != self.admin_expert_add_passwordag.text():
            self.Regit_Error.setText('两次密码输入不一样，请检查')
            self.admin_expert_add_passwordag.setText('')
            return 0
        if len(self.admin_expert_add_password.text().strip()) < 8:
            self.Regit_Error.setText('密码需要至少8位，\n建议包含字母、数字和特殊字符')
            self.admin_expert_add_password.setText('')
            self.admin_expert_add_passwordag.setText('')
            return 0
        if self.admin_expert_add_username.text().strip() == '':
            self.Regit_Error.setText('用户名不可以为空')
            return 0
        if self.admin_expert_add_email.text().strip() == '':
            self.Regit_Error.setText('邮箱不可以为空')
            return 0
        email = self.admin_expert_add_email.text().strip()
        if email[-4:] != '.com' and email[-3:] != '.en':
            self.Regit_Error.setText('邮箱格式无效')
            return 0
        return 1

    #处理添加专家信息请求结果
    def add_expert_response(self, response):
        if response[1] == 'ok':
            print(response)
            self.Regit_Error.setText('信息添加成功!')
            self.show_expert_request()
        else:
            self.Regit_Error.setText(response[2])

    #发送删除专家请求
    def expert_delete_request(self):
        selectItem = self.expert_inf_table.selectedItems()
        if selectItem:
            expert_id = selectItem[0].text()
            print(expert_id)
            message = json.dumps(['request:删除专家', expert_id])
            self.client.send(message.encode())

    #处理删除专家请求结果
    def expert_delete_response(self):
        self.Regit_Error.setText('删除成功')
        self.show_expert_request()

    #专家状态激活或冻结
    def expert_active_request(self):
        selectItem = self.expert_inf_table.selectedItems()
        print(selectItem[0])
        if selectItem:
            expert_id = selectItem[0].text()
            message = json.dumps(['request:专家状态', '激活', expert_id])
            self.client.send(message.encode())

    def expert_freeze_request(self):
        selectItem = self.expert_inf_table.selectedItems()
        print(selectItem[0])
        if selectItem:
            expert_id = selectItem[0].text()
            message = json.dumps(['request:专家状态', '冻结', expert_id])
            self.client.send(message.encode())

    #重置用户密码
    def expert_resetpwd_request(self):
        selectItem = self.expert_inf_table.selectedItems()
        print(selectItem[0])
        if selectItem:
            expert_id = selectItem[0].text()
            message = json.dumps(['request:重置密码', '专家', expert_id])
            self.client.send(message.encode())

    #处理用户\专家状态设置请求结果
    def active_response(self):
        self.Regit_Error.setText('状态更改成功!')
        self.show_user_request()
    #处理重置密码请求结果
    def resetpwd_response(self):
        self.Regit_Error.setText('密码重置成功!')

    #机器人发信息
    def robot_send(self):
        question = self.robot_message.toPlainText()
        choose = self.robot_choose.currentText()
        message = json.dumps(['request:机器人问题', question, choose])
        self.robot_answer.clear()
        self.client.send(message.encode())

    def reset(self):
        self.robot_message.clear()
        self.user_question.clear()
        self.user_ap.clear()
        self.expert_responsesend.clear()

    def robot_response(self, mes):
        self.robot_answer.append(mes)
        self.robot_answer.moveCursor(self.robot_answer.textCursor().End)

    #接收消息
    def recv_message(self):
        while True:
            try:
                response = self.client.recv(5120).decode()
                response = json.loads(response)
                print(response)
                if response[0] == 'response:登录信息':
                    self.login_handle_response(response)
                elif response[0] == 'response:用户注册信息':
                    self.user_regit_handle_response(response)
                elif response[0] == 'response:专家入驻信息':
                    self.expert_regit_handle_response(response)
                elif response[0] == 'response:显示用户信息':
                    print(response)
                    self.show_user_response(response[1])
                elif response[0] == 'response:显示专家信息':
                    self.show_expert_response(response[1])
                elif response[0] == 'response:添加用户信息':
                    self.add_user_response(response)
                elif response[0] == 'response:添加专家信息':
                    self.add_expert_response(response)
                elif response[0] == 'response:删除用户':
                    self.user_delete_response()
                elif response[0] == 'response:删除专家':
                    self.expert_delete_response()
                elif response[0] == 'response:用户状态' or response[0] == 'response:专家状态':
                    self.active_response()
                elif response[0] == 'response:重置密码':
                    self.resetpwd_response()
                elif response[0] == 'response:机器人问题':
                    self.robot_response(response[1])
                elif response[0] == 'response:显示用户个人信息':
                    self.user_flush_response(response[1])
                elif response[0] == 'response:显示专家个人信息':
                    self.expert_flush_response(response[1])
                elif response[0] == 'response:修改信息':
                    self.update_response(response)
                elif response[0] == 'response:用户界面显示专家信息':
                    self.user_expertflush_response(response[1])
                elif response[0] == 'response:搜索专家':
                    self.user_searchexpert_response(response)
                elif response[0] == 'response:用户提问':
                    self.user_expertsend_response()
                elif response[0] == 'response:用户邮箱问题刷新':
                    self.user_emailflushqu_response(response[1])
                elif response[0] == 'response:用户邮箱预约刷新':
                    self.user_emailflushap_response(response[1])
                elif response[0] == 'response:用户预约':
                    self.user_expertsend_response()
                elif response[0] == 'response:显示用户问题':
                    self.expert_flushq_response(response[1])
                elif response[0] == 'response:显示用户预约':
                    self.expert_flusha_response(response[1])
                elif response[0] == 'response:问题内容':
                    self.expert_showq_response(response[1])
                elif response[0] == 'response:预约内容':
                    self.expert_showa_response(response[1])
                elif response[0] == 'response:专家回复':
                    self.expert_response_response()
                elif response[0] == 'response:专家处理预约':
                    self.expert_accept_and_reject()
                elif response[0] == 'response:专家处理预约':
                    self.expert_accept_and_reject()
                elif response[0] == 'response:专家问题邮箱':
                    self.expert_qutable_response(response[1])
                elif response[0] == 'response:专家预约邮箱':
                    self.expert_aptable_response(response[1])

            except:
                continue

    #处理服务器发回的登录信息
    def login_handle_response(self, response):
        if response[1] == 'ok':
            print('ok')
            if response[2] == '0':
                self.user_flush_request()
                self.Clear_widget()
                self.tabWidget.setCurrentIndex(1)  # 切换到用户界面

            elif response[2] == '1':
                self.status = '专家'
                self.expert_flush_request()
                self.Clear_widget()
                self.tabWidget.setCurrentIndex(2)#切换到专家界面
            else:
                self.show_user_request()  # 发送用户信息展示请求
                self.show_expert_request()
                self.Clear_widget()
                self.status = '管理员'
                self.tabWidget.setCurrentIndex(3)#切换到管理员界面
        if response[1] == 'error':
            self.Login_Error.setText(str(response[2]))

    #处理服务器发回的注册信息
    def user_regit_handle_response(self, response):#用户
        if response[1] == 'ok':
            self.Regit_Error.setText('注册成功，点击右下方按钮可返回登录界面')
            print('ok')
        else:
            self.Regit_Error.setText(response[2])

    def expert_regit_handle_response(self, response):#专家
        if response[1] == 'ok':
            self.Regit_Error.setText('入驻成功!点击右下方按钮可返回登录界面\n'
                                     '当前专家账号为未激活状态，请等待管理员激活')
        else:
            self.Regit_Error.setText(response[2])


#md5 加密
def md5_code(password):
    hash = hashlib.md5(bytes("疑问医答", encoding="utf-8"))  # md5加密
    hash.update(bytes(password, encoding='utf-8'))
    password = hash.hexdigest()  # 对密码进行加密处理
    return password

#主函数
def main():
    app = QApplication([])
    wind = Client_window()
    wind.show()
    app.exec_()

if __name__ == '__main__':
    main()
