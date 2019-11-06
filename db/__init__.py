from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///test.db', echo=False)
Session = sessionmaker(bind=engine)

__builtins__.setdefault('Session', Session)

from .models import Department, Position, User, Common_parameter, Instruction, Tag, Plasure