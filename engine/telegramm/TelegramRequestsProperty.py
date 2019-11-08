class TelegramRequestsProperty:

    @property
    def message_id(self):
        """Id сообщения."""
        if 'message_id' in self.obj.keys():
            return self.obj['message_id']
        elif 'message' in self.obj.keys():
            return self.obj['message']['message_id']
        elif 'callback_query' in self.obj.keys():
            if 'message' in self.obj['callback_query'].keys():
                if 'message_id' in self.obj['callback_query']['message'].keys():
                    return self.obj['callback_query']['message']['message_id']


    @property
    def sender_id(self):
        """Отправитель сообщения."""
        if 'callback_query' in self.obj.keys():
            if 'message' in self.obj['callback_query'].keys():
                if 'chat' in self.obj['callback_query']['message'].keys():
                    if 'id' in self.obj['callback_query']['message']['chat'].keys():
                        return self.obj['callback_query']['message']['chat']['id']
        elif 'message' in self.obj.keys():
            return self.obj['message']['from']['id']
        elif 'edited_message' in self.obj.keys():
            return self.obj['edited_message']['from']['id']
        elif 'inline_query' in self.obj:
            if 'from' in self.obj['inline_query']:
                return self.obj['inline_query']['from']['id']

    @property
    def chat_id(self):
        """ID чата отправителя."""
        if 'callback_query' in self.obj.keys():
            if 'message' in self.obj['callback_query'].keys():
                if 'chat' in self.obj['callback_query']['message'].keys():
                    if 'id' in self.obj['callback_query']['message']['chat'].keys():
                        return self.obj['callback_query']['message']['chat']['id']
        if 'message' in self.obj.keys():
            return self.obj['message']['chat']['id']
        elif 'edited_message' in self.obj.keys():
            return self.obj['edited_message']['chat']['id']

    @property
    def username(self):
        """username сообщения."""
        if 'message' in self.obj.keys():
            if "username" in self.obj['message']['from'].keys():
                return self.obj['message']['from']['username']
            else:
                return self.first_name + ' ' + self.last_name
        elif 'inline_query' in self.obj:
            if 'from' in self.obj['inline_query']:
                if 'username' in self.obj['inline_query']['from']:
                    return self.obj['inline_query']['from']['username']
                else:
                    return self.first_name + ' ' + self.last_name

    @property
    def first_name(self):
        """first_name сообщения."""
        if 'message' in self.obj.keys():
            if "first_name" in self.obj['message']['from'].keys():
                return self.obj['message']['from']['first_name']
        elif 'inline_query' in self.obj:
            if 'from' in self.obj['inline_query'].keys():
                if 'username' in self.obj['inline_query']['from'].keys():
                    return self.obj['inline_query']['from']['first_name']
        return ''

    @property
    def last_name(self):
        """last_name сообщения."""
        if 'message' in self.obj.keys():
            if "last_name" in self.obj['message']['from'].keys():
                return self.obj['message']['from']['last_name']
        elif 'inline_query' in self.obj.keys():
            if 'from' in self.obj['inline_query'].keys():
                if 'username' in self.obj['inline_query']['from'].keys():
                    return self.obj['inline_query']['from']['last_name']
        return ''

    @property
    def text(self):
        if 'message' in self.obj.keys():
            if 'text' in self.obj['message'].keys():
                return self.obj['message']['text']
        elif 'edited_message' in self.obj.keys():
            return self.obj['edited_message']['text']
        elif 'text' in self.obj.keys():
            return self.obj['text']


    @property
    def update_id(self):
        return self.obj['update_id'] + 1

    @property
    def resend_chat_id(self):
        """Id чата отправителя."""
        if 'reply_to_message' in self.obj['message'].keys():
            return self.obj['message']['reply_to_message']['chat']['id']

    @property
    def resend_username(self, cur_chat=False):
        """От кого отправлено сообщение."""
        if 'reply_to_message' in self.obj['message'].keys():
            tt = self.obj['message']['reply_to_message']['from']
            if 'username' in tt.keys():
                return tt['username']
            else:
                return tt['first_name'] + ' ' + tt['last_name']

    @property
    def resend_id(self, cur_chat=False):
        """От кого отправлено сообщение."""
        if 'reply_to_message' in self.obj['message'].keys():
            if 'id' in self.obj['message']['reply_to_message']['from'].keys():
                return self.obj['message']['reply_to_message']['from']['id']

    @property
    def resend_message_id(self):
        """id пользователя перенаправленного сообщения."""
        if 'message' in self.obj.keys():
            if 'reply_to_message' in self.obj['message'].keys():
                return self.obj['message']['reply_to_message']['message_id']

    @property
    def is_message(self):
        """Является ли сообщением."""
        if 'message' in self.obj.keys():
            return 'text' in self.obj['message'].keys()

    @property
    def is_common_chat(self):
        """Является ли чат общим или индивидуальным."""
        if 'message' in self.obj.keys():
            if 'chat' in self.obj['message'].keys():
                if 'type' in self.obj['message']['chat'].keys():
                    if self.obj['message']['chat']['type'] == 'group' or self.obj['message']['chat']['type'] == 'supergroup':
                        return True

    @property
    def command_names(self):
        """Наименование команд."""
        commands = []
        if 'message' in self.obj.keys():
            if 'entities' in self.obj['message'].keys():
                if 'type' in self.obj['message']['entities'][0].keys():
                    for i in self.obj['message']['entities']:
                        if 'type' in i.keys():
                            if i['type'] == 'bot_command':
                                commands.append(self.text[i['offset']+1:i['offset'] + i['length']].split('@')[0])
        return commands

    @property
    def hashtags(self):
        """Наименование команд."""
        hashtags = []
        if 'entities' in self.obj['message'].keys():
            if 'type' in self.obj['message']['entities'][0].keys():
                for i in self.obj['message']['entities']:
                    if 'type' in i.keys():
                        if i['type'] == 'hashtag':
                            hashtags.append(self.text[i['offset']: i['offset'] + i['length']])
        return hashtags

    @property
    def message_usernames(self):
        """Пользователи указанные в сообщении"""
        names =[]
        if 'entities' in self.obj['message'].keys():
            if 'type' in self.obj['message']['entities'][0].keys():
                for i in self.obj['message']['entities']:
                    if 'type' in i.keys():
                        if i['type'] == 'mention':
                            names.append(self.text[i['offset']+1 : i['offset'] + i['length']])
        return names