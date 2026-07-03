from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from aos.config import DB_PATH, DATA_DIR
DATA_DIR.mkdir(exist_ok=True)
engine=create_engine(f'sqlite:///{DB_PATH}', echo=False, future=True)
SessionLocal=sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base=declarative_base()
@contextmanager
def get_session():
    s=SessionLocal()
    try: yield s
    finally: s.close()
def init_db():
    from aos.db import models
    Base.metadata.create_all(bind=engine)
