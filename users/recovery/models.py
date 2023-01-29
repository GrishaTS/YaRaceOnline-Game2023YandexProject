import sqlite3

from settings import DATABASE


class UserModel:
    @staticmethod
    def update_password_of_the_user(*, login, password):
        con = sqlite3.connect(DATABASE)
        request = f'''UPDATE user
                      SET password = '{password}'
                      WHERE login = '{login}'
                   '''
        con.execute(request)
        con.commit()

    @staticmethod
    def select_all_user_data(*, login):
        con = sqlite3.connect(DATABASE)
        request = f'''SELECT * FROM user
                      WHERE login = '{login}'
                   '''
        data = con.execute(request).fetchall()
        con.commit()
        return data

    @staticmethod
    def select_user_login(*, login):
        con = sqlite3.connect(DATABASE)
        request = f'''
                      SELECT login
                      FROM user
                      WHERE login = '{login}'
                   '''
        data = con.execute(request).fetchall()
        con.commit()
        return data


users_model = UserModel()
