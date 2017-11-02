from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CPU(Base):
    __tablename__ = 'cpus'

    id = Column(Integer, primary_key=True)
    name = Column(String)
