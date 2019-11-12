from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///G:\\Мой диск\\new_bot\\for_test.db', echo=False)
Session = sessionmaker(bind=engine)

__builtins__.setdefault('Session', Session)

from .models import Department, Position, User, Common_parameter, Instruction, Tag, Plasure, Instruction_association