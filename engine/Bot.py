import requests
import re
import os

from threading import Thread
from telegramm import TelegramRequests
from session import User_session, Common_session, Control_session
from Bot_methods import Bot_methods
from instructions import Hashtag_cloud
import sys
sys.path.append(os.getcwd())

import db
import pik_db

User_session.db = db
User_session.pik_db = pik_db
User_session.Control_session = Control_session
Common_session.db = db
Common_session.pik_db = pik_db
Hashtag_cloud.db = db

class Bot(Bot_methods):
    """
    Бот для работы с телегой.

    """
    db = db

    def __init__(self, token):
        self.last_update = None
        self.token = token
        TelegramRequests.token = token
        self.hashtag_cloud = Hashtag_cloud(self.db)
        self.control_session = Control_session
        self.sessions = []

    def work(self):
        """Работа бота."""
        last_updates = self.get_last_update()
        if last_updates:

            for last_update in last_updates:
                self.work_thread(last_update)

    def work_thread(self, update):
        # print(self.hashtag_cloud.link_data)
        # update.inline_hashtags
        # print(update.obj)
        # print(TelegramRequests.send_inline_result(update.query_id, 'test'))
        # if update.chat_id and update.chat_id == Control_session.chat_id:
        #     session = Control_session.create(update, bot=self)
        if update.text:
            self.control_session.resend_message(update)
        if not update.is_common_chat:
            session = User_session.create(update, bot=self)
        else:
            session = Common_session.create(update, bot=self)
        if session not in self.sessions:
            self.sessions.append(session)

    def get_updates(self, offset=None, timeout=30):
        """Получает обновления."""
        params = {'timeout': timeout, 'offset': offset}
        api_url = "https://api.telegram.org/bot{}/getUpdates".\
            format(self.token)
        resp = requests.get(api_url, params)
        result_json = resp.json()['result']
        return result_json

    def get_last_update(self):
        """Получает последнее обновление."""
        if not self.last_update:
            get_result = self.get_updates()
        else:
            get_result = self.get_updates(offset=self.last_update.update_id)
        if len(get_result):
            results = [TelegramRequests(i) for i in get_result]
            self.last_update = results[-1]
            return results
