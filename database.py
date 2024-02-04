import sqlite3
import os
import shutil


app_data_location = os.path.join(os.getenv('APPDATA'), 'MkReman', 'Share App')
if not os.path.exists(os.path.join(app_data_location, 'DataBase.db')):
    os.makedirs(app_data_location)
    shutil.copy('./DataBase.db', os.path.join(app_data_location, 'DataBase.db'))

conn = sqlite3.connect(os.path.join(app_data_location, 'DataBase.db'))
c = conn.cursor()


# c.execute("""CREATE TABLE Members (
#             Name text,
#             Email text
#             )""")
# c.execute("""CREATE TABLE Profile (
#             Variables text,
#             Entries text
#             )""")
# c.execute("""CREATE TABLE LightTheme (
#             Variables text,
#             Entries text
#             )""")
# c.execute("""CREATE TABLE DarkTheme (
#             Variables text,
#             Entries text
#             )""")


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

# inset data in DataBase
# Database.insert_member('mayank', 'mkreman12@gmail.com')
# Database.insert_member('mk', 'nmayank1998@gmail.com')

# to update email
# Database.update_email(name, email)

# get email of name
# inv = Database.get_by_name('mk')
# print(inv)

# to delete any Members
# Database.remove_inv('')

# Database.insert_profile_value('name_idx', 'mayank')
# Database.insert_profile_value('user_email', 'mkreman12@gmail.com')
# Database.insert_profile_value('email_password_idx', 'exizpkzgapqarksk')
# Database.insert_profile_value('phone_number', '9829206585')
# Database.insert_profile_value('upi_id', 'mkreman@ybl,mkreman@paytm,mayanknagar18011998@oksbi')
# Database.update_profile_value('theme', 'LightTheme')
#
# Database.insert_theme_value('LightTheme', 'fg_color', '#000000')
# Database.insert_theme_value('LightTheme', 'label_fg_color', '#000000')
# Database.insert_theme_value('LightTheme', 'entry_bg_color', '#f2f2f2')
# Database.update_theme_value('LightTheme', 'bg_color', '#e3e3e3')
# Database.insert_theme_value('LightTheme', 'font', 'Cambria')
# Database.insert_theme_value('LightTheme', 'button_size', '12')
# Database.insert_theme_value('LightTheme', 'font_size', '14')

# Database.update_theme_value('DarkTheme', 'fg_color', 'white')
# Database.insert_theme_value('DarkTheme', 'label_fg_color', 'white')
# Database.insert_theme_value('DarkTheme', 'entry_bg_color', '#525252')
# Database.insert_theme_value('DarkTheme', 'bg_color', "#2e2e2e")
# Database.insert_theme_value('DarkTheme', 'font', 'Cambria')
# Database.insert_theme_value('DarkTheme', 'button_size', '12')
# Database.insert_theme_value('DarkTheme', 'font_size', '14')

# Print all meta values
# print(get_members())
# print(get_variable_values())

# Print all values in DarkTheme table
# print(c.execute("SELECT * FROM DarkTheme").fetchall())

# Print all tables in dataset
# c.execute("SELECT name FROM sqlite_master WHERE type='table';")
# print(c.fetchall())
