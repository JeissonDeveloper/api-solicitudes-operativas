from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Colaborador, Solicitud, utc_now
from app.schemas import (
    ColaboradorCreate,
    ColaboradorOut,
    DecisionIn,
    SolicitudCreate,
    SolicitudOut,
)

router = APIRouter()


@router.post("/colaboradores", response_model=ColaboradorOut, status_code=201)
def crear_colaborador(payload: ColaboradorCreate, db: Session = Depends(get_db)):
    existe = db.scalar(select(Colaborador).where(Colaborador.documento == payload.documento))
    if existe:
        raise HTTPException(status_code=409, detail="El documento ya está registrado")
    colaborador = Colaborador(**payload.model_dump())
    db.add(colaborador)
    db.commit()
    db.refresh(colaborador)
    return colaborador


@router.post("/solicitudes", response_model=SolicitudOut, status_code=201)
def crear_solicitud(payload: SolicitudCreate, db: Session = Depends(get_db)):
    colaborador = db.scalar(
        select(Colaborador).where(
            Colaborador.documento == payload.documento,
            Colaborador.activo == 1,
        )
    )
    if not colaborador:
        raise HTTPException(status_code=404, detail="Colaborador no encontrado o inactivo")

    solicitud = Solicitud(
        colaborador_id=colaborador.id,
        tipo=payload.tipo,
        descripcion=payload.descripcion,
    )
    db.add(solicitud)
    db.commit()
    db.refresh(solicitud)
    return solicitud


@router.get("/solicitudes", response_model=list[SolicitudOut])
def listar_solicitudes(
    estado: str | None = Query(default=None),
    tipo: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    stmt = select(Solicitud)
    if estado:
        stmt = stmt.where(Solicitud.estado == estado)
    if tipo:
        stmt = stmt.where(Solicitud.tipo == tipo)
    return db.scalars(stmt.order_by(Solicitud.id.desc())).all()


@router.get("/solicitudes/{solicitud_id}", response_model=SolicitudOut)
def obtener_solicitud(solicitud_id: int, db: Session = Depends(get_db)):
    solicitud = db.get(Solicitud, solicitud_id)
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    return solicitud


@router.patch("/solicitudes/{solicitud_id}/decision", response_model=SolicitudOut)
def decidir_solicitud(
    solicitud_id: int, payload: DecisionIn, db: Session = Depends(get_db)
):
    solicitud = db.get(Solicitud, solicitud_id)
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    if solicitud.estado != "pendiente":
        raise HTTPException(status_code=409, detail="La solicitud ya fue resuelta")

    solicitud.estado = payload.estado
    solicitud.actualizada_en = utc_now()
    db.commit()
    db.refresh(solicitud)
    return solicitud


@router.get("/reportes/resumen")
def resumen(db: Session = Depends(get_db)):
    filas = db.execute(
        select(Solicitud.estado, func.count(Solicitud.id)).group_by(Solicitud.estado)
    ).all()
    return {estado: total for estado, total in filas}
