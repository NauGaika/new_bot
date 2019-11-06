from telegramm import TelegramRequests
from .User_session_info import User_session_info
from .User_session_instructions import User_session_instructions
from .User_session_crocotime import User_session_crocotime
from .User_session_inline import User_session_inline



class User_session(User_session_info, User_session_instructions, User_session_crocotime, User_session_inline):
    user_sessions = {}
    _all_tags = None
    db = None

    @classmethod
    def create(cls, upd, bot=None):
        if upd.chat_id not in cls.user_sessions.keys():
            cls.user_sessions.setdefault(upd.chat_id, cls(upd, bot=bot))
        cur_session = cls.user_sessions[upd.chat_id]
        cur_session.messages_all.append(upd)
        # upd.print_obj()
        if not cur_session.all_user_data_is_check:
            cur_session.all_user_data_is_check = cur_session.check_all_user_data()
        if cur_session.all_user_data_is_check:
            # print(upd.inline_data)
            cur_session.command_reduser()
        return cur_session

    def __init__(self, upd, bot=None):
        self.bot = bot
        self.instruction_question = ""
        self.chine = []
        self.user_data = self.db.User.get_user(upd)
        self.current_inline_keypud = None
        self.messages_all = []
        self.messages_current = []
        self.__status = {'gen': '', 'sub': ''}
        self._is_admin = False
        self.user_id = upd.sender_id
        self.param_to_confim_name = None
        self.param_to_confim_value = None
        self.param_to_confim_value_dict = {}
        self.all_user_data_is_check = False
        self.current_command = ""
        self.hashtags = []
        self.instruction_question = ""
        self.cur_message = ""
        super(User_session, self).__init__()

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__status['gen'] = value[0]
        self.__status['sub'] = value[1]
        print(self.__status)

    @property
    def is_admin(self):
        if self.user_data.is_admin:
            self._is_admin = True
            return self._is_admin

    def clear_current_status(self, param):
        self.status = ['', '']
        self.param_to_confim_value = None
        self.param_to_confim_name = None
        self.current_command = ''
        if param in self.param_to_confim_value_dict.keys():
            del self.param_to_confim_value_dict[param]

    def command_reduser(self):
        last_message = self.messages_all[-1]
        text = last_message.text
        # last_message.print_obj()
        if last_message.inline_query:
            self.inline_reducer()
        if last_message.command_names or self.current_command:
            if ('add_instruction' in last_message.command_names) or (self.current_command == 'add_instruction'):
                if self.is_admin:
                    self.current_command = 'add_instruction'
                    self.add_instruction(text)
                    print("Пользователь {} добавляет инструкцию".format(self.user_data.fio))
            elif ('info' in last_message.command_names):
                self.show_user_info()
                print("Пользователь {} узнает информацию о себе".format(self.user_data.fio))
            elif ('croco_day' in last_message.command_names):
                self.croco_get_last_day()
                print("Пользователь {} узнает крокотайм за день".format(self.user_data.fio))
            elif ('croco_week' in last_message.command_names):
                self.get_prev_week()
                print("Пользователь {} узнает крокотайм за неделю".format(self.user_data.fio))
            elif ('croco_weekend' in last_message.command_names):
                self.croco_get_last_weekend()
                print("Пользователь {} узнает крокотайм за предыдущие выходные".format(self.user_data.fio))

            elif ('find_instruction' in last_message.command_names) or (self.current_command == 'find_instruction'):
                self.current_command = 'find_instruction'
                print("Пользователь {} ищет инструкцию".format(self.user_data.fio))
                if 'find_instruction' in last_message.command_names:
                    self.chine = []
                    self.status = ['', '']
                    if self.current_inline_keypud:
                        TelegramRequests.delete_message(self.user_id, self.current_inline_keypud.message_id)
                self.find_instruction()
