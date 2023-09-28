from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_url = "mysql+pymysql://root:root@localhost/APItube"

engine = create_engine(db_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base:
    __allow_unmapped__ = True

base = declarative_base(cls=Base)