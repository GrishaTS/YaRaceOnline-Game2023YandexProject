import sys
from PyQt5.QtWidgets import QApplication
from users.sign_up.sign_up_widget import SignUpWidget
from users.sign_in.sign_in_widget import SignInWidget
from users.recovery.recovery_widget import RecoveryWidget
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RecoveryWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())