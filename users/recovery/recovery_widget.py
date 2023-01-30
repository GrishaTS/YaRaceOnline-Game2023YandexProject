import sqlite3

from PyQt5.QtWidgets import QLineEdit, QMainWindow, QMessageBox

from settings import DATABASE

from core.exceptions import ValidationError
from users.recovery.models import users_model
from users.recovery.templates.recovery_template import Ui_Recovery
from users.recovery.validators import validate_login
from core.validators import validate_password


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

        users_model.update_password_of_the_user(login=login, password=password)

        data = users_model.select_all_user_data(login=login)
        # homepage(login=data[0][1])
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
