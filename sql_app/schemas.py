from decimal import Decimal
from pydantic import BaseModel


class ItemBase(BaseModel):
    sku: int
    nome: str


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    cod_barras1: str | None = None
    cod_barras2: str | None = None
    referencia: str | None = None
    preco_custo: Decimal
    preco_real: Decimal
    preco_venda1: Decimal
    cfop_nfe: int | None = None
    cfop_sat: int | None = None


    class Config:
        from_attributes = True