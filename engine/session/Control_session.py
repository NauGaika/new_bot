from telegramm import TelegramRequests
from .Control_session_instructions import Control_session_instructions
import pandas as pd
import re
import pymorphy2
from rutermextract import TermExtractor

class Control_session(Control_session_instructions):
# class Control_session:
    chat_id = None
    stop_words = ["узнать","необходимый","какой","c","а","алло","без","белый","близко","более","больше","большой","будем","будет","будете","будешь","будто","буду","будут","будь","бы","бывает","бывь","был","была","были","было","быть","в","важная","важное","важные","важный","вам","вами","вас","ваш","ваша","ваше","ваши","вверх","вдали","вдруг","ведь","везде","вернуться","весь","вечер","взгляд","взять","вид","видел","видеть","вместе","вне","вниз","внизу","во","вода","война","вокруг","вон","вообще","вопрос","восемнадцатый","восемнадцать","восемь","восьмой","вот","впрочем","времени","время","все","все еще","всегда","всего","всем","всеми","всему","всех","всею","всю","всюду","вся","всё","второй","вы","выйти","г","где","главный","глаз","говорил","говорит","говорить","год","года","году","голова","голос","город","да","давать","давно","даже","далекий","далеко","дальше","даром","дать","два","двадцатый","двадцать","две","двенадцатый","двенадцать","дверь","двух","девятнадцатый","девятнадцать","девятый","девять","действительно","дел","делал","делать","делаю","дело","день","деньги","десятый","десять","для","до","довольно","долго","должен","должно","должный","дом","дорога","друг","другая","другие","других","друго","другое","другой","думать","душа","е","его","ее","ей","ему","если","есть","еще","ещё","ею","её","ж","ждать","же","жена","женщина","жизнь","жить","за","занят","занята","занято","заняты","затем","зато","зачем","здесь","земля","знать","значит","значить","и","иди","идти","из","или","им","имеет","имел","именно","иметь","ими","имя","иногда","их","к","каждая","каждое","каждые","каждый","кажется","казаться","как","какая","какой","кем","книга","когда","кого","ком","комната","кому","конец","конечно","которая","которого","которой","которые","который","которых","кроме","кругом","кто","куда","лежать","лет","ли","лицо","лишь","лучше","любить","люди","м","маленький","мало","мать","машина","между","меля","менее","меньше","меня","место","миллионов","мимо","минута","мир","мира","мне","много","многочисленная","многочисленное","многочисленные","многочисленный","мной","мною","мог","могу","могут","мож","может","может быть","можно","можхо","мои","мой","мор","москва","мочь","моя","моё","мы","на","наверху","над","надо","назад","наиболее","найти","наконец","нам","нами","народ","нас","начала","начать","наш","наша","наше","наши","не","него","недавно","недалеко","нее","ней","некоторый","нельзя","нем","немного","нему","непрерывно","нередко","несколько","нет","нею","неё","ни","нибудь","ниже","низко","никакой","никогда","никто","никуда","ним","ними","них","ничего","ничто","но","новый","нога","ночь","ну","нужно","нужный","нх","о","об","оба","обычно","один","одиннадцатый","одиннадцать","однажды","однако","одного","одной","оказаться","окно","около","он","она","они","оно","опять","особенно","остаться","от","ответить","отец","откуда","отовсюду","отсюда","очень","первый","перед","писать","плечо","по","под","подойди","подумать","пожалуйста","позже","пойти","пока","пол","получить","помнить","понимать","понять","пор","пора","после","последний","посмотреть","посреди","потом","потому","почему","почти","правда","прекрасно","при","про","просто","против","процентов","путь","пятнадцатый","пятнадцать","пятый","пять","работа","работать","раз","разве","рано","раньше","ребенок","решить","россия","рука","русский","ряд","рядом","с","с кем","сам","сама","сами","самим","самими","самих","само","самого","самой","самом","самому","саму","самый","свет","свое","своего","своей","свои","своих","свой","свою","сделать","сеаой","себе","себя","сегодня","седьмой","сейчас","семнадцатый","семнадцать","семь","сидеть","сила","сих","сказал","сказала","сказать","сколько","слишком","слово","случай","смотреть","сначала","снова","со","собой","собою","советский","совсем","спасибо","спросить","сразу","стал","старый","стать","стол","сторона","стоять","страна","суть","считать","т","та","так","такая","также","таки","такие","такое","такой","там","твои","твой","твоя","твоё","те","тебе","тебя","тем","теми","теперь","тех","то","тобой","тобою","товарищ","тогда","того","тоже","только","том","тому","тот","тою","третий","три","тринадцатый","тринадцать","ту","туда","тут","ты","тысяч","у","увидеть","уж","уже","улица","уметь","утро","хороший","хорошо","хотел бы","хотеть","хоть","хотя","хочешь","час","часто","часть","чаще","чего","человек","чем","чему","через","четвертый","четыре","четырнадцатый","четырнадцать","что","чтоб","чтобы","чуть","шестнадцатый","шестнадцать","какой","шестой","шесть","эта","эти","этим","этими","этих","это","этого","этой","этом","этому","этот","эту","я","являюсь"]
    term_extractor = TermExtractor()
    morph = pymorphy2.MorphAnalyzer()

    def __init__(self, chat_id, bot=None):
        self.chat_id = chat_id
        self.messages = []
        self.bot = bot
        self._status = {}
        self.instruction_to_send = {}
        super(Control_session, self).__init__()

    @property
    def status(self):
        res = self._status.setdefault(self.messages[-1].sender_id,
            {
                'gen': '',
                'sub': ''
            }
        )
        return res

    @status.setter
    def status(self, value):
        self.status
        self._status[self.messages[-1].sender_id]['gen'] = value[0]
        self._status[self.messages[-1].sender_id]['sub'] = value[1]
        print(self._status[self.messages[-1].sender_id])

    def work(self, upd):
        if upd not in self.messages:
            self.messages.append(upd)
        # upd.print_obj()
        # если сообщение является ответом на сообщение с запросом на инструкцию
        if self.status['gen'] == 'request_instruction':
            instruction = self.db.Instruction.get_by_link(self.instruction_to_send[upd.sender_id]['link'])
            if instruction:
                instruction, session = instruction
                self.db.Tag.add_new_keywords_to_instruction(instruction, self.get_instruction_words_wage(self.instruction_to_send[upd.sender_id]['text']), session=session)
                TelegramRequests.send_message(self.instruction_to_send[upd.sender_id]['chat_id'], self.instruction_to_send[upd.sender_id]['link'])
            else:
                TelegramRequests.send_message(self.chat_id, 'Инструкции {} не существует. Создайте ее'.format(self.instruction_to_send[upd.sender_id]['link']))
            self.status = ['', '']
        elif upd.resend_message_id in self.instruction_requests.keys():
            text = upd.text
            self.status = ['request_instruction', '']
            text = text.replace('#link', '')
            text = text.strip()
            self.instruction_to_send.setdefault(upd.sender_id,
                {
                    'link': text,
                    'title': '',
                    'chat_id': self.instruction_requests[upd.resend_message_id][1],
                    'text': self.instruction_requests[upd.resend_message_id][2]
                })
            self.work(upd)


    @classmethod
    def resend_message(cls, upd):
        if upd.chat_id:
            if upd.chat_id != cls.chat_id:
                res_mes = TelegramRequests.resend_message(cls.chat_id, upd.chat_id, upd.message_id)
                cls.messages.setdefault(res_mes.message_id, upd.chat_id)
            else:
                if upd.resend_message_id in cls.messages.keys():
                    TelegramRequests.send_message(cls.messages[upd.resend_message_id], upd.text)

    def get_instruction_words_wage(self, text):
        res = {}
        words_count = 0
        templ = re.compile('[0-9.]+')

        for term in self.term_extractor(text, nested=True):
            res.setdefault(term.normalized, term.count)
            words_count += term.count
        for i in res.keys():
            res[i] = (res[i] / words_count)
        text_split = templ.findall(text)
        for i in text_split:
            res.setdefault(i, text_split.count(i) / words_count)
        for i in list(res.keys()):
            res2 = self.morph.parse(i)
            res.setdefault(res2[0].normal_form, res[i])
        return res
