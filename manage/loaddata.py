import json
import sqlite3

from core.exceptions import FixtureError
from settings import DATABASE


class Model:
    @staticmethod
    def insert_garage(*, table, data):
        con = sqlite3.connect(DATABASE)
        request = f'''INSERT INTO {table}
                          (id, model, photo,
                          price, velocity, x, y)
                      VALUES
                          ('{data[0]}', '{data[1]}',
                          '{data[2]}', '{data[3]}',
                          '{data[4]}', '{data[5]}',
                          '{data[6]}')
                       '''
        con.execute(request)
        con.commit()


def loaddata(file):
    if not file.endswith('.json'):
        raise FixtureError('Only load file with json extension')
    with open(file) as reading_file:
        data = json.load(reading_file)
        for entry in data:
            fields = [entry['pk']] + list(entry['fields'].values())
            Model().insert_garage(table=entry['model'], data=fields)
