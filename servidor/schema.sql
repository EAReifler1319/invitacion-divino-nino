-- Una fila por familia. Si la misma familia confirma otra vez, se actualiza (no se duplica).
CREATE TABLE IF NOT EXISTS confirmaciones (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  clave       TEXT    NOT NULL UNIQUE,   -- nombre normalizado (para no duplicar)
  familia     TEXT    NOT NULL,          -- como lo escribieron
  personas    INTEGER NOT NULL,
  foto        BLOB,                      -- miniatura (~40 KB) para ver la lista rápido
  foto_tipo   TEXT,
  creado      TEXT    NOT NULL,
  actualizado TEXT    NOT NULL,
  hd_tipo     TEXT,                      -- la foto original en HD está en KV con la llave  hd:<id>
  hd_bytes    INTEGER,
  token       TEXT                       -- permiso de un solo uso para subir la foto HD
);
