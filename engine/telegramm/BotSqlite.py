import sqlite3
import os

class BotSqlite:

    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def get_user_likes(self, user_id):
        """Получает количество лайков у пользователя."""
        res = self.cursor.execute("SELECT likes FROM pik_users WHERE user_id='{}'".format(user_id))
        res = res.fetchone()
        if res:
            return res[0]

    def add_carma(self, username, count):
        if username[0] != '@':
            username = '@' + username
        self.cursor.execute("UPDATE Likes SET likes = (SELECT SUM(likes) FROM Likes WHERE username='{}') + {} WHERE username= '{}'".format(username, count, username))
        self.conn.commit()

    def substract_carma(self, username, count):
        if username[0] != '@':
            username = '@' + username
        self.cursor.execute("UPDATE Likes SET likes = (SELECT SUM(likes) FROM Likes WHERE username='{}') - {} WHERE username= '{}'".format(username, count, username))
        self.conn.commit()

    def nulify_carma(self, username):
        if username[0] != '@':
            username = '@' + username
        self.cursor.execute("UPDATE Likes SET likes = 0 WHERE username= '{}'".format(username))
        self.conn.commit()

    def get_top(self, count=10):
        res = self.cursor.execute("SELECT username, first_name, last_name, likes FROM pik_users ORDER BY likes DESC LIMIT 10")
        res = res.fetchall()
        new_res = []
        for i in res:
            if res[0]:
                new_res.append((i[0], i[3]))
            else:
                new_res.append((i[1] + ' ' + i[2], i[3]))
        return new_res

    def get_param(self, par_name):
        res = self.cursor.execute("SELECT val_int FROM  system_variable  WHERE name = '{}'".format(par_name))
        if res:
            return res.fetchone()[0]

    def set_param(self, par_name, number):
        res = self.cursor.execute("UPDATE system_variable SET val_int = {} WHERE name = '{}'".format(number, par_name))
        self.conn.commit()

    def save_user(self, upd):
        if not self.user_is_exists(upd.sender_id):
            print("Сохранен пользователь {} {} {} {}".format(upd.sender_id, upd.username, upd.first_name, upd.last_name))
        else:
            print("Обновлен пользователь {} {} {} {}".format(upd.sender_id, upd.username, upd.first_name, upd.last_name))
        self.cursor.execute("""
            INSERT OR REPLACE INTO pik_users ('user_id', 'username', 'first_name', 'last_name', 'likes')
                                  VALUES ('{0}', '{1}', '{2}', '{3}', 
                                  (SELECT likes FROM pik_users WHERE user_id={0}))
            """.format(upd.sender_id, upd.username, upd.first_name, upd.last_name))
        self.conn.commit()

    def user_is_exists(self, user_id):
        res = self.cursor.execute("""
                SELECT 1 FROM pik_users WHERE user_id = {}
            """.format(user_id))
        if res.fetchone():
            return True

    def get_user_email(self, user_id):
        """Есть ли у пользователя e-mail."""
        res = self.cursor.execute("""
                SELECT email FROM pik_users WHERE user_id = {}
            """.format(user_id))
        if res.fetchone()[0] != None:
            return res.fetchone()[0]

    def get_user_name(self, user_id):
        res = self.cursor.execute("""
            SELECT username, first_name, last_name FROM pik_users WHERE user_id = {}
        """.format(user_id))
        res = res.fetchone()
        if res:
            if res[0]:
                return res[0]
            else:
                return res[2] + ' ' + res[1]

    def get_user_id(self, username):
        res = self.cursor.execute("""
            SELECT user_id FROM pik_users WHERE username = '{}'
        """.format(username))
        res = res.fetchone()
        if res:
            return res[0]

    def make_plasure(self, user_to, user_from):
        # print(user_to, user_from)
        self.cursor.execute("""
            INSERT INTO likes (user_id, helper_id, date) VALUES ({}, {} , datetime())
        """.format(user_from, user_to))
        res = self.cursor.execute("""
                UPDATE pik_users SET likes=(
                    SELECT 
                        CASE likes 
                            WHEN likes
                                THEN likes + 1
                            ELSE 1
                        END likes
                    FROM pik_users
                    WHERE user_id={0})
                WHERE user_id={0}
            """.format(user_to))
        self.conn.commit()

    def get_user_data(self, user_id):
        req = "SELECT username, last_name, first_name, email, bkp, section, position from pik_users WHERE user_id={}".format(upd.sender_id)
        res = self.cursor.execute(req)
        if res:
            res = res.fetchone()
            data = {
                'username': res[0],
                'last_name': res[1],
                'first_name': res[2],
                'email': res[3],
                'bkp': res[4],
                'section': res[5],
                'position': res[6]
            }
        return data


#######################
    def get_chat(self, upd):
        if not upd.is_common_chat:
            req = "INSERT INTO chats (chat_id, user_id) SELECT {0}, {1} WHERE NOT EXISTS(SELECT 1 FROM chats WHERE user_id={1} AND chat_id={})".format(upd.chat_id, upd.user_id)
            self.cursor.execute(req)
            self.conn.commit()
            return True
        else:
            return False

    def get_chat_status(self, upd):
        req = "SELECT status from chats WHERE chat_id={}".format(upd.chat_id)
        res = self.cursor.execute(req)
        if res.fetchone():
            return res.fetchone()

    def set_chat_status(self, upd, status):
        req = "UPDATE chats SET status = '{1}' chat_id={0}".format(upd.chat_id, status)
        res = self.cursor.execute(req)
        self.conn.commit()
        return status