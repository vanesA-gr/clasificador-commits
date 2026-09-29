-- Crear rol con privilegios mínimos
CREATE ROLE app_ia WITH LOGIN PASSWORD 'secreto_seguro';

-- Crear la tabla de inferencias
CREATE TABLE inferencias (
    id SERIAL PRIMARY KEY,
    commit_hash VARCHAR(64) NOT NULL,
    resultado_clasificacion VARCHAR(100) NOT NULL,
    motor_usado VARCHAR(50) NOT NULL,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Asignar permisos al usuario
GRANT SELECT, INSERT ON inferencias TO app_ia;
GRANT USAGE, SELECT ON SEQUENCE inferencias_id_seq TO app_ia;

