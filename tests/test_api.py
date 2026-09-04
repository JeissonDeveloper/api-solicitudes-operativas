def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_flujo_completo_solicitud(client):
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


def test_documento_duplicado(client):
    payload = {"documento": "2002002002", "nombre": "Luis Mora", "area": "TI"}
    assert client.post("/api/colaboradores", json=payload).status_code == 201
    assert client.post("/api/colaboradores", json=payload).status_code == 409


def test_solicitud_sin_colaborador(client):
    r = client.post(
        "/api/solicitudes",
        json={
            "documento": "0000000000",
            "tipo": "soporte",
            "descripcion": "Acceso a aplicación corporativa",
        },
    )
    assert r.status_code == 404


def test_no_decidir_dos_veces(client):
    client.post(
        "/api/colaboradores",
        json={"documento": "3003003003", "nombre": "Carla Ruiz", "area": "RRHH"},
    )
    alta = client.post(
        "/api/solicitudes",
        json={
            "documento": "3003003003",
            "tipo": "autorizacion",
            "descripcion": "Autorización de descuento nómina",
        },
    )
    sid = alta.json()["id"]
    assert client.patch(
        f"/api/solicitudes/{sid}/decision", json={"estado": "rechazada"}
    ).status_code == 200
    segunda = client.patch(
        f"/api/solicitudes/{sid}/decision", json={"estado": "aprobada"}
    )
    assert segunda.status_code == 409
