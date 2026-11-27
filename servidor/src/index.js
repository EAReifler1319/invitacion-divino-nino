// Servidor de la invitación (Cloudflare Worker + base de datos D1 + almacenamiento KV para fotos HD).
//
//   POST   /api/confirmar          (público)  familia, personas, mini   -> guarda o actualiza; devuelve id + token
//   PUT    /api/foto-hd/:id        (público, con el token de arriba)   -> la foto original en HD (cuerpo = la imagen)
//   GET    /api/lista              (Emily)    lista sin fotos + totales
//   GET    /api/foto/:id           (Emily)    miniatura (para ver la lista rápido)
//   GET    /api/foto-hd/:id        (Emily)    foto original en HD (para descargar)
//   DELETE /api/confirmacion/:id   (Emily)    borra una confirmación y sus fotos
//
// "Emily" = enviar el encabezado  Authorization: Bearer <ADMIN_KEY>
//
// Por qué dos pasos: la base de datos D1 solo acepta filas de ~2 MB, así que ahí va la miniatura;
// la foto HD (hasta 25 MB) va a KV y se sube como flujo directo, sin pasar por la memoria del servidor.

const MAX_MINI = 1_500_000;
const MAX_HD = 25 * 1024 * 1024 - 1024; // límite de un valor en KV
const TIPOS = ['image/jpeg', 'image/png', 'image/webp', 'image/heic', 'image/heif'];

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Authorization, Content-Type, X-Token',
  'Access-Control-Max-Age': '86400',
};

const json = (data, status = 200) =>
  new Response(JSON.stringify(data), { status, headers: { 'Content-Type': 'application/json; charset=utf-8', ...CORS } });

// "  Familia  LAMAR álvaro " -> "lamar alvaro"
function normalizar(s) {
  return s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase()
    .replace(/^\s*(la\s+)?familia\s+/, '').replace(/\s+/g, ' ').trim();
}

// Compara sin filtrar cuánto se parecen (tiempo constante)
function iguales(a, b) {
  a = String(a || ''); b = String(b || '');
  if (!a || !b || a.length !== b.length) return false;
  let d = 0;
  for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return d === 0;
}
const claveOk = (req, env) => iguales((req.headers.get('Authorization') || '').replace(/^Bearer\s+/i, ''), env.ADMIN_KEY);

async function confirmar(req, env) {
  let form;
  try { form = await req.formData(); } catch { return json({ error: 'Datos inválidos' }, 400); }
  if (form.get('web')) return json({ ok: true }); // casilla trampa para robots

  const familia = String(form.get('familia') || '').replace(/\s+/g, ' ').trim().slice(0, 60);
  const personas = parseInt(form.get('personas'), 10);
  const mini = form.get('mini') || form.get('foto');
  const clave = normalizar(familia);

  if (!clave) return json({ error: 'Falta el nombre de la familia' }, 400);
  if (!(personas >= 1 && personas <= 30)) return json({ error: 'Número de personas inválido' }, 400);
  if (!mini || typeof mini === 'string') return json({ error: 'Falta la foto' }, 400);
  if (!TIPOS.includes(mini.type)) return json({ error: 'La foto debe ser JPG, PNG o WEBP' }, 400);
  if (mini.size > MAX_MINI) return json({ error: 'La foto es muy pesada' }, 413);

  const ahora = new Date().toISOString();
  const token = crypto.randomUUID();
  const row = await env.DB.prepare(
    `INSERT INTO confirmaciones (clave, familia, personas, foto, foto_tipo, creado, actualizado, token)
     VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?6, ?7)
     ON CONFLICT(clave) DO UPDATE SET
       familia = excluded.familia, personas = excluded.personas,
       foto = excluded.foto, foto_tipo = excluded.foto_tipo, actualizado = excluded.actualizado,
       token = excluded.token
     RETURNING id`
  ).bind(clave, familia, personas, await mini.arrayBuffer(), mini.type, ahora, token).first();

  return json({ ok: true, id: row.id, token });
}

// La foto HD llega como cuerpo de la petición y se guarda directo en KV (sin cargarla entera en memoria)
async function subirHD(req, env, id) {
  const r = await env.DB.prepare('SELECT token FROM confirmaciones WHERE id = ?1').bind(id).first();
  if (!r || !iguales(req.headers.get('X-Token'), r.token)) return json({ error: 'Permiso inválido' }, 403);
  const tipo = (req.headers.get('Content-Type') || '').split(';')[0].trim();
  const largo = parseInt(req.headers.get('Content-Length') || '0', 10);
  if (!TIPOS.includes(tipo)) return json({ error: 'La foto debe ser JPG, PNG o WEBP' }, 400);
  if (!(largo > 0)) return json({ error: 'Falta la foto' }, 411);
  if (largo > MAX_HD) return json({ error: 'La foto pesa más de 25 MB' }, 413);

  await env.FOTOS.put('hd:' + id, req.body, { metadata: { tipo, bytes: largo } });
  await env.DB.prepare('UPDATE confirmaciones SET hd_tipo = ?1, hd_bytes = ?2, token = NULL WHERE id = ?3')
    .bind(tipo, largo, id).run();
  return json({ ok: true });
}

async function lista(env) {
  const { results } = await env.DB.prepare(
    `SELECT id, familia, personas, creado, actualizado, hd_tipo, hd_bytes
     FROM confirmaciones ORDER BY creado`
  ).all();
  const personas = results.reduce((t, r) => t + r.personas, 0);
  return json({ familias: results.length, personas, regalos: personas, confirmaciones: results });
}

async function verMini(env, id) {
  const r = await env.DB.prepare('SELECT foto, foto_tipo FROM confirmaciones WHERE id = ?1').bind(id).first();
  if (!r || !r.foto) return json({ error: 'No hay foto' }, 404);
  const bytes = r.foto instanceof ArrayBuffer ? r.foto : new Uint8Array(r.foto);
  return new Response(bytes, { headers: { 'Content-Type': r.foto_tipo || 'image/jpeg', 'Cache-Control': 'private, max-age=3600', ...CORS } });
}

async function verHD(env, id) {
  const { value, metadata } = await env.FOTOS.getWithMetadata('hd:' + id, { type: 'stream' });
  if (!value) return verMini(env, id); // si la HD no llegó a subirse, al menos la miniatura
  return new Response(value, {
    headers: { 'Content-Type': (metadata && metadata.tipo) || 'image/jpeg', 'Cache-Control': 'private, max-age=3600', ...CORS },
  });
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    const ruta = url.pathname.replace(/\/+$/, '');

    if (req.method === 'OPTIONS') return new Response(null, { status: 204, headers: CORS });

    try {
      if (ruta === '/api/confirmar' && req.method === 'POST') return await confirmar(req, env);
      let m = ruta.match(/^\/api\/foto-hd\/(\d+)$/);
      if (m && req.method === 'PUT') return await subirHD(req, env, Number(m[1]));

      if (ruta.startsWith('/api/')) {
        if (!claveOk(req, env)) return json({ error: 'Clave incorrecta' }, 401);
        if (ruta === '/api/lista' && req.method === 'GET') return await lista(env);
        if (m && req.method === 'GET') return await verHD(env, Number(m[1]));
        m = ruta.match(/^\/api\/foto\/(\d+)$/);
        if (m && req.method === 'GET') return await verMini(env, Number(m[1]));
        m = ruta.match(/^\/api\/confirmacion\/(\d+)$/);
        if (m && req.method === 'DELETE') {
          const id = Number(m[1]);
          await env.DB.prepare('DELETE FROM confirmaciones WHERE id = ?1').bind(id).run();
          await env.FOTOS.delete('hd:' + id);
          return json({ ok: true });
        }
      }
      return json({ error: 'No encontrado' }, 404);
    } catch (e) {
      return json({ error: 'Error del servidor' }, 500);
    }
  },
};
