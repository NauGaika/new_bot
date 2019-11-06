from telegramm import TelegramRequests

class User_session_inline:

    def __init__(self):
        super(User_session_inline, self).__init__()
        self.inline_prev_value = ''

    def inline_reducer(self):
        """Обрабатывает комманды из коммандной строки"""
        last_message = self.messages_all[-1]
        if last_message.query and len(last_message.query) > 3:
            self.inline_prev_value = last_message.query.lower()
            TelegramRequests.preview_tags(self.user_id, self.exist_tag(self.inline_prev_value))

    @property
    def all_tags(self):
        """Все тэги имеющиеся в базе."""
        if self._all_tags is None:
            self._all_tags = self.db.Tag.get_all_hashtag()
            self._all_tags = [i.tag for i in self._all_tags]
            print('Загрузили все тэги из базы')
        return self._all_tags

    def exist_tag(self, tag):
        res = []
        for i in self.all_tags:
            if tag in i:
                res.append(i)
        if not res:
            res = [self.inline_prev_value]
        if len(res) > 10:
            res = res[:10]
        return res
