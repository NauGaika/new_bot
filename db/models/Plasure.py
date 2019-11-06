import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey

Base = __builtins__['Base']
Session = __builtins__['Session']


class Plasure(Base):
    __tablename__ = 'plasures'

    id = Column(Integer, primary_key=True)
    thanksgiving_id = Column(Integer, ForeignKey('users.telegramm_id'))
    gratefull_id = Column(Integer, ForeignKey('users.telegramm_id'))
    date = Column(DateTime, default=datetime.datetime.utcnow())

    # def __init__(self, thanksgiving_id, gratefull_id):
    #     self.gratefull_id = gratefull_id
    #     self.thanksgiving_id = thanksgiving_id

    def __repr__(self):
        return "<Plasure('%s'>" % (self.id)

    @classmethod
    def make_plasure(cls, thanksgiving_id, gratefull_id):
        session = Session()
        el = cls()
        el.thanksgiving_id = thanksgiving_id
        el.gratefull_id = gratefull_id
        session.add(el)
        session.commit()
