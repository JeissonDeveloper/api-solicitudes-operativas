# Integración con Power Automate

Este backend se consume desde un flujo con la acción **HTTP**.
No hace falta conector premium de SQL si la API queda publicada (Azure, on-prem con gateway, o un entorno interno).

## Flujo típico

1. Trigger: elemento creado en SharePoint, envío de formulario o correo.
2. Acción HTTP — crear solicitud.
3. Acción de aprobación (Approvals o correo).
4. Acción HTTP — registrar la decisión.
5. Condición: notificar al solicitante.

## POST — crear solicitud

- Método: `POST`
- URI: `https://TU-HOST/api/solicitudes`
- Headers: `Content-Type: application/json`
- Body:

```json
{
  "documento": "@{outputs('Obtener_empleado')?['documento']}",
  "tipo": "cambio_turno",
  "descripcion": "@{triggerBody()?['descripcion']}"
}
```

Respuesta esperada `201`:

```json
{
  "id": 1,
  "colaborador_id": 1,
  "tipo": "cambio_turno",
  "descripcion": "Cambio de turno del 22 al 23 de agosto",
  "estado": "pendiente",
  "creada_en": "2026-09-04T02:00:00+00:00",
  "actualizada_en": "2026-09-04T02:00:00+00:00"
}
```

Guarda `id` en una variable del flujo.

## PATCH — decisión

- Método: `PATCH`
- URI: `https://TU-HOST/api/solicitudes/@{variables('solicitud_id')}/decision`
- Body:

```json
{ "estado": "aprobada" }
```

Si el flujo intenta decidir dos veces, la API responde `409`. Eso evita estados sucios cuando un aprobador reenvía el correo.

## Errores que el flujo debe contemplar

| HTTP | Cuándo | Qué hacer en Automate |
|---|---|---|
| 404 | Documento no existe | Correo a mesas de ayuda / crear colaborador |
| 409 | Duplicado o ya resuelta | Terminar flujo, no reintentar |
| 422 | JSON inválido | Revisar mapeo del formulario |

## Por qué esta pieza importa en el perfil

Power Automate solo no alcanza cuando hay validación, historial y reportes.
La API deja las reglas en un solo lugar (SQL + endpoints) y el flujo orquesta personas y notificaciones.
