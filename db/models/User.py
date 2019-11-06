from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from .Plasure import Plasure
Base = __builtins__['Base']
Session = __builtins__['Session']


class User(Base):
    __tablename__ = 'users'
    telegramm_id = Column(Integer, primary_key=True)
    pik_id = Column(Integer)
    username = Column(String)
    name = Column(String)
    fullname = Column(String)
    patronymic = Column(String)
    email = Column(String)
    department_id = Column(Integer, ForeignKey('departments.id'))
    department = relationship('Department', lazy="joined")
    position_id = Column(Integer, ForeignKey('positions.Id'))
    position = relationship('Position', lazy="joined")
    plasures = Column(Integer, default=0)
    is_admin = Column(Boolean, default=0)
    instructions = relationship("Instruction", lazy="joined")
    gratefull = relationship(
        "User",
        secondary=Plasure.__tablename__,
        primaryjoin='User.telegramm_id==Plasure.gratefull_id',
        secondaryjoin='User.telegramm_id==Plasure.thanksgiving_id',
        backref="thanksgiving")

    def __init__(self, telegramm_id):
        self.telegramm_id = telegramm_id

    def __repr__(self):
        return "<User('%s' telegramm_id '%s' username '%s')>" % (self.email, self.telegramm_id, self.username)

    @classmethod
    def get_user(cls, upd):
        username = upd.username
        session = Session()
        res = session.query(cls).filter_by(telegramm_id=upd.sender_id)
        if res.count() == 1:
            el = res.one()
            if el.username != username:
                el.username = username
                session.commit()
            return res.one()
        else:
            el = cls(upd.sender_id)
            el.username = username
            session.add(el)
            session.commit()
            return el

    @classmethod
    def get_user_by_id(cls, user_id, username=None):
        session = Session()
        res = session.query(cls).filter_by(telegramm_id=user_id)
        if res.count() == 1:
            el = res.one()
            if username:
                if el.username != username:
                    el.username = username
                    session.commit()
            return res.one()
        else:
            el = cls(user_id)
            if username:
                el.username = username
            session.add(el)
            session.commit()
            return el

    @classmethod
    def set_private_chat(cls, telegramm_id, chat_id):
        session = Session()
        res = session.query(cls).filter_by(telegramm_id=telegramm_id)
        if res.count() == 1:
            if res.one().private_chat != chat_id:
                res.one().private_chat = chat_id
        session.commit()

    @classmethod
    def get_user_by_telegramm(cls, telegramm_id):
        session = Session()
        res = session.query(cls).filter_by(telegramm_id=telegramm_id)
        if res.count() == 1:
            return res.one()

    @classmethod
    def set_param(cls, telegramm_id, parameter, value):
        session = Session()
        res = session.query(cls).filter_by(telegramm_id=telegramm_id)
        if res.count() == 1:
            res = res.one()
            setattr(res, parameter, value)
        session.commit()

    @classmethod
    def get_user_by_username(cls, username):
        session = Session()
        res = session.query(cls).filter_by(username=username)
        if res.count() == 1:
            return res.one()

    @classmethod
    def add_plasures(cls, telegramm_id, count=1):
        session = Session()
        res = session.query(cls).filter_by(telegramm_id=telegramm_id)
        if res.count() == 1:
            el = res.one()
            el.plasures += count
        session.commit()

    @classmethod
    def get_all_instructions_count(cls, telegramm_id):
        session = Session()
        res = session.query(cls.instructions).filter_by(telegramm_id=telegramm_id)
        return res.count()

    @classmethod
    def set_fio(cls, user_id, fio):
        session = Session()
        user = session.query(cls).filter_by(telegramm_id=user_id).one()
        res = fio.split(' ')
        if res:
            if len(res) > 0:
                user.fullname = res[0]
            if len(res) > 1:
                user.name = res[1]
            if len(res) > 2:
                user.patronymic = res[2]
        session.commit()

    @classmethod
    def set_department_id(cls, user_id, dep_id):
        session = Session()
        user = session.query(cls).filter_by(telegramm_id=user_id).one()
        user.department_id = dep_id
        session.commit()

    @classmethod
    def set_position_id(cls, user_id, position_id):
        session = Session()
        user = session.query(cls).filter_by(telegramm_id=user_id).one()
        user.position_id = position_id
        session.commit()

    @classmethod
    def set_pik_id(cls, user_id, pik_id):
        session = Session()
        user = session.query(cls).filter_by(telegramm_id=user_id).one()
        user.pik_id = pik_id
        session.commit()

    @classmethod
    def clear_email(cls, user_id):
        session = Session()
        user = session.query(cls).filter_by(telegramm_id=user_id).one()
        user.email = ""
        session.commit()

    @property
    def fio(self):
        return "{} {} {}".format(self.fullname, self.name, self.patronymic)
    
