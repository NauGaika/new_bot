from telegramm import TelegramRequests

class Control_session_instructions:
    instruction_requests = {}
#     def __init__(self):
#         self.instruction_request = None
#         self.link_instruction_request = None
#         super(Control_session_instructions, self).__init__()

    def request_instruction(self, upd, text):
        print('Запрос на получение инструкции в диспетчерскую')
        self.messages.append(upd)
        text = upd.text
        if text:
            res = TelegramRequests.resend_message(self.chat_id, upd.chat_id, upd.message_id)
            self.__class__.instruction_requests.update({res.message_id: (upd.message_id, upd.chat_id, text)})

