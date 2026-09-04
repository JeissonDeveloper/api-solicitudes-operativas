# API de Solicitudes Operativas

Backend REST en **Python + FastAPI + SQL** para digitalizar solicitudes internas:
alta de colaborador, creación de solicitud, aprobación o rechazo, y un reporte por estado.

Es el puente entre un formulario / Power Automate y una base de datos. No es un tutorial: es el núcleo que un flujo low-code necesita cuando Excel y el correo ya no escalan.

## Problema

En operaciones (cambio de turno, autorización, soporte) el proceso vive en Excel, correos y WhatsApp.
Esta API concentra la regla de negocio:

1. Un formulario o un flujo envía `POST /api/solicitudes`.
2. La API valida que el colaborador exista y esté activo, y persiste en SQL.
3. Un aprobador decide con `PATCH /api/solicitudes/{id}/decision`.
4. Un reporte agrupa pendientes / aprobadas / rechazadas.

```text
Formulario web  →  Power Automate (HTTP)  →  FastAPI  →  SQL
                         ↑
                   Aprobación / rechazo
```

## Stack

- Python 3.11+
- FastAPI + Pydantic
- SQLAlchemy 2 + SQLite (SQL real; se puede apuntar a PostgreSQL con `DATABASE_URL`)
- Pytest

## Cómo correrla

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

- Swagger: http://127.0.0.1:8000/docs
- Salud: http://127.0.0.1:8000/health

## Endpoints

| Método | Ruta | Qué hace |
|---|---|---|
| GET | `/health` | Salud del servicio |
| POST | `/api/colaboradores` | Crea colaborador |
| POST | `/api/solicitudes` | Crea solicitud |
| GET | `/api/solicitudes` | Lista (filtros `estado`, `tipo`) |
| GET | `/api/solicitudes/{id}` | Consulta una solicitud |
| PATCH | `/api/solicitudes/{id}/decision` | Aprueba o rechaza |
| GET | `/api/reportes/resumen` | Totales por estado (`GROUP BY`) |

### Alta de colaborador

```json
{
  "documento": "1001234567",
  "nombre": "Ana Pérez",
  "area": "Operaciones"
}
```

### Alta de solicitud

```json
{
  "documento": "1001234567",
  "tipo": "cambio_turno",
  "descripcion": "Cambio de turno del 22 al 23 de agosto"
}
```

`tipo` acepta: `cambio_turno` | `autorizacion` | `soporte`.

### Decisión

```json
{ "estado": "aprobada" }
```

Reglas de negocio que un entrevistador suele preguntar:

- Documento duplicado → `409`
- Colaborador inexistente o inactivo → `404`
- Decidir una solicitud que ya no está pendiente → `409`

## Pruebas

```bash
pytest -q
```

Corren contra SQLite en memoria. No tocan `solicitudes.db`.

## Integración con Power Automate

Ver [docs/integracion-power-automate.md](docs/integracion-power-automate.md).

Resumen: trigger (SharePoint o formulario) → acción HTTP `POST` → aprobación → HTTP `PATCH`.

## Estructura

```text
app/
  main.py              # FastAPI + /health
  database.py          # motor SQL
  models.py            # tablas y constraints
  schemas.py           # contratos Pydantic
  routers/solicitudes.py
sql/
  schema.sql           # modelo en SQL puro
  seed.sql             # datos de demo
docs/
  integracion-power-automate.md
tests/
```

## Autor

Jeisson Javier Silva Beltrán  
Analista de Automatización | Power Platform · Python · SQL · APIs REST  
[github.com/JeissonDeveloper](https://github.com/JeissonDeveloper)
