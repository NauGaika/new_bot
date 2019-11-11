from telegramm import TelegramRequests
import pandas as pd
import re
import pymorphy2
from rutermextract import TermExtractor


class User_session_instructions:
    stop_words = ["узнать","необходимый","какой","c","а","алло","без","белый","близко","более","больше","большой","будем","будет","будете","будешь","будто","буду","будут","будь","бы","бывает","бывь","был","была","были","было","быть","в","важная","важное","важные","важный","вам","вами","вас","ваш","ваша","ваше","ваши","вверх","вдали","вдруг","ведь","везде","вернуться","весь","вечер","взгляд","взять","вид","видел","видеть","вместе","вне","вниз","внизу","во","вода","война","вокруг","вон","вообще","вопрос","восемнадцатый","восемнадцать","восемь","восьмой","вот","впрочем","времени","время","все","все еще","всегда","всего","всем","всеми","всему","всех","всею","всю","всюду","вся","всё","второй","вы","выйти","г","где","главный","глаз","говорил","говорит","говорить","год","года","году","голова","голос","город","да","давать","давно","даже","далекий","далеко","дальше","даром","дать","два","двадцатый","двадцать","две","двенадцатый","двенадцать","дверь","двух","девятнадцатый","девятнадцать","девятый","девять","действительно","дел","делал","делать","делаю","дело","день","деньги","десятый","десять","для","до","довольно","долго","должен","должно","должный","дом","дорога","друг","другая","другие","других","друго","другое","другой","думать","душа","е","его","ее","ей","ему","если","есть","еще","ещё","ею","её","ж","ждать","же","жена","женщина","жизнь","жить","за","занят","занята","занято","заняты","затем","зато","зачем","здесь","земля","знать","значит","значить","и","иди","идти","из","или","им","имеет","имел","именно","иметь","ими","имя","иногда","их","к","каждая","каждое","каждые","каждый","кажется","казаться","как","какая","какой","кем","книга","когда","кого","ком","комната","кому","конец","конечно","которая","которого","которой","которые","который","которых","кроме","кругом","кто","куда","лежать","лет","ли","лицо","лишь","лучше","любить","люди","м","маленький","мало","мать","машина","между","меля","менее","меньше","меня","место","миллионов","мимо","минута","мир","мира","мне","много","многочисленная","многочисленное","многочисленные","многочисленный","мной","мною","мог","могу","могут","мож","может","может быть","можно","можхо","мои","мой","мор","москва","мочь","моя","моё","мы","на","наверху","над","надо","назад","наиболее","найти","наконец","нам","нами","народ","нас","начала","начать","наш","наша","наше","наши","не","него","недавно","недалеко","нее","ней","некоторый","нельзя","нем","немного","нему","непрерывно","нередко","несколько","нет","нею","неё","ни","нибудь","ниже","низко","никакой","никогда","никто","никуда","ним","ними","них","ничего","ничто","но","новый","нога","ночь","ну","нужно","нужный","нх","о","об","оба","обычно","один","одиннадцатый","одиннадцать","однажды","однако","одного","одной","оказаться","окно","около","он","она","они","оно","опять","особенно","остаться","от","ответить","отец","откуда","отовсюду","отсюда","очень","первый","перед","писать","плечо","по","под","подойди","подумать","пожалуйста","позже","пойти","пока","пол","получить","помнить","понимать","понять","пор","пора","после","последний","посмотреть","посреди","потом","потому","почему","почти","правда","прекрасно","при","про","просто","против","процентов","путь","пятнадцатый","пятнадцать","пятый","пять","работа","работать","раз","разве","рано","раньше","ребенок","решить","россия","рука","русский","ряд","рядом","с","с кем","сам","сама","сами","самим","самими","самих","само","самого","самой","самом","самому","саму","самый","свет","свое","своего","своей","свои","своих","свой","свою","сделать","сеаой","себе","себя","сегодня","седьмой","сейчас","семнадцатый","семнадцать","семь","сидеть","сила","сих","сказал","сказала","сказать","сколько","слишком","слово","случай","смотреть","сначала","снова","со","собой","собою","советский","совсем","спасибо","спросить","сразу","стал","старый","стать","стол","сторона","стоять","страна","суть","считать","т","та","так","такая","также","таки","такие","такое","такой","там","твои","твой","твоя","твоё","те","тебе","тебя","тем","теми","теперь","тех","то","тобой","тобою","товарищ","тогда","того","тоже","только","том","тому","тот","тою","третий","три","тринадцатый","тринадцать","ту","туда","тут","ты","тысяч","у","увидеть","уж","уже","улица","уметь","утро","хороший","хорошо","хотел бы","хотеть","хоть","хотя","хочешь","час","часто","часть","чаще","чего","человек","чем","чему","через","четвертый","четыре","четырнадцатый","четырнадцать","что","чтоб","чтобы","чуть","шестнадцатый","шестнадцать","какой","шестой","шесть","эта","эти","этим","этими","этих","это","этого","этой","этом","этому","этот","эту","я","являюсь"]
    term_extractor = TermExtractor()
    morph = pymorphy2.MorphAnalyzer()
    _instruction_big_data = None

    def __init__(self):
        self.text_query = ''
        self.prev_instruction_message = None
        super(User_session_instructions, self).__init__()

    def create_instruction(self):
        user = self.user_id
        title = self.param_to_confim_value_dict['instruction']['title']
        link = self.param_to_confim_value_dict['instruction']['link']
        tags = self.param_to_confim_value_dict['instruction']['tags']
        words = self.param_to_confim_value_dict['instruction']['words']
        title_keywords = self.get_instruction_words_wage(self.param_to_confim_value_dict['instruction']['title'])
        instruction_id = self.db.Instruction.create_new(title, link, user)
        tags = self.db.Tag.create_tags_with_wage(tags, instruction_id=instruction_id, koef=3)
        tags = self.db.Tag.create_tags_with_wage(title_keywords, instruction_id=instruction_id, koef=3)
        tags = self.db.Tag.create_tags_with_wage(words, instruction_id=instruction_id)

    def add_instruction(self, text):
        self.param_to_confim_value_dict.setdefault('instruction', {})
        if self.status['gen'] == '':
            self.status['gen'] = 'instruction_link'
            self.status['sub'] = 'req'
            self.command_reduser()
        elif self.status['gen'] == 'instruction_link':
            if self.status['sub'] == 'req':
                TelegramRequests.send_message(self.user_id, 'Укажиты ссылку на инструкцию. Например http://pikipedia.pik.ru')
                self.status['sub'] = 'get'

            elif self.status['sub'] == 'get':
                res = self.db.Instruction.is_link_exist(text)
                if not res:
                    TelegramRequests.send_keyboard(self.user_id, 'Вы указали ссылку на инструкцию "{}" если все верно - подтвердите. Если хотиет внести изменения - укажите данные еще раз. Либо отмените добавление статьи'.format(text), ['Подтверждаю', 'Отменить'])
                    self.status['sub'] = 'confim'
                    self.param_to_confim_value_dict['instruction']['link'] = text
                else:
                    TelegramRequests.send_message(self.user_id, 'Инструкция по ссылке {} уже добавлена'.format(text))
                    self.status['sub'] = 'get'
            elif self.status['sub'] == 'confim':
                if text == "Подтверждаю":
                    self.status['gen'] = 'instruction_title'
                    self.status['sub'] = 'req'
                else:
                    self.status['sub'] = 'get'
                self.command_reduser()
        elif self.status['gen'] == 'instruction_title':
            if self.status['sub'] == 'req':
                TelegramRequests.send_message(self.user_id, 'Укажиты заголовок инструкции. Например Главная страница пикипедии')
                self.status['sub'] = 'get'

            elif self.status['sub'] == 'get':
                TelegramRequests.send_keyboard(self.user_id, 'Вы указали заголовок инструкции "{}" если все верно - подтвердите. Если хотиет внести изменения - укажите данные еще раз. Либо отмените добавление статьи'.format(text), ['Подтверждаю', 'Отменить'])
                self.param_to_confim_value_dict['instruction']['title'] = text
                self.status['sub'] = 'confim'

            elif self.status['sub'] == 'confim':
                if text == "Подтверждаю":
                    self.status['gen'] = 'instruction_tag'
                    self.status['sub'] = 'req'
                else:
                    self.status['sub'] = 'get'
                self.command_reduser()
        elif self.status['gen'] == 'instruction_tag':
            if self.status['sub'] == 'req':
                self.param_to_confim_value_dict['instruction']['tags'] = []
                text = 'Укажиты тэги инструкции через запятую. Напирмер "Спецификаци, ВРС, БДС, КЖ, АР"'
                TelegramRequests.send_message(self.user_id, text)
                self.status['sub'] = 'get'

            elif self.status['sub'] == 'get':
                all_tags = text.split(',')
                all_tags = [i.strip().lower() for i in all_tags if i.strip() != ""]
                all_tags += self.param_to_confim_value_dict['instruction']['tags']
                all_tags = list(set(all_tags))
                self.param_to_confim_value_dict['instruction']['tags'] = all_tags
                exist_tags, not_exist_tags = self.db.Tag.check_exist(self.param_to_confim_value_dict['instruction']['tags'])
                exist_text = ', '.join(exist_tags)
                not_exist_text = ', '.join(not_exist_tags)
                TelegramRequests.send_keyboard(self.user_id, """
        Вы указали существующие тэги: {} \n Будут добавлены новые тэги: {} \n если все верно - подтвердите. Если хотиет внести изменения - укажите данные еще раз. Либо отмените добавление статьи
        """.format(exist_text, not_exist_text), ['Подтверждаю', 'Отменить'])
                self.status['sub'] = 'confim'

            elif self.status['sub'] == 'confim':
                if text == "Подтверждаю":
                    TelegramRequests.send_keyboard(self.user_id, """
                    Вы можете указать текстовую часть статьи для уточнения поиска
                    """, ['Подтверждаю', 'Отменить'])
                    self.param_to_confim_value_dict['instruction'].setdefault('words', {})
                    self.status['gen'] = 'add_instruction_text'
                    self.status['sub'] = 'start'
                else:
                    self.status['sub'] = 'get'
                    self.command_reduser()
        elif self.status['gen'] == 'add_instruction_text':
            if text == "Подтверждаю":
                self.status['gen'] = 'add_instruction_to_db'
                self.status['sub'] = ''
            else:
                TelegramRequests.send_keyboard(self.user_id, """
                    Вы можете указать текстовую часть статьи для уточнения поиска
                    """, ['Подтверждаю', 'Отменить'])
                self.param_to_confim_value_dict['instruction']['words'].update(self.get_instruction_words_wage(text))
        elif self.status['gen'] == 'add_instruction_to_db':
            tags = ''
            for i in self.param_to_confim_value_dict['instruction']['tags']:
                tags += i + ', '
            TelegramRequests.send_message(self.user_id, """
            Вы добавили статью: {}
            Ссылка на статью: {}
            Тэги статьи: {}
                """.format(self.param_to_confim_value_dict['instruction']['title'], self.param_to_confim_value_dict['instruction']['link'], tags))
            self.create_instruction()
            self.clear_current_status('instruction')
        if text == "Отменить":
            self.clear_current_status('instruction')

    def find_instruction(self):
        obj = self.messages_all[-1]
        # text = obj.text
        if self.status['gen'] == "":
            self.status = ['instruction_get_question', '']
            TelegramRequests.send_message(self.user_id, 'Введите вопрос на который вы хотите получить инструкцию.')
        elif self.status['gen'] == 'instruction_get_question':
            if obj.text:
                self.instruction_question = obj
            self.status = ['instruction_confim_question', '']
            self.find_instruction()
        elif self.status['gen'] == 'instruction_confim_question':
            self.status = ['instruction_find', '']
            self.find_instruction()
        elif self.status['gen'] == 'instruction_find':
            if obj.text:
                # print(obj.text)
                self.text_query += ' ' + obj.text
                cur_text = pd.Series(list(self.get_instruction_words_wage(obj.text).keys()))
                print(cur_text)
                if not cur_text.empty:
                    cur_text = cur_text[cur_text.isin(self.instruction_big_data.columns)]
                    res = self.instruction_big_data
                    res = self.instruction_big_data.filter(items=cur_text, axis=1)
                    res['summ'] = res.sum(axis=1)
                    res = res[res['summ'] > 0]
                    res = res.sort_values(by=['summ'], ascending=False)
                    print(self.text_query)
                    print(res)
                    # length = len(res)
                    res_limit = res.head(5)
                    instructions = self.db.Instruction.get_by_list_ids(list(res_limit.index))
                    cur_message = ""
                    for instr in instructions:
                        link = instr['link']
                        title = instr['title']
                        cur_message += '<a href="{}">{}</a>\n\n'.format(link, title)
                    if not cur_message:
                        TelegramRequests.send_message(self.user_id, 'Статья по вашему запросу не найдена. Отправляем запрос координатору. Скоро вам ответят в этом чате')
                        self.bot.control_session.request_instruction(obj, self.text_query)
                    else:
                        cur_message = "Найденные статьи: \n" + cur_message
                        if self.prev_instruction_message:
                            TelegramRequests.edit_message_text(self.user_id, self.prev_instruction_message.message_id, cur_message, parsemod_html=True, inline_keyboard=['Статья найдена', 'Статья не найдена'])
                        else:
                            self.prev_instruction_message = TelegramRequests(TelegramRequests.send_message(self.user_id, cur_message, parsemod_html=True, inline_buttons=['Статья найдена', 'Статья не найдена'], hide_keyboard=False))

                else:
                    TelegramRequests.send_message(self.user_id, 'Напишите более подробно ваш запрос. т.к. не удалось создать ключевые слова.')
            if obj.inline_data == "Статья найдена":
                # self.prev_instruction_message.print_obj()
                self.text_query = ''
                self.status = ["", ""]
                self.chine = []
                self.current_command = ''
                TelegramRequests.edit_message_reply_markup(self.user_id, self.prev_instruction_message.message_id)
                self.prev_instruction_message = None
            elif obj.inline_data == "Статья не найдена":
                TelegramRequests.send_message(self.user_id, 'Отправляем запрос координатору. Скоро вам ответят в этом чате')
                self.bot.control_session.request_instruction(self.instruction_question, self.text_query)

        #     res = self.bot.hashtag_cloud.get_hashtag_with_links(self.bot.hashtag_cloud.link_data)
        #     tags = {i: res[i] for i in res.keys()}
        #     self.current_inline_keypud = TelegramRequests(TelegramRequests.send_inline_keypud(self.user_id, "Нажмите на кнопку, который подходит под ваш запрос.", tags))
        #     self.status['sub'] = 'next'
        # elif obj.inline_data:
        #     if obj.inline_data == "Статья найдена":
        #         TelegramRequests.edit_inline_keypud(self.user_id, self.current_inline_keypud.message_id, self.cur_message, parsemod_html=True)
        #         self.status = ["", ""]
        #         self.chine = []
        #         self.current_command = ''
        #     elif obj.inline_data == "Статья не найдена":
        #         TelegramRequests.delete_message(self.user_id, self.current_inline_keypud.message_id)
        #         TelegramRequests.send_message(self.user_id, 'На ваш вопрос "{}" вскоре ответит координатор.'.format(self.instruction_question.text))
        #         self.status = ["", ""]
        #         self.chine = []
        #         self.current_command = ''
        #     else:
        #         res = self.bot.hashtag_cloud.get_hashtag_with_links(self.bot.hashtag_cloud.link_data, parameter_confims=self.chine)
                # if type(res) != list:
                #     for key in res.values():
                #         links = self.db.Instruction.get_by_list_ids(key)
                #         self.cur_message = ""
                #         tt = 10
                #         for el in links:
                #             if tt == 0:
                #                 break
                #             tt -= 1
                #             title = el['title']
                #             link = el['link']
                #             self.cur_message += '<a href="{}">{}</a>\n\n'.format(link, title)
                #         TelegramRequests.edit_inline_keypud(self.user_id, self.current_inline_keypud.message_id, self.cur_message, parsemod_html=True, reject_text="Статья не найдена", confim_text="Статья найдена")
                # if obj.inline_data in res.keys():
                # print(res.keys())
                # self.chine.append(obj.inline_data)
                # res = self.bot.hashtag_cloud.get_hashtag_with_links(self.bot.hashtag_cloud.link_data, parameter_confims=self.chine)
                # if type(res) != list:
                #     tags = {i: res[i] for i in res.keys()}
                #     all_links = []
                #     tt = 10
                #     for i in res.values():
                #         all_links += i
                #     links = self.db.Instruction.get_by_list_ids(all_links)
                #     self.cur_message = ""
                #     for el in links:
                #         if tt == 0:
                #             break
                #         tt -= 1
                #         title = el['title']
                #         link = el['link']
                #         self.cur_message += '<a href="{}">{}</a>\n\n'.format(link, title)
                #     TelegramRequests.edit_inline_keypud(self.user_id, self.current_inline_keypud.message_id, self.cur_message, buttons=tags, parsemod_html=True, confim_text="Статья найдена", reject_text="Статья не найдена",)
        


                #     links = self.db.Instruction.get_by_list_ids(res)
                #     self.cur_message = ""
                #     tt = 10
                #     for el in links:
                #         if tt == 0:
                #             break
                #         tt -= 1
                #         title = el['title']
                #         link = el['link']
                #         self.cur_message += '<a href="{}">{}</a>\n\n'.format(link, title)
                #     TelegramRequests.edit_inline_keypud(self.user_id, self.current_inline_keypud.message_id, self.cur_message, parsemod_html=True, reject_text="Статья не найдена", confim_text="Статья найдена")

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
        if not words_count:
            words_count = 1
        for i in text_split:
            res.setdefault(i, text_split.count(i) / words_count)
        for i in list(res.keys()):
            res2 = self.morph.parse(i)
            res.setdefault(res2[0].normal_form, res[i])
        return res

    @property
    def instruction_big_data(self):
        self.__class__._instruction_big_data = self.db.Instruction.get_big_data()
        return self.__class__._instruction_big_data
