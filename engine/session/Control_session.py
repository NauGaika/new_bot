from telegramm import TelegramRequests




class Control_session():
    chat_id = -339404157
    sessions = {}
    messages = {}


    @classmethod
    def create(cls, upd, bot=None):
        if upd.chat_id not in cls.sessions.keys():
            cls.sessions.setdefault(upd.chat_id, cls(upd, bot=bot))
        cur_session = cls.sessions[upd.chat_id]
        cur_session.messages_all.append(upd)
        return cur_session

    @classmethod
    def resend_message(cls, upd):
        if upd.chat_id:
            if upd.chat_id != cls.chat_id:
                res_mes = TelegramRequests.resend_message(cls.chat_id, upd.chat_id, upd.message_id)
                cls.messages.setdefault(res_mes.message_id, upd.chat_id)
                # text = upd.text
                # res = cls.templ.findall(text)
                # res = list(set([i.lower() for i in res]))
                # res = [cls.morph.parse(i)[0] for i in res if i not in stop_words]
                # res = [i.normal_form for i in res]
                # text = ', '.join(res)
                # text = "Предполагаемые теги: " + text
                # TelegramRequests.send_message(cls.chat_id, text)
            else:
                if upd.resend_message_id in cls.messages.keys():
                    TelegramRequests.send_message(cls.messages[upd.resend_message_id], upd.text)
