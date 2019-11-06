from sqlalchemy import Column, Integer, String

Session = __builtins__['Session']
Base = __builtins__['Base']


class Common_parameter(Base):
    __tablename__ = 'common_parameters'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    value = Column(String)

    def __init__(self, title, value):
        self.title = title
        self.value = value

    def __repr__(self):
        return "<Common_parameter('%s' - '%s')>" % (self.title, self.value)

    @classmethod
    def set_parameter(cls, parameter, value):
        session = Session()
        parameter = parameter.lower()
        res = session.query(cls).filter_by(title=parameter)
        if res.count() == 1:
            parameter = res.one()
        else:
            el = cls(parameter, value)
            session.add(el)
        session.commit()

    @classmethod
    def get_parameter(cls, parameter):
        session = Session()
        parameter = parameter.lower()
        res = session.query(cls).filter_by(title=parameter)
        if res.count() == 1:
            parameter = res.one()
            return parameter.value
