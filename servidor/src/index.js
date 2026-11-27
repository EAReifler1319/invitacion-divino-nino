// Servidor de la invitación (Cloudflare Worker + base de datos D1).
//
//   POST   /api/confirmar          (público)  familia, personas, foto  -> guarda o actualiza
//   GET    /api/lista              (Emily)    lista sin fotos + totales
//   GET    /api/foto/:id           (Emily)    la foto de una familia
//   DELETE /api/confirmacion/:id   (Emily)    borra una confirmación (por ejemplo, las de prueba)
//
// "Emily" = enviar el encabezado  Authorization: Bearer <ADMIN_KEY>

const MAX_FOTO = 1_800_000; // bytes (D1 acepta filas de hasta ~2 MB; el celular la manda ~300 KB)
const TIPOS = ['image/jpeg', 'image/png', 'image/webp'];

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Authorization, Content-Type',
  'Access-Control-Max-Age': '86400',
};

const json = (data, status = 200) =>
  new Response(JSON.stringify(data), { status, headers: { 'Content-Type': 'application/json; charset=utf-8', ...CORS } });

// "  Familia  LAMAR álvaro " -> "lamar alvaro"
function normalizar(s) {
  return s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase()
    .replace(/^\s*(la\s+)?familia\s+/, '').replace(/\s+/g, ' ').trim();
}

// Compara la clave sin filtrar cuánto se parece (tiempo constante)
function claveOk(req, env) {
  const dada = (req.headers.get('Authorization') || '').replace(/^Bearer\s+/i, '');
  const real = env.ADMIN_KEY || '';
  if (!real || dada.length !== real.length) return false;
  let d = 0;
  for (let i = 0; i < real.length; i++) d |= dada.charCodeAt(i) ^ real.charCodeAt(i);
  return d === 0;
}

async function confirmar(req, env) {
  let form;
  try { form = await req.formData(); } catch { return json({ error: 'Datos inválidos' }, 400); }
  if (form.get('web')) return json({ ok: true }); // casilla trampa para robots

  const familia = String(form.get('familia') || '').replace(/\s+/g, ' ').trim().slice(0, 60);
  const personas = parseInt(form.get('personas'), 10);
  const foto = form.get('foto');
  const clave = normalizar(familia);

  if (!clave) return json({ error: 'Falta el nombre de la familia' }, 400);
  if (!(personas >= 1 && personas <= 30)) return json({ error: 'Número de personas inválido' }, 400);
  if (!foto || typeof foto === 'string') return json({ error: 'Falta la foto' }, 400);
  if (!TIPOS.includes(foto.type)) return json({ error: 'La foto debe ser JPG, PNG o WEBP' }, 400);
  if (foto.size > MAX_FOTO) return json({ error: 'La foto es muy pesada' }, 413);

  const ahora = new Date().toISOString();
  const bytes = await foto.arrayBuffer();
  await env.DB.prepare(
    `INSERT INTO confirmaciones (clave, familia, personas, foto, foto_tipo, creado, actualizado)
     VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?6)
     ON CONFLICT(clave) DO UPDATE SET
       familia = excluded.familia, personas = excluded.personas,
       foto = excluded.foto, foto_tipo = excluded.foto_tipo, actualizado = excluded.actualizado`
  ).bind(clave, familia, personas, bytes, foto.type, ahora).run();

  return json({ ok: true });
}

async function lista(env) {
  const { results } = await env.DB.prepare(
    'SELECT id, familia, personas, creado, actualizado, foto IS NOT NULL AS tiene_foto FROM confirmaciones ORDER BY creado'
  ).all();
  const personas = results.reduce((t, r) => t + r.personas, 0);
  return json({ familias: results.length, personas, regalos: personas, confirmaciones: results });
}

async function verFoto(env, id) {
  const r = await env.DB.prepare('SELECT foto, foto_tipo, familia FROM confirmaciones WHERE id = ?1').bind(id).first();
  if (!r || !r.foto) return json({ error: 'No hay foto' }, 404);
  const bytes = r.foto instanceof ArrayBuffer ? r.foto : new Uint8Array(r.foto);
  return new Response(bytes, { headers: { 'Content-Type': r.foto_tipo || 'image/jpeg', 'Cache-Control': 'private, max-age=3600', ...CORS } });
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    const ruta = url.pathname.replace(/\/+$/, '');

    if (req.method === 'OPTIONS') return new Response(null, { status: 204, headers: CORS });

    try {
      if (ruta === '/api/confirmar' && req.method === 'POST') return await confirmar(req, env);

      if (ruta.startsWith('/api/')) {
        if (!claveOk(req, env)) return json({ error: 'Clave incorrecta' }, 401);
        if (ruta === '/api/lista' && req.method === 'GET') return await lista(env);
        let m = ruta.match(/^\/api\/foto\/(\d+)$/);
        if (m && req.method === 'GET') return await verFoto(env, Number(m[1]));
        m = ruta.match(/^\/api\/confirmacion\/(\d+)$/);
        if (m && req.method === 'DELETE') {
          await env.DB.prepare('DELETE FROM confirmaciones WHERE id = ?1').bind(Number(m[1])).run();
          return json({ ok: true });
        }
      }
      return json({ error: 'No encontrado' }, 404);
    } catch (e) {
      return json({ error: 'Error del servidor' }, 500);
    }
  },
};
