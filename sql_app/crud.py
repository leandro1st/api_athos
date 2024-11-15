from sqlalchemy.orm import Session
from . import models


def get_all_items(db: Session):
    return db.query(models.Item).all()

def get_last_item(db: Session):
    return db.query(models.Item).order_by(models.Item.sku.desc()).first()

def get_item(db: Session, sku: int):
    return db.query(models.Item).filter(models.Item.sku == sku).first()

def get_gtin(db: Session, gtin: str):
    return db.query(models.Gtin).filter(models.Gtin.gtin == gtin).first()