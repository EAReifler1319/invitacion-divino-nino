# Invitación – Fiesta del Divino Niño

Link público: https://eareifler1319.github.io/invitacion-divino-nino/

## Carpetas

| Carpeta / archivo | Qué es |
|---|---|
| `index.html` | La invitación. Es la página que publica GitHub Pages. |
| `img/` | Imágenes que usa la invitación (Niño sin fondo, rosas, adornos). `compartir.jpg` es la foto que sale al mandar el link por WhatsApp. |
| `compartir/` | La invitación en **un solo archivo** con las imágenes adentro, para mandarla por WhatsApp o correo. |
| `herramientas/` | Scripts para quitar fondos, armar el archivo único y crear la foto para compartir. |
| `originales/` | Imágenes originales sin editar (solo en esta computadora, no se suben a GitHub). |

## Después de hacer cambios en `index.html`

1. Rearmar el archivo único: `sh herramientas/armar-archivo-unico.sh`
2. Si cambian la fecha o el texto de la portada: `python herramientas/portada-compartir.py`
3. Subir a GitHub: `git add -A && git commit -m "cambios" && git push`

## Datos que están en `index.html`

- WhatsApp de Emily: busca `const WHATSAPP=`.
- Fecha de la cuenta regresiva: busca `const FIESTA=` (hora de Quito).
