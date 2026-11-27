-- Se ejecutó una vez (2026-11-27) para pasar a fotos en HD. La tabla nueva ya trae estas columnas en schema.sql.
ALTER TABLE confirmaciones ADD COLUMN hd_tipo TEXT;
ALTER TABLE confirmaciones ADD COLUMN hd_bytes INTEGER;
ALTER TABLE confirmaciones ADD COLUMN token TEXT;
