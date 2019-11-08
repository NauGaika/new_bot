import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
# from .Tag import Tag
import pandas as pd
import numpy as np

Base = __builtins__['Base']
Session = __builtins__['Session']


class Instruction(Base):
    __tablename__ = 'instructions'
    all_links = None
    id = Column(Integer, primary_key=True)
    title = Column(String)
    link = Column(String)
    creator_id = Column(Integer, ForeignKey('users.telegramm_id'))
    date = Column(DateTime, default=datetime.datetime.utcnow())
    relevance = Column(Boolean, default=True)
    tags = relationship("Instruction_association", backref="instructions")

    def __init__(self, title, link, user):
        self.title = title
        self.link = link
        self.creator_id = user

    def __repr__(self):
        return "<Instruction('%s'>" % (self.title)

    @classmethod
    def all_links_to_memory(cls):
        if cls.all_links is None:
            session = Session()
            result = {}
            res = session.query(cls.id, cls.title, cls.link).all()
            for i in res:
                result.setdefault(int(i.id), {'title': i.title, 'link': i.link})
            cls.all_links = result
            print("Загрузили ссылки из базы")
        return cls.all_links

    @classmethod
    def create_new(cls, title, link, user):
        session = Session()
        el = cls(title, link, user)
        session.add(el)
        session.commit()
        el_id = int(el.id)
        print("Создали новую статью '{}'".format(el.title))
        return el_id

    @classmethod
    def is_link_exist(cls, text):
        session = Session()
        res = session.query(cls).filter_by(link=text).count()
        session.commit()
        if res:
            return True

    @classmethod
    def get_all_instruction(cls):
        session = Session()
        res = session.query(cls).all()
        return res

    @classmethod
    def get_by_list_ids(cls, elem_ids):
        elems = cls.all_links_to_memory()
        res = [elems[i] for i in elem_ids]
        return res

    @classmethod
    def get_big_data(cls):
        session = Session()
        instructions = session.query(cls).all()
        instructions = {instruction.id: {tag.tag.tag: tag.wage for tag in instruction.tags} for instruction in instructions}
        tags = set()
        for i in instructions.values():
            for b in i.keys():
                tags.add(b)
        arr = np.zeros((len(instructions.keys()), len(tags)))
        df = pd.DataFrame(data=arr, index=instructions.keys(), columns=tags)
        for i in instructions.keys():
            for b in instructions[i].keys():
                df[b][i] = instructions[i][b]
        return df

    @classmethod
    def get_by_link(cls, link):
        session = Session()
        res = session.query(cls).filter_by(link=link)
        if res.count():
            return res.one(), session
