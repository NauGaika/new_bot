from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

Base = __builtins__['Base']
Session = __builtins__['Session']


class Position(Base):
    __tablename__ = "positions"

    Id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name

    @classmethod
    def create_position_if_not_exist(cls, positions):
        if positions:
            session = Session()
        for i in positions:
            find = session.query(cls).filter_by(name=i.Name)
            if find.count() == 0:
                el = cls(i.Name)
                session.add(el)
                print('Создана должность ' + el.name)
            else:
                el = find.one()
                print('Должность уже была создана ' + el.name)
        session.commit()
        el_id = el.Id
        return el_id
