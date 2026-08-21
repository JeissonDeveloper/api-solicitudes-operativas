# API de Solicitudes Operativas

API REST en **Python + FastAPI + SQL** para gestionar solicitudes internas:
alta de colaboradores, creación de solicitudes, aprobación/rechazo y un reporte simple.

Este proyecto demuestra lo que un analista de automatización necesita cuando una empresa pregunta:
“¿Sabes SQL? ¿Sabes APIs?” — sí, y aquí está el código.

## Qué resuelve

En operaciones reales (cambio de turno, autorizaciones, tickets) el proceso suele vivir en Excel, correos y WhatsApp. Esta API es el núcleo de una automatización:

1. Un formulario o un flujo de Power Automate envía un `POST`.
2. La API valida al colaborador y guarda la solicitud en SQL.
3. Un aprobador cambia el estado con `PATCH`.
4. Un reporte cuenta pendientes / aprobadas / rechazadas.

## Stack

- Python 3.11+
- FastAPI
- SQLAlchemy + SQLite (SQL real, fácil de migrar a PostgreSQL)
- Pydantic
- Pytest

## Cómo correrla

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Abre la documentación interactiva: http://127.0.0.1:8000/docs

## Endpoints

| Método | Ruta | Qué hace |
|---|---|---|
| GET | `/health` | Salud del servicio |
| POST | `/api/colaboradores` | Crea colaborador |
| POST | `/api/solicitudes` | Crea solicitud (JSON) |
| GET | `/api/solicitudes` | Lista (filtros `estado`, `tipo`) |
| GET | `/api/solicitudes/{id}` | Consulta una solicitud |
| PATCH | `/api/solicitudes/{id}/decision` | Aprueba o rechaza |
| GET | `/api/reportes/resumen` | Totales por estado |

Ejemplo de alta:

```json
{
  "documento": "1001234567",
  "tipo": "cambio_turno",
  "descripcion": "Cambio de turno del 22 al 23 de agosto"
}
```

## Pruebas

```bash
pytest -q
```

## Cómo se conecta con Power Automate

En un flujo real:

1. Trigger: elemento creado en SharePoint o envío de formulario.
2. Acción HTTP: `POST /api/solicitudes` con el JSON.
3. Condición / aprobación.
4. Acción HTTP: `PATCH /api/solicitudes/{id}/decision`.

Eso es exactamente el perfil híbrido: **low-code + API + SQL**.

## Autor

Jeisson Javier Silva Beltrán — [github.com/JeissonDeveloper](https://github.com/JeissonDeveloper)
