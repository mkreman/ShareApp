import sqlite3
import os
import shutil


app_data_location = os.path.join(os.getenv('APPDATA'), 'MkReman', 'Share App')
if not os.path.exists(os.path.join(app_data_location, 'DataBase.db')):
    os.makedirs(app_data_location)
    shutil.copy('./DataBase.db', os.path.join(app_data_location, 'DataBase.db'))

conn = sqlite3.connect(os.path.join(app_data_location, 'DataBase.db'))
c = conn.cursor()


def get_members():
    return {x[0]: x[1] for x in c.execute("SELECT * from Members")}


def get_variable_values():
    return {x[0]: x[1] for x in c.execute("SELECT * from Profile")}


def get_theme_values(theme):
    return {x[0]: x[1] for x in c.execute(f"SELECT * from {theme}")}


class Database:
    font_list = sorted(['Arial', 'Cambria', 'Segoe UI', 'Segoe Script', 'Sitka Text', 'Times New Roman',
                                 'Imprint MT Shadow'])

    @staticmethod
    def insert_member(name, email):
        with conn:
            c.execute("INSERT INTO Members VALUES (:name, :email)", {'name': name, 'email': email})

    @staticmethod
    def get_member_by_name(name):
        c.execute("SELECT * FROM Members WHERE name=:name", {'name': name})
        return c.fetchall()

    @staticmethod
    def update_email(name, email):
        with conn:
            c.execute("""UPDATE Members SET email = :email WHERE name = :name""", {'name': name, 'email': email})

    @staticmethod
    def remove_member(name):
        with conn:
            c.execute("DELETE from Members WHERE name = :name", {'name': name})

    @staticmethod
    def insert_profile_value(variable, entry):
        with conn:
            c.execute("INSERT INTO Profile VALUES (:variable, :entry)", {'variable': variable, 'entry': entry})

    @staticmethod
    def update_profile_value(variable, entry):
        with conn:
            c.execute("""UPDATE Profile SET entries = :entry WHERE Variables = :variable""",
                      {'variable': variable, 'entry': entry})

    @staticmethod
    def remove_profile_value(variable):
        with conn:
            c.execute("DELETE from Profile WHERE Variables = :variable", {'variable': variable})

    @staticmethod
    def insert_theme_value(theme, variable, entry):
        with conn:
            command = f"INSERT INTO {theme} VALUES (:variable, :entry)"
            c.execute(command, {'variable': variable, 'entry': entry})

    @staticmethod
    def update_theme_value(theme, variable, entry):
        with conn:
            command = f"UPDATE {theme} SET entries = :entry WHERE Variables = :variable"
            c.execute(command, {'variable': variable, 'entry': entry})

    @staticmethod
    def remove_theme_value(theme, variable):
        with conn:
            command = f"DELETE from {theme} WHERE Variables = :variable"
            c.execute(command, {'variable': variable})
