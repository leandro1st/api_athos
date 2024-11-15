from typing import Any, List
from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
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

# 404 - not found
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({'sku': exc.detail})
    )

# 422 - type error
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({'sku': exc.errors()[0]['input']})
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

@app.get("/items/")
def read_item_empty():
    raise HTTPException(status_code=404, detail='')

@app.get("/items/{sku}", response_model=schemas.Item)
def read_item(sku: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, sku=sku)
    if db_item is None:
        raise HTTPException(status_code=404, detail=sku)
    
    return db_item

@app.patch("/items/")
def update_item_empty():
    raise HTTPException(status_code=404, detail='')

@app.patch("/items/{sku}", response_model=schemas.Item)
def update_item(sku: int, item_update: schemas.ItemUpdate, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, sku=sku)
    if db_item is None:
        raise HTTPException(status_code=404, detail=sku)
        
    db_item.preco_custo = item_update.preco_custo
    db_item.preco_venda1 = item_update.preco_venda1
    db_item.observacao = item_update.observacao
    db.commit()
    db.refresh(db_item)

    return db_item


@app.get("/gtin/")
def read_gtin_empty():
    raise HTTPException(status_code=404, detail='')

@app.get("/gtin/{gtin}", response_model=schemas.Gtin)
def read_gtin(gtin: str, db: Session = Depends(get_db)):
    db_gtin = crud.get_gtin(db, gtin=gtin)
    if db_gtin is None:
        raise HTTPException(status_code=404, detail='')
    
    return db_gtin

@app.post("/gtin/")
def create_gtin_empty():
    raise HTTPException(status_code=404, detail='')

@app.post("/gtin/{gtin}", response_model=schemas.Gtin)
def create_gtin(gtin: str, gtin_create: schemas.GtinCreate, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, sku=gtin_create.sku)
    if db_item is None:
        raise HTTPException(status_code=404, detail=gtin_create.sku)

    db_gtin = crud.get_gtin(db, gtin=gtin)
    if db_gtin is None:
        db_gtin = models.Gtin(gtin=gtin, sku=gtin_create.sku)
        db.add(db_gtin)
        db.commit()
        db.refresh(db_gtin)

    return db_gtin