import sqlite3

from settings import DATABASE


class UsersModel:
    @staticmethod
    def insert_new_user(*, login, password):
        con = sqlite3.connect(DATABASE)
        request = f'''INSERT INTO users
                          ('login', 'password')
                      VALUES ('{login}', '{password}')
                   '''
        con.execute(request)
        con.commit()


users_model = UsersModel()