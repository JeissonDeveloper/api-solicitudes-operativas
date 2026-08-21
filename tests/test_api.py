from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_flujo_completo_solicitud():
    colab = client.post(
        "/api/colaboradores",
        json={"documento": "1001234567", "nombre": "Ana Pérez", "area": "Operaciones"},
    )
    assert colab.status_code == 201

    alta = client.post(
        "/api/solicitudes",
        json={
            "documento": "1001234567",
            "tipo": "cambio_turno",
            "descripcion": "Cambio de turno del 22 al 23 de agosto",
        },
    )
    assert alta.status_code == 201
    solicitud_id = alta.json()["id"]
    assert alta.json()["estado"] == "pendiente"

    decision = client.patch(
        f"/api/solicitudes/{solicitud_id}/decision",
        json={"estado": "aprobada"},
    )
    assert decision.status_code == 200
    assert decision.json()["estado"] == "aprobada"

    resumen = client.get("/api/reportes/resumen")
    assert resumen.status_code == 200
    assert resumen.json().get("aprobada", 0) >= 1
