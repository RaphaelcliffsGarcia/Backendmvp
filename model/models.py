from sqlalchemy import create_engine, Column, Integer, String, Text, Float
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Transacao(Base):
    __tablename__ = 'transacao'
    id = Column(Integer, primary_key=True)
    descricao = Column(Text)
    valor = Column(Float)
    tipo = Column(String(255))