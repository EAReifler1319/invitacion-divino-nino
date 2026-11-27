-- Una fila por familia. Si la misma familia confirma otra vez, se actualiza (no se duplica).
CREATE TABLE IF NOT EXISTS confirmaciones (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  clave       TEXT    NOT NULL UNIQUE,   -- nombre normalizado (para no duplicar)
  familia     TEXT    NOT NULL,          -- como lo escribieron
  personas    INTEGER NOT NULL,
  foto        BLOB,                      -- JPEG ya achicado en el celular (~300 KB)
  foto_tipo   TEXT,
  creado      TEXT    NOT NULL,
  actualizado TEXT    NOT NULL
);
