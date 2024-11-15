from sqlalchemy import Column, Integer, Numeric, String
from .database import Base


class Item(Base):
    __tablename__ = "produtos"

    sku = Column(Integer, primary_key=True)
    nome = Column(String)
    cod_barras1 = Column(String)
    cod_barras2 = Column(String)
    referencia = Column(String)
    preco_custo = Column(Numeric)
    preco_real = Column(Numeric)
    preco_venda1 = Column(Numeric)
    cfop_nfe = Column(Integer)
    cfop_sat = Column(Integer)
    observacao = Column(String)


class Gtin(Base):
    __tablename__ = "cod_barras"

    gtin = Column(String, primary_key=True)
    sku = Column(Integer)