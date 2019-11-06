from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


engine = create_engine('sqlite:///test.db', echo=True)

Session = sessionmaker(bind=engine)
__builtins__.Session = Session
import models



__builtins__.Base.metadata.create_all(engine)