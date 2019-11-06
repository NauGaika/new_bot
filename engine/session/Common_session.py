from telegramm import TelegramRequests
from commands.plasure import Bot_plasure


class Common_session:
    common_sessions = {}
    db = None

    @classmethod
    def create(cls, upd, bot=None):
        if not Bot_plasure.db:
            Bot_plasure.db = cls.db
        if upd.chat_id not in cls.common_sessions.keys():
            cls.common_sessions.setdefault(upd.chat_id, cls(upd, bot=bot))
        cur_session = cls.common_sessions[upd.chat_id]
        cur_session.messages_all.append(upd)
        cur_session.get_or_create_user()
        return cur_session

    def __init__(self, upd, bot=None):
        self.bot=bot
        self.db.User.get_user(upd)
        self.messages_all = []
        self.messages_current = []

    def get_or_create_user(self):
        cur_message = self.messages_all[-1]
        cur_user = self.db.User.get_user(cur_message)
        Bot_plasure.is_plasure(cur_message, cur_user)
