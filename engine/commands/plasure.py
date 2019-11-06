import re
from telegramm.TelegramRequests import TelegramRequests


class Bot_plasure:
    plasure_templates = ['спасибо', 'благодарю', 'спс', 'от души']
    db = None

    @classmethod
    def is_plasure(cls, upd, user):
        templ = cls.make_template(cls.plasure_templates)
        # print(upd.obj)
        # templ_2 = cls.make_template(cls.plasure_templates, start_str="^@[\w\d_]+\s+")
        if upd.text:
            if templ.search(upd.text):
                if upd.resend_id:
                    gratefull = cls.db.User.get_user_by_id(upd.resend_id, upd.resend_username)
                    if gratefull.telegramm_id != user.telegramm_id:
                        cls.db.Plasure.make_plasure(user.telegramm_id, gratefull.telegramm_id)
                        TelegramRequests.send_message(upd.chat_id, 'Поблагодарили пользователя {} у него теперь {} благодарностей'.format(gratefull.username, gratefull.plasures+1))
                        cls.db.User.add_plasures(gratefull.telegramm_id)
                        print("Поблагодарили пользователя {}".format(gratefull))
                elif upd.message_usernames:
                    print(upd.message_usernames)
                    gratefull = cls.db.User.get_user_by_username(upd.message_usernames[0])
                    if gratefull:
                        cls.db.Plasure.make_plasure(user.telegramm_id, gratefull.telegramm_id)
                        print("{} поблагодарил пользователя {}".format(user, gratefull))
                        TelegramRequests.send_message(upd.chat_id, 'Поблагодарили пользователя {} у него теперь {} благодарностей'.format(gratefull.username, gratefull.plasures+1))
                        cls.db.User.add_plasures(gratefull.telegramm_id)
                elif templ.search(upd.text):
                    TelegramRequests.send_message(upd.chat_id, 'Если вы хотите поблагодарить кого-нибудь - Ответьте на сообщение со словами спасибо')
                # TelegramRequests.send_message(upd.chat_id, 'Вы поблагодарили @{} пикули  ☄️ пользователя равны {}'.format(upd.resend.username, cls.db.User.get_user_likes(user_to_plasure_id)))
        # elif templ.search(upd.text):
        #     TelegramRequests.send_message(upd.chat_id, 'Если вы хотите поблагодарить кого-нибудь - Ответьте на сообщение-ответ')

    @classmethod
    def make_template(cls, arr, start_str=""):
        """Делает из массива регулярное выражение на содержит."""
        templ = start_str
        pos = 1
        for i in arr:
            templ += "({})".format(i)
            if pos != len(arr):
                templ += '|'
            pos += 1
        return re.compile(templ, re.IGNORECASE)
