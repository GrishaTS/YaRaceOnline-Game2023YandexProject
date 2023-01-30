import sqlite3

from settings import DATABASE


class UserModel:
    @staticmethod
    def select_user(*, login):
        con = sqlite3.connect(DATABASE)
        request = f''' SELECT
                          coins, music, sounds,
                          record, password
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
                          ('login', 'password')
                      VALUES ('{login}', '{password}')
                   '''
        con.execute(request)
        con.commit()


users_model = UserModel()


class User:
    def __init__(self, login):
        self.login = login
        user_data = users_model.select_user(login=login)
        error_message = (
            'There is not user with such login'
            'or there are more than one user with such login'
        )
        assert len(user_data) == 1, error_message
        user_data = user_data[0]
        self.user_data = user_data
        self.coins = user_data[0]
        self.music = user_data[1]
        self.sounds = user_data[2]
        self.record = user_data[3]
        self.password = user_data[4]

    def __setitem__(self, key, value):
        self.__dict__[key] = value
        users_model.update_user(login=self.login, key=key, value=value)

    def __delitem__(self, key):
        users_model.delete_user(login=self.login)
        del self.__dict__[key]

    @property
    def all_data(self):
        return self.user_data

user1 = User('admin123')
user1.sounds = 6
print(user1.sounds, type(user.sounds))