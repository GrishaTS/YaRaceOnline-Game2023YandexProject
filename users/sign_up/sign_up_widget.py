import sqlite3

from PyQt5.QtWidgets import QLineEdit, QMainWindow, QMessageBox

from core.exceptions import ValidationError
from core.validators import validate_password
from homepage.screensaver import homepage
from settings import DATABASE
from users.models import User, users_model
from users.sign_up.templates.sign_up_template import Ui_SigningUp
from users.sign_up.validators import validate_agreement, validate_login


class SignUpWidget(QMainWindow, Ui_SigningUp):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.password_sign_up_edit.setEchoMode(QLineEdit.Password)
        self.password2_sign_up_edit.setEchoMode(QLineEdit.Password)
        self.sign_up_confirm_button.clicked.connect(self.registrate_user)
        self.password_sign_up_edit.setPlaceholderText('Enter the password')
        self.password2_sign_up_edit.setPlaceholderText('Repeat the password')
        self.form = None

    def registrate_user(self):
        con = sqlite3.connect(DATABASE)
        login = self.login_sign_up_edit.text()
        password1 = self.password_sign_up_edit.text()
        password2 = self.password2_sign_up_edit.text()
        agreement = self.confirm_personal_data_checkbox.isChecked()
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
        agreement = self.validate_show_message(
            agreement,
            validate_func=validate_agreement,
        )
        if any(x is None for x in (login, password, agreement)):
            return

        users_model.insert_user(
            login=login,
            password=password,
        )
        con.commit()
        self.hide()
        homepage(user)

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
