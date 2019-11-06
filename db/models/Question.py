from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = __builtins__['Base']


class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    questioin = Column(String)

    def __init__(self, question):
        self.question = question

    def __repr__(self):
        return "<Question('%s'>" % (self.question)
