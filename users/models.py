import sqlite3

from settings import DATABASE


class UserModel:
    @staticmethod
    def select_user(*, login):
        con = sqlite3.connect(DATABASE)
        request = f''' SELECT
                          id, coins, record, selected_car, password,
                          selected_music, selected_sounds
                      FROM user
                      WHERE login = '{login}'
                   '''
        data = con.execute(request).fetchall()
        con.commit()
        return data

    @staticmethod
    def select_user_value(*, key, value):
        con = sqlite3.connect(DATABASE)
        request = f'''SELECT
                          {key}
                      FROM user
                      WHERE {key} = '{value}'
                   '''
        data = con.execute(request).fetchall()
        con.commit()
        return data

    @staticmethod
    def select_user_id(*, login):
        con = sqlite3.connect(DATABASE)
        request = f'''SELECT
                          id
                      FROM user
                      WHERE login = '{login}'
                  '''
        data = con.execute(request).fetchall()
        con.commit()
        return data

    @staticmethod
    def update_user(*, login, key, value):
        con = sqlite3.connect(DATABASE)
        request = f'''UPDATE user
                      SET {key} = '{value}'
                      WHERE login = '{login}'
                   '''
        con.execute(request)
        con.commit()

    @staticmethod
    def delete_user(*, login):
        con = sqlite3.connect(DATABASE)
        request = f'''DELETE user
                      WHERE login = '{login}'
                    '''
        con.execute(request)
        con.commit()

    @staticmethod
    def insert_user(*, login, password):
        con = sqlite3.connect(DATABASE)
        request = f'''INSERT INTO user
                          ('login', 'password', selected_car, coins,
                           selected_music, selected_sounds, record)
                      VALUES ('{login}', '{password}', 1, 0, 5, 5, 0)
                   '''
        con.execute(request)
        con.commit()
        UserModel.insert_user_garage(login=login)

    @staticmethod
    def insert_user_garage(*, login):
        con = sqlite3.connect(DATABASE)
        user_id = UserModel.select_user_id(login=login)[0][0]
        request = f'''INSERT INTO user_garage
                         (user_id, garage_id)
                      VALUES ({user_id}, 1)
                   '''
        con.execute(request)
        con.commit()


users_model = UserModel()


class User:
    def __init__(self, login):
        self.login = login
        user_data = users_model.select_user(login=login)
        attribute = [
            'id', 'coins', 'record', 'selected_car', 'password',
            'selected_music', 'selected_sounds',
        ]
        try:
            user_data = user_data[0]
            self.user_data = user_data
            for i in range(len(attribute)):
                self.__dict__[attribute[i]] = user_data[i]
        except LookupError:
            self.user_data = user_data

    def __setitem__(self, key, value):
        self.__dict__[key] = value
        users_model.update_user(login=self.login, key=key, value=value)

    def __delitem__(self, key):
        users_model.delete_user(login=self.login)
        del self.__dict__[key]

    @property
    def all_data(self):
        return self.user_data
