import sqlite3

class DatabaseQuery:
    def __init__(self, db_name):
        self.db_name = db_name

    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS users ( userid VARCHAR(8) NOT NULL, status VARCHAR(8) NOT NULL DEFAULT "clean", user_to_chat VARCHAR(8), chat_status VARCHAR(20) NOT NULL DEFAULT "not active", photo BOOLEAN NOT NULL DEFAULT "TRUE", age INT(3) DEFAULT NULL, gender VARCHAR(1) DEFAULT NULL);')
        conn.commit()
        conn.close()

    def register_user(self, chat_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE userid = '{}'".format(chat_id)).fetchone()[0]
        except:
            cursor.execute("INSERT INTO users (userid) VALUES ('{}')".format(chat_id))
            conn.commit()
        conn.close()

    def active_user(self, chat_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET chat_status = 'active' WHERE userid = '{}'".format(chat_id))
        conn.commit()
        conn.close()

    def check_connect(self, chat_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        user_to_chat = cursor.execute("SELECT userid FROM users WHERE chat_status = 'active' AND NOT userid = '{}'".format(chat_id)).fetchone()
        if user_to_chat:
            cursor.execute("UPDATE users SET chat_status = 'occuped', user_to_chat = '{}' WHERE userid = '{}'".format(user_to_chat[0], chat_id))
            cursor.execute("UPDATE users SET chat_status = 'occuped', user_to_chat = '{}' WHERE userid = '{}'".format(chat_id, user_to_chat[0]))
            conn.commit()
            conn.close()
            return True
        else:
            conn.close()
            return False

    def end_conversation(self, chat_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET chat_status = 'not active', user_to_chat = 'NULL' WHERE userid = '{}'".format(chat_id))
        cursor.execute("UPDATE users SET chat_status = 'not active', user_to_chat = 'NULL' WHERE user_to_chat = '{}'".format(chat_id))
        conn.commit()
        conn.close()

    def set_pics(self, chat_id, opt):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET photo = '{}' WHERE userid = '{}'".format(opt, chat_id))
        conn.commit()
        conn.close()

    def check_pics(self, chat_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        check = cursor.execute("SELECT photo FROM users WHERE userid = '{}'".format(chat_id)).fetchone()[0]
        conn.close()
        return check

    def get_user_to_chat(self, chat_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            check = cursor.execute("SELECT user_to_chat FROM users WHERE userid = '{}'".format(chat_id)).fetchone()[0]
            conn.close()
            if check:
                return check
            else:
                return 0
        except:
            conn.close()
            return 0

    def get_chat_status(self, chat_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        status = cursor.execute("SELECT chat_status FROM users WHERE userid = '{}'".format(chat_id)).fetchone()[0]
        conn.close()
        return status
