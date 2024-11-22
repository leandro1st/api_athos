from decimal import Decimal
from pydantic import BaseModel


class Item(BaseModel):
    sku: int
    nome: str
    cod_barras1: str | None = None
    cod_barras2: str | None = None
    referencia: str | None = None
    preco_custo: Decimal
    preco_real: Decimal
    preco_venda1: Decimal
    cfop_nfe: int | None = None
    cfop_sat: int | None = None
    observacao: str | None = None

    class Config:
        from_attributes = True

class ItemUpdate(BaseModel):
    preco_custo: Decimal
    preco_real: Decimal
    preco_venda1: Decimal
    observacao: str


class Gtin(BaseModel):
    gtin: str
    sku: int

    class Config:
        from_attributes = True

class GtinCreate(BaseModel):
    sku: int