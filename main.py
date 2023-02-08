import argparse
import sys

from PyQt5.QtWidgets import QApplication

from manage.loaddata import loaddata
from manage.init_database import check_create_db
from users.sign_in.sign_in_widget import SignInWidget


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


parser = argparse.ArgumentParser()
parser.add_argument(
    '--loaddata',
    help='load data from fixture to your database'
)
args = parser.parse_args()

if args.loaddata is not None:
    loaddata(args.loaddata)

if __name__ == '__main__' and args.loaddata is None:
    check_create_db()
    app = QApplication(sys.argv)
    ex = SignInWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
