import sqlite3
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
import zadacha
import sys

db_name = sqlite3.connect('database.db')
cur = db_name.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS users(login TEXT, password TEXT)''')
db_name.commit()


class Registration(QtWidgets.QMainWindow, zadacha.Ui_MainWindow):
    def __init__(self):
        super(Registration, self).__init__()
        self.setupUi(self)
        self.label.setText('')
        self.label_2.setText('Регистрация')
        self.lineEdit.setPlaceholderText('Введите логин...')
        self.lineEdit_2.setPlaceholderText('Введите пароль...')
        self.pushButton.setText('Регистрация')
        self.pushButton_2.setText('Вход')
        self.setWindowTitle('Авторизация')
        self.pushButton.pressed.connect(self.Registr)
        self.pushButton_2.pressed.connect(self.login)

    def login(self):
        self.login = Login()
        self.login.show()
        self.hide()

    def Registr(self):
        login1 = self.lineEdit.text()
        password1 = self.lineEdit_2.text()
        if len(login1) == 0 or len(password1) == 0:
            return
        cur.execute(f'SELECT login FROM users WHERE login = "{login1}"')
        if cur.fetchone() is None:
            cur.execute(f'INSERT INTO users VALUES ("{login1}", "{password1}")')
            self.label.setText(f'Аккаунт {login1} успешно зарегистрирован.')
            db_name.commit()
        else:
            self.label.setText('Такой аккаунт уже зарегистрирован.')


class Login(QtWidgets.QMainWindow, zadacha.Ui_MainWindow):
    def __init__(self):
        super(Login, self).__init__()
        self.setupUi(self)
        self.label.setText('')
        self.label_2.setText('Вход')
        self.lineEdit.setPlaceholderText('Введите логин...')
        self.lineEdit_2.setPlaceholderText('Введите пароль...')
        self.pushButton.setText('Регистрация')
        self.pushButton_2.setText('Вход')
        self.setWindowTitle('Авторизация')
        self.pushButton.pressed.connect(self.login)
        self.pushButton_2.pressed.connect(self.Registr)

    def Registr(self):
        self.Registr = Registration()
        self.Registr.show()
        self.hide()

    def login(self):
        login1 = self.lineEdit.text()
        password1 = self.lineEdit_2.text()
        if len(login1) == 0 or len(password1) == 0:
            return
        cur.execute(f'SELECT password FROM users WHERE login = "{login1}"')
        check_password = cur.fetchall()
        cur.execute(f'SELECT password FROM users WHERE login = "{login1}"')
        check_login = cur.fetchall()
        if check_password[0][0] == password1 and check_login[0][0] == login1:
            self.label.setText('Успешная авторизация')
        else:
            self.label.setText('Ошибка авторизации')


app = QApplication([])
ex = Login()
ex.show()
app.exec()