# Invitación – Gran Fiesta del Niño Jesús

- Invitación (para enviar): https://eareifler1319.github.io/invitacion-nino-jesus/
- Confirmaciones de Emily (con clave): https://eareifler1319.github.io/invitacion-nino-jesus/confirmaciones.html

## Cómo funciona

1. El invitado llena los 3 pasos y toca **Confirmar mi asistencia**.
2. Se guardan en **Cloudflare** (carpeta `servidor/`): el nombre, el número de personas, una miniatura (base de datos D1) y la **foto original en HD**, hasta 25 MB (almacenamiento KV). El invitado ve el avance de la subida.
3. Emily entra a `confirmaciones.html` con su clave y ve las familias, las fotos y los totales. La lista usa miniaturas (carga rápido); ver en grande, descargar una o todas en .zip baja la foto original en HD. También puede borrar confirmaciones.

Si una familia confirma otra vez con el mismo nombre, se **actualiza** (no se duplica).

## Carpetas

| Carpeta / archivo | Qué es |
|---|---|
| `index.html` | La invitación. Es la página que publica GitHub Pages. |
| `confirmaciones.html` | Página privada de Emily (pide clave). |
| `img/` | Imágenes que usa la invitación (Niño Jesús sin fondo, rosas, adornos). `compartir.jpg` es la foto que sale al mandar el link por WhatsApp. |
| `compartir/` | La invitación en **un solo archivo** con las imágenes adentro. También guarda las confirmaciones en el servidor. |
| `servidor/` | El servidor en Cloudflare (Worker + base de datos D1) que guarda las confirmaciones. |
| `herramientas/` | Scripts para quitar fondos, armar el archivo único y crear la foto para compartir. |
| `originales/` | Imágenes originales sin editar (solo en esta computadora, no se suben a GitHub). |

## Después de hacer cambios en `index.html`

1. Rearmar el archivo único: `sh herramientas/armar-archivo-unico.sh`
2. Si cambian la fecha o el texto de la portada: `python herramientas/portada-compartir.py`
3. Subir a GitHub: `git add -A && git commit -m "cambios" && git push`

## Servidor (carpeta `servidor/`)

- Dirección: https://invitacion-nino-jesus.invitacion-nino-jesus-servidor.workers.dev
- Base de datos D1: `invitacion-confirmaciones` (datos + miniaturas)
- Almacenamiento KV: `FOTOS` (fotos originales en HD, llave `hd:<id>`)
- Publicar cambios del servidor: `cd servidor` y luego `npx wrangler deploy`
- Cambiar la clave de Emily: `cd servidor` y luego `npx wrangler secret put ADMIN_KEY` (la clave **no** está en el código ni en GitHub)
- Probar en la computadora: `cd servidor`, `npx wrangler dev --local` y abrir la invitación con `?api=http://127.0.0.1:8787` al final del link (la clave local va en `servidor/.dev.vars`)

## Datos que están en `index.html`

- Dirección del servidor: busca `const API=` (también en `confirmaciones.html`).
- Fecha de la cuenta regresiva: busca `const FIESTA=` (hora de Quito).
