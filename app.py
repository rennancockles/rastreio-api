import os
from typing import Any, Optional

from correios import Correios
from correios.entities import Evento, Objeto
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from pydantic import BaseModel

correios = Correios()
app = FastAPI(
    title="Rastreio Correios",
    description="API de rastreio de pacotes dos correios",
    openapi_prefix=os.getenv("OPENAPI_PREFIX", ""),
)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class CodigoRastreio(BaseModel):
    numero: Optional[str]


@app.get("/track/{objeto}", response_model=Objeto)
def track(objeto: str) -> Any:
    """Obtém dados do rastreio de um pacote"""
    rastro = correios.rastreio(objeto)
    if rastro.categoria.lower().startswith("erro"):
        raise HTTPException(
            status_code=404,
            detail=f"{rastro.categoria.removesuffix('.')}: {rastro.numero}",
        )
    return rastro


@app.get("/last/{objeto}", response_model=Evento)
def last(objeto: str) -> Any:
    """Obtém dados do último evendo do rastreio de um pacote"""
    rastro = correios.rastreio(objeto)
    if len(rastro.eventos) > 0:
        return rastro.eventos[0]
    raise HTTPException(
        status_code=404, detail=f"{rastro.categoria.removesuffix('.')}: {rastro.numero}"
    )


@app.get("/generate/{objeto}", response_model=CodigoRastreio)
def generate(objeto: str) -> Any:
    """Gera um dígito verificador válido para um código de rastreio"""
    return CodigoRastreio(numero=correios.gera_codigo_valido(objeto))


@app.get("/find/{cep}/{objeto}")
def find(cep: str, objeto: str, previous: int = 0, next: int = 10) -> Any:
    """Busca um código de rastreio que pertença a um determinado CEP"""
    return CodigoRastreio(numero=correios.busca_por_cep(cep, objeto, previous, next))


handler = Mangum(app=app)
