import databases
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from core.config import settings

database = databases.Database(settings.SQLALCHEMY_DATABASE_URL)

Base = declarative_base()

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL,
                       pool_pre_ping=True,
                       echo=settings.DEBUG,
                       future=True,  # Use 2.0 style
                       connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False,
                            future=True,  # Use 2.0 style
                            bind=engine)
