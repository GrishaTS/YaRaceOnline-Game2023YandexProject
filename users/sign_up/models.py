import sqlite3

from settings import DATABASE


class UserModel:
    @staticmethod
    def insert_new_user(*, login, password):
        con = sqlite3.connect(DATABASE)
        request = f'''
                      INSERT INTO user
                          ('login', 'password')
                      VALUES ('{login}', '{password}')
                   '''
        con.execute(request)
        con.commit()

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