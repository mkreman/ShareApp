import sqlite3
import os
import shutil


app_data_location = os.path.join(os.getenv('APPDATA'), 'MkReman', 'Share App')
if not os.path.exists(os.path.join(app_data_location, 'DataBase.db')):
    os.makedirs(app_data_location)
    shutil.copy('./DataBase.db', os.path.join(app_data_location, 'DataBase.db'))

conn = sqlite3.connect(os.path.join(app_data_location, 'DataBase.db'))
c = conn.cursor()


def members():
    inves = dict()
    for inv in c.execute("SELECT * from investors"):
        inves[inv[0]] = inv[1]
    return inves


def get_variable_values():
    res = dict()
    for x in c.execute("SELECT * from meta_values"):
        res[x[0]] = x[1]
    return res


class Database:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def insert_member(self):
        with conn:
            c.execute("INSERT INTO investors VALUES (:name, :email)", {'name': self.name, 'email': self.email})

    @staticmethod
    def get_member_by_name(name):
        c.execute("SELECT * FROM investors WHERE name=:name", {'name': name})
        return c.fetchall()

    @staticmethod
    def update_email(name, email):
        with conn:
            c.execute("""UPDATE investors SET email = :email
                WHERE name = :name""",
                      {'name': name, 'email': email})

    @staticmethod
    def remove_member(name):
        with conn:
            c.execute("DELETE from investors WHERE name = :name", {'name': name})

    @staticmethod
    def insert_meta_value(variable, entry):
        with conn:
            c.execute("INSERT INTO meta_values VALUES (:variable, :entry)", {'variable': variable,
                                                                             'entry': entry})

    @staticmethod
    def update_meta_value(variable, entry):
        with conn:
            c.execute("""UPDATE meta_values SET entries = :entry
                    WHERE Variables = :variable""",
                      {'variable': variable, 'entry': entry})

    @staticmethod
    def remove_meta_values(variable):
        with conn:
            c.execute("DELETE from meta_values WHERE Variables = :variable", {'variable': variable})
