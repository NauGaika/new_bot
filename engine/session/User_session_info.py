from telegramm import TelegramRequests


class User_session_info:

    def set_user_param(self, parameter, value):
        self.db.User.set_param(self.user_id, parameter, value)

    def check_all_user_data(self):
        self.user_data = self.db.User.get_user_by_telegramm(self.user_id)
        if not self.user_data.email:
            self.param_to_confim_name = 'email'
            messages = [
                "Я не знаю ваш email. Напишите его пожалуйста в ответном сообщении.\n Например 'bimbro@pik.ru'",
                "Вы указали email '{}' подтвердите или напишите заново",
                "Вы установили email '{}'",
            ]
            self.get_user_parameter(self.param_to_confim_name, messages)
        elif not self.user_data.pik_id:
            pik_user = self.pik_db.Users.get_user_by_username(self.user_data.email)
            if pik_user:
                dep_id = self.db.Department.create_departments_if_not_exist(pik_user.department)
                position_id = self.db.Position.create_position_if_not_exist(pik_user.Positions)
                self.db.User.set_fio(self.user_data.telegramm_id, pik_user.Fio)
                self.db.User.set_department_id(self.user_data.telegramm_id, dep_id)
                self.db.User.set_position_id(self.user_data.telegramm_id, position_id)
                self.db.User.set_pik_id(self.user_data.telegramm_id, pik_user.Id)
                self.user_data = self.db.User.get_user_by_telegramm(self.user_id)
                print('Записали данные пользователя {}'.format(self.user_data.fio))

            else:
                self.db.User.clear_email(self.user_data.telegramm_id)
                TelegramRequests.send_message(self.user_id, 'Такого пользователя в ГК "ПИК" не существует')
                self.check_all_user_data()
        else:
            self.status = ('', '')
            return True

    def get_user_parameter(self, parameter, messages):
        if self.param_to_confim_name:
            text = self.messages_all[-1].text
            if self.status['gen'] == "parameter" and self.status['sub'] == "get":
                TelegramRequests.send_message(self.user_id, messages[0])
                self.status = ['parameter', 'input']
            elif self.status['gen'] == "parameter" and self.status['sub'] == "input":
                self.param_to_confim_value = text
                TelegramRequests.send_keyboard(self.user_id, messages[1].format(self.param_to_confim_value), ['Подтверждаю'])
                self.status = ['parameter', 'confim']
            elif self.status['gen'] == "parameter" and self.status['sub'] == "confim":
                if text == 'Подтверждаю':
                    self.set_user_param(parameter, self.param_to_confim_value)
                    TelegramRequests.send_message(self.user_id, messages[2].format(self.param_to_confim_value))
                    self.status = ["",""]
                    self.check_all_user_data()
                if text == 'Подтверждаю':
                    self.status = ["", ""]
                    self.param_to_confim_value = ""
                    self.param_to_confim_name = ""
                else:
                    self.param_to_confim_value = text
                    TelegramRequests.send_keyboard(self.user_id, messages[1].format(self.param_to_confim_value), ['Подтверждаю'])
            else:
                self.status = ['parameter', 'get']
                self.get_user_parameter(parameter, messages)

    def show_user_info(self):
        user = self.db.User.get_user_by_id(self.user_id)
        all_links_count = self.db.User.get_all_instructions_count(self.user_id)
        TelegramRequests.send_message(self.user_id, """
Ваши данные
id: {}
Юзернейм: {}
Фамилия: {}
Имя: {}
Отчество: {}
Лайки: {}
email: {}
Подразделение: {}
Должность: {}
Количество инструкций: {}
            """.format(
            user.telegramm_id,
            user.username,
            user.fullname,
            user.name,
            user.patronymic,
            user.plasures,
            user.email,
            user.department.name,
            user.position.name,
            all_links_count
        ))
