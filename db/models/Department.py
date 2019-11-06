from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

Base = __builtins__['Base']
Session = __builtins__['Session']


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    head_department_id = Column(Integer, ForeignKey('departments.id'))
    gen_department = relationship("Department", remote_side="Department.id", backref=backref("sub_departments"), lazy="joined")

    def __init__(self, name):
        self.name = name
        self.department_id = None

    @classmethod
    def create_departments_if_not_exist(cls, pik_department):
        chine_arr = []
        session = Session()
        pik_department.department_chine(chine_arr)
        if chine_arr:
            prev = None
            for i in reversed(chine_arr):
                find = session.query(cls).filter_by(name=i.Name)
                if find.count() == 0:
                    print("Создаем департамент " + i.Name)
                    el = cls(i.Name)
                    session.add(el)
                else:
                    print("Департамент уже существует  " + i.Name)
                    el = find.one()
                if prev is not None:
                    el.gen_department = prev
                prev = el
        el_id = el.id
        session.commit()
        return el_id
