import os
import sqlite3

from settings import DATABASE


class CreateTables:
    @staticmethod
    def create_user_table():
        con = sqlite3.connect(DATABASE)
        request = '''CREATE TABLE user (
            id              INTEGER PRIMARY KEY AUTOINCREMENT
                                    UNIQUE
                                    NOT NULL,
            login           VARCHAR UNIQUE
                                    NOT NULL,
            coins           INTEGER,
            record          TIME,
            password        VARCHAR NOT NULL,
            selected_car    INTEGER REFERENCES garage (id),
            selected_music  INTEGER CHECK (selected_music >= 0 AND
                                        selected_music < 11),
            selected_sounds INTEGER CHECK (selected_sounds >= 0 AND
                                        selected_sounds < 11)
        )
        '''
        con.execute(request)
        con.commit()

    @staticmethod
    def create_garage_table():
        con = sqlite3.connect(DATABASE)
        request = '''CREATE TABLE garage (
            id       INTEGER PRIMARY KEY AUTOINCREMENT
                            UNIQUE
                            NOT NULL,
            model    VARCHAR UNIQUE
                            NOT NULL,
            photo            NOT NULL,
            price    INTEGER,
            velocity INTEGER,
            x        INTEGER,
            y        INTEGER
        )
        '''
        con.execute(request)
        con.commit()

    @staticmethod
    def create_user_garage_table():
        con = sqlite3.connect(DATABASE)
        request = '''CREATE TABLE user_garage (
            id        INTEGER PRIMARY KEY AUTOINCREMENT
                            UNIQUE
                            NOT NULL,
            user_id   BIGINT  REFERENCES user (id) ON DELETE CASCADE
                            NOT NULL,
            garage_id BIGINT  REFERENCES garage (id) ON DELETE CASCADE
                            NOT NULL
        )
        '''
        con.execute(request)
        con.commit()


def check_create_db():
    if not os.path.exists('db.sqlite3'):
        open(DATABASE, 'x')
        CreateTables.create_user_table()
        CreateTables.create_garage_table()
        CreateTables.create_user_garage_table()
