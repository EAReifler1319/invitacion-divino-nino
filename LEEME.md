# Invitación – Fiesta del Divino Niño

Link público: https://eareifler1319.github.io/invitacion-divino-nino/

## Carpetas

| Carpeta / archivo | Qué es |
|---|---|
| `index.html` | La invitación. Es la página que publica GitHub Pages. |
| `img/` | Imágenes que usa la invitación (Niño sin fondo, rosas, adornos). |
| `compartir/` | La invitación en **un solo archivo** con las imágenes adentro, para mandarla por WhatsApp o correo. |
| `herramientas/` | Scripts para quitar fondos y armar el archivo único. |
| `originales/` | Imágenes originales sin editar (solo en esta computadora, no se suben a GitHub). |

## Después de hacer cambios en `index.html`

1. Rearmar el archivo único: `sh herramientas/armar-archivo-unico.sh`
2. Subir a GitHub: `git add -A && git commit -m "cambios" && git push`

## Pendiente

- Poner el número de WhatsApp de Emily en `index.html` (busca `const WHATSAPP=''`).
