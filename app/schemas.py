from typing import Literal

from pydantic import BaseModel, Field

TipoSolicitud = Literal["cambio_turno", "autorizacion", "soporte"]
EstadoSolicitud = Literal["pendiente", "aprobada", "rechazada"]


class ColaboradorCreate(BaseModel):
    documento: str = Field(min_length=5, max_length=20)
    nombre: str = Field(min_length=3, max_length=120)
    area: str = Field(min_length=2, max_length=80)


class ColaboradorOut(BaseModel):
    id: int
    documento: str
    nombre: str
    area: str
    activo: int

    model_config = {"from_attributes": True}


class SolicitudCreate(BaseModel):
    documento: str
    tipo: TipoSolicitud
    descripcion: str = Field(min_length=5, max_length=500)


class SolicitudOut(BaseModel):
    id: int
    colaborador_id: int
    tipo: TipoSolicitud
    descripcion: str
    estado: EstadoSolicitud
    creada_en: str
    actualizada_en: str

    model_config = {"from_attributes": True}


class DecisionIn(BaseModel):
    estado: Literal["aprobada", "rechazada"]
