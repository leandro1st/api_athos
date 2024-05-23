from typing import Any, List
from fastapi import Depends, FastAPI, HTTPException, Response
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import orjson
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine


class CustomORJSONResponse(Response):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        assert orjson is not None, "orjson must be installed"
        return orjson.dumps(content, option=orjson.OPT_INDENT_2)
    
models.Base.metadata.create_all(bind=engine)

app = FastAPI(default_response_class=CustomORJSONResponse)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def root():
    return '<h1>Bem-vindo!</h1>'

# @app.get("/items/", response_model=List[schemas.Item])
# def read_item(db: Session = Depends(get_db)):
#     db_item = crud.get_all_items(db)
#     if db_item is None:
#         raise HTTPException(status_code=404, detail="No items found")
#     return db_item

@app.get("/items/")
def read_item_empty():
    return {'sku': ''}

@app.get("/items/last", response_model=schemas.Item)
def read_item_last(db: Session = Depends(get_db)):
    db_item = crud.get_last_item(db)
    if db_item is None:
        raise HTTPException(status_code=404, detail="No item found")
    return db_item

@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="No item found")
    return db_item