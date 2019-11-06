import time
import json
import requests
import re


class TelegramRequestsInline:

    @property
    def inline_query(self):
        if 'inline_query' in self.obj:
            return self.obj['inline_query']

    @property
    def callback_query(self):
        if 'callback_query' in self.obj.keys():
            return self.obj['callback_query']

    @property
    def inline_data(self):
        if self.callback_query:
            if 'data' in self.callback_query.keys():
                return self.callback_query['data']

    @property
    def query(self):
        if self.inline_query:
            if 'query' in self.inline_query:
                return self.inline_query['query']

    @property
    def query_id(self):
        if self.inline_query:
            if 'id' in self.inline_query:
                return self.inline_query['id']


    @property
    def inline_hashtags(self):
        if self.query:
            template = re.compile('#[\wа-яА-Я\dёЁ]+')
            hashtags = template.findall(self.query)
            return hashtags

    @classmethod
    def send_inline_result(cls, query_id, text, hashtags = ['Василий', 'Петрович', 'Автомобиль', 'BDS', 'Ошибка']):
        results = [{
            'type': 'article',
            'id': '22',
            'title': 'Проверяем артикль',
            'input_message_content': {
                'message_text': text + 'test',
            },
            'reply_markup': {
                'inline_keyboard': []
            }
        }]
        for i in hashtags:
            results[0]['reply_markup']['inline_keyboard'].append([{'text': i, 'callback_data': "hashtag" + i}])
        results = json.dumps(results)
        params = {'inline_query_id': query_id, 'results': results}
        api_url = "https://api.telegram.org/bot{}/".format(cls.token)
        method = 'answerInlineQuery'
        resp = requests.post(api_url + method, params)
        return resp.json()

    @classmethod
    def send_inline_keypud(cls, chat_id, text, buttons, confim_text=""):
        token = cls.token
        buttons = [[{'text': "{} ({})".format(button, len(button_count)), 'callback_data': button}] for button, button_count in buttons.items()]
        if confim_text:
            buttons[0].append({'text': confim_text, 'callback_data': confim_text})
        buttons_obj = {'inline_keyboard': buttons}
        buttons_obj = json.dumps(buttons_obj)
        params = {'chat_id': chat_id, 'text': text, 'reply_markup': buttons_obj}
        api_url = "https://api.telegram.org/bot{}/".format(token)
        method = 'sendMessage'
        resp = requests.post(api_url + method, params)
        resp = resp.json()['result']
        return resp

    @classmethod
    def edit_inline_keypud(cls, chat_id, message_id, text, confim_text="", parsemod_html=True, reject_text="", buttons={}):
        token = cls.token
        params = {'chat_id': chat_id, 'text': text, 'message_id': message_id}
        if buttons:
            buttons = [[{'text': "{} ({})".format(button, len(button_count)), 'callback_data': button}] for button, button_count in buttons.items()]
        else:
            buttons = []
        if confim_text:
            buttons.append([{'text': confim_text, 'callback_data': confim_text}])
        if reject_text:
            buttons.append([{'text': reject_text, 'callback_data': reject_text}])
        if buttons:
            buttons_obj = {'inline_keyboard': buttons}
            buttons_obj = json.dumps(buttons_obj)
            params.update({'reply_markup': buttons_obj})
        if parsemod_html:
            params.update({'parse_mode': 'HTML'})
        api_url = "https://api.telegram.org/bot{}/".format(token)
        method = 'editMessageText'
        resp = requests.post(api_url + method, params)
