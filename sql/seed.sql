-- Datos de demostración (SQLite)
INSERT INTO colaboradores (documento, nombre, area, activo) VALUES
    ('1001234567', 'Ana Pérez', 'Operaciones', 1),
    ('2002002002', 'Luis Mora', 'TI', 1);

INSERT INTO solicitudes (colaborador_id, tipo, descripcion, estado) VALUES
    (1, 'cambio_turno', 'Cambio de turno del 22 al 23 de agosto', 'pendiente'),
    (1, 'autorizacion', 'Descuento de nómina septiembre', 'aprobada'),
    (2, 'soporte', 'Acceso a aplicación corporativa', 'rechazada');
