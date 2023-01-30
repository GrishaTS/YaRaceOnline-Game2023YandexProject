from PyQt5.QtWidgets import QLineEdit, QMainWindow, QMessageBox

from homepage.screensaver import homepage
from users.models import User
from users.recovery.recovery_widget import RecoveryWidget
from users.sign_in.templates.sign_in_template import Ui_SigningIn
from users.sign_up.sign_up_widget import SignUpWidget


class SignInWidget(QMainWindow, Ui_SigningIn):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.sign_in_button.clicked.connect(self.sign_in)
        self.sign_up_button.clicked.connect(self.sign_up)
        self.forgot_password_button.clicked.connect(self.recovery)
        self.password_sign_in_edit.setEchoMode(QLineEdit.Password)
        self.form = None

    def sign_in(self):
        login = self.login_sign_in_edit.text()
        password = self.password_sign_in_edit.text()
        user = User(login)
        data = user.all_data

        if not data:
            QMessageBox.warning(
                self,
                'Error',
                'You aren\'t registered',
                QMessageBox.Ok,
            )
            return

        if data[4] != password:
            QMessageBox.warning(
                self,
                'Error',
                'Wrong password',
                QMessageBox.Ok,
            )
            return

        user_data = ...
        homepage(user_data)
        self.hide()

    def sign_up(self):
        self.form = SignUpWidget()
        self.form.show()
        self.hide()

    def recovery(self):
        self.form = RecoveryWidget()
        self.form.show()
        self.hide()
