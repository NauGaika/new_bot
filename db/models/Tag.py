from sqlalchemy import Column, Integer, String, Table, ForeignKey, Float, MetaData, and_
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from .Instruction import Instruction

Session = __builtins__['Session']
Base = __builtins__['Base']

metadata = MetaData()


class Instruction_association(Base):
    __tablename__ = 'instruction_associations'
    instruction_id = Column(Integer, ForeignKey('instructions.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)
    tag = relationship("Tag", backref="tags", lazy="joined")
    instruction = relationship("Instruction", backref="instructions", lazy="joined")
    wage = Column(Float, default=0)


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    tag = Column(String)
    instructions = relationship('Instruction_association', backref='tags')

    def __init__(self, tag):
        self.tag = tag

    def __repr__(self):
        return "<Tag = '%s')>" % (self.tag)

    @classmethod
    def create_tags_with_wage(cls, tags_with_wage, instruction_id=None, koef=1, def_wage=0.1):
        """Создаем тэги, которых не хватает в базе.

        Создаем тэги, которые переданы в tags_with_wage
        Тэги создаются, если их нет. Если они есть - они грузятся
        в tags_with_wage

        Если передается list - всем элементам назначается
        вес из def_wage.

        Если передается инструкция, то данные тэги назначаются
        ей.
        """
        session = Session()
        with session.no_autoflush:
            all_tags = session.query(cls)
            all_tags = {i.tag: i for i in all_tags.all()}

            if isinstance(tags_with_wage, list):
                tags_with_wage = {i: def_wage for i in tags_with_wage}

            if instruction_id is not None:
                instruction = session.query(Instruction).filter_by(id=instruction_id).one()
            all_instruction_associations = set()
            for i in instruction.tags:
                all_instruction_associations.add(i.tag.tag)
            # print(all_instruction_associations)
            for i in tags_with_wage.keys():
                if i not in all_tags.keys():
                    cur_tag = cls(i)
                    all_tags.setdefault(cur_tag.tag, cur_tag)
                else:
                    cur_tag = all_tags[i]
                if cur_tag.tag not in all_instruction_associations:
                    # print(cur_tag.tag)
                    assa = Instruction_association(wage=tags_with_wage[i])
                    assa.tag = cur_tag
                    assa.instruction = instruction
        session.commit()

    @classmethod
    def get_all_hashtag(cls):
        session = Session()
        res = session.query(cls)
        if res.count():
            all_tags = res.all()
            return all_tags

    @classmethod
    def teg_from_text(cls, text):
        res = cls.templ.findall(text)
        res = list(set([i.lower() for i in res]))
        res = [cls.morph.parse(i)[0] for i in res if i not in cls.stop_words]
        res = [i.normal_form for i in res]
        return res

    @classmethod
    def check_exist(cls, tags):
        session = Session()
        exists = []
        not_exists = []
        for i in tags:
            res = session.query(cls.tag).filter_by(tag=i)
            if res.count():
                exists.append(i)
            else:
                not_exists.append(i)
        return exists, not_exists

    @classmethod
    def add_new_keywords_to_instruction(cls, instruction, tags, session=None):
        if session is not None:
            for tag in tags:
                res = session.query(cls).filter_by(tag=tag)
                if res.count():
                    cur_tag = res.one()
                    is_add = False
                else:
                    cur_tag = cls(tag)
                    is_add = True
                if not is_add:
                    print(cur_tag)
                    print(instruction)
                    res_2 = session.query(Instruction_association).filter_by(tag_id=cur_tag.id).filter_by(instruction_id=instruction.id)
                if not is_add and res_2.count():
                    res_2 = res_2.one()
                    res_2.wage += 0.03
                else:
                    ass = Instruction_association(wage=0.03)
                    ass.instruction = instruction
                    ass.tag = cur_tag
        session.commit()