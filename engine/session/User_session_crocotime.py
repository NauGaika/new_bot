from telegramm import TelegramRequests


class User_session_crocotime:

    def croco_get_last_day(self):
        """Получаем информацию крокотайма за предыдущий день."""
        res = self.pik_db.CrocoTime.get_prev_day(self.user_data.pik_id)
        if res:
            message = """
    За вчерашний день вы отработали {} часов
    Из них {} - продуктивные
    """.format(round(res['SummaryHours']*100)/100, round(res['PermittedHours']*100)/100)
            TelegramRequests.send_message(self.user_id, message)
        else:
            TelegramRequests.send_message(self.user_id, "Выгрузки крокотйам еще не было")

    def get_prev_week(self):
        """Получаем информацию крокотайма за предыдущую неделю."""
        res = self.pik_db.CrocoTime.get_prev_week(self.user_data.pik_id)
        if res:
            message = """
    За неделю вы отработали {} часов
    Из них {} - продуктивные
    """.format(round(res['SummaryHours']*100)/100, round(res['PermittedHours']*100)/100)
            TelegramRequests.send_message(self.user_id, message)
        else:
            print(res)

    def croco_get_last_weekend(self):
        """Получаем информацию крокотайма за предыдущие выходные"""
        res = self.pik_db.CrocoTime.get_prev_weakend(self.user_data.pik_id)
        if res:
            message = """
    За выходные вы отработали {} часов
    Из них {} - продуктивные
    """.format(round(res['SummaryHours']*100)/100, round(res['PermittedHours']*100)/100)
            TelegramRequests.send_message(self.user_id, message)
        else:
            print(res)