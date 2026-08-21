from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class Colaborador(Base):
    __tablename__ = "colaboradores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    documento: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    area: Mapped[str] = mapped_column(String(80), nullable=False)
    activo: Mapped[int] = mapped_column(Integer, default=1)

    solicitudes: Mapped[list["Solicitud"]] = relationship(back_populates="colaborador")


class Solicitud(Base):
    __tablename__ = "solicitudes"
    __table_args__ = (
        CheckConstraint("tipo IN ('cambio_turno', 'autorizacion', 'soporte')", name="ck_tipo"),
        CheckConstraint("estado IN ('pendiente', 'aprobada', 'rechazada')", name="ck_estado"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    colaborador_id: Mapped[int] = mapped_column(ForeignKey("colaboradores.id"), nullable=False)
    tipo: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    estado: Mapped[str] = mapped_column(String(20), default="pendiente", index=True)
    creada_en: Mapped[str] = mapped_column(String(40), default=utc_now)
    actualizada_en: Mapped[str] = mapped_column(String(40), default=utc_now)

    colaborador: Mapped[Colaborador] = relationship(back_populates="solicitudes")
