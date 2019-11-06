from sqlalchemy import Column, Integer, String, Table, ForeignKey

from sqlalchemy.orm import relationship

Base = __builtins__['Base']

chine_resolve = Table(
    'chine_resolve',
    Base.metadata,
    Column('chine_id', Integer, ForeignKey('chines.id')),
    Column('resolve_id', Integer, ForeignKey('instructions.id')),
)


class Chine(Base):
    __tablename__ = 'chines'

    id = Column(Integer, primary_key=True)
    chine = Column(String)
    full_question = Column(String)
    resolve = relationship('Instruction', secondary=chine_resolve, backref='instruction')
    user_id = Column(Integer, ForeignKey('users.telegramm_id'))

    def __init__(self, chine, resolve=None):
        self.chine = chine
        self.resolve = resolve

    def __repr__(self):
        return "<chine(%s)>" % (self.id)
