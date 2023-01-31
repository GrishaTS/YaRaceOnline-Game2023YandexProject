import sqlite3

from PyQt5.QtWidgets import QLineEdit, QMainWindow, QMessageBox

from core.exceptions import ValidationError
from core.validators import validate_password
from homepage.screensaver import homepage
from settings import DATABASE
from users.models import User
from users.recovery.templates.recovery_template import Ui_Recovery
from users.recovery.validators import validate_login


class RecoveryWidget(QMainWindow, Ui_Recovery):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.password_recovery_edit.setPlaceholderText('Enter new password')
        self.password2_recovery_edit.setPlaceholderText('Repeat the password')
        self.password_recovery_edit.setEchoMode(QLineEdit.Password)
        self.password2_recovery_edit.setEchoMode(QLineEdit.Password)
        self.recovery_button.clicked.connect(self.recovery)
        self.form = None

    def recovery(self):
        con = sqlite3.connect(DATABASE)
        login = self.login_recovery_edit.text()
        password1 = self.password_recovery_edit.text()
        password2 = self.password2_recovery_edit.text()
        user = User(login)

        login = self.validate_show_message(
            login,
            validate_func=validate_login,
            con=con,
        )
        password = self.validate_show_message(
            password1,
            password2,
            validate_func=validate_password,
        )
        if any(x is None for x in (login, password)):
            return
        user['password'] = password
        user = User(login)
        data = user.all_data
        homepage(data)
        self.hide()

    def validate_show_message(self, *data, validate_func, con=None):
        try:
            data = validate_func(*data, con)
        except ValidationError as e:
            QMessageBox.warning(
                self,
                'Error',
                str(e),
                QMessageBox.Ok,
            )
            return
        return data
