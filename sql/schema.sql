-- Modelo de datos para solicitudes internas (SQLite / SQL estándar)

CREATE TABLE IF NOT EXISTS colaboradores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    documento TEXT NOT NULL UNIQUE,
    nombre TEXT NOT NULL,
    area TEXT NOT NULL,
    activo INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS solicitudes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    colaborador_id INTEGER NOT NULL,
    tipo TEXT NOT NULL CHECK (tipo IN ('cambio_turno', 'autorizacion', 'soporte')),
    descripcion TEXT NOT NULL,
    estado TEXT NOT NULL DEFAULT 'pendiente'
        CHECK (estado IN ('pendiente', 'aprobada', 'rechazada')),
    creada_en TEXT NOT NULL DEFAULT (datetime('now')),
    actualizada_en TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (colaborador_id) REFERENCES colaboradores(id)
);

CREATE INDEX IF NOT EXISTS idx_solicitudes_estado ON solicitudes(estado);
CREATE INDEX IF NOT EXISTS idx_solicitudes_tipo ON solicitudes(tipo);
