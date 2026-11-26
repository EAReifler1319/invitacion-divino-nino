"""Quita el fondo negro de la foto del Niño Jesús.
- El halo y el resplandor se vuelven luz semitransparente (sin bordes duros).
- La cabeza, el cuerpo, la capa y los pies quedan sólidos (no se transparentan sobre las nubes).
Uso (desde la carpeta INVITACION):
  python herramientas/quitar-fondo-nino-jesus.py originales/nino-jesus-original.jpg img/nino-jesus.webp"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage as nd

src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert('RGB')
a = np.asarray(im).astype(np.float32)
H, W = a.shape[:2]
mx = a.max(2)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)

# 1) Luz: todo lo que es luz sobre negro se des-mezcla (halo y resplandor quedan como brillo)
luz = np.clip((mx - 34) / 221, 0, 1) ** 1.5

# 2) Cabeza (cara + pelo): sólida, con borde suave
cabeza = ((((xx - 357) / 128) ** 2 + ((yy - 262) / 118) ** 2) < 1) | ((((xx - 352) / 62) ** 2 + ((yy - 392) / 26) ** 2) < 1)  # + cuello

# 3) Cuerpo, capa, brazos y pies (de los hombros hacia abajo): zonas claras + sus pliegues oscuros
# (de y=375 hacia abajo; más arriba solo las manos, a los lados, para no tomar el resplandor)
manos = (yy >= 300) & (yy < 420) & ((xx < 178) | (xx > 540)) & (mx > 130) & (a[..., 2] > 115)   # piel (el resplandor amarillo casi no tiene azul)
manos = nd.binary_fill_holes(nd.binary_closing(manos, iterations=2))
claro = ((mx > 85) & (yy >= 412)) | ((mx > 165) & (yy >= 388)) | manos
claro = nd.binary_closing(claro, iterations=3)
cuerpo = nd.binary_fill_holes(claro)
lab, k = nd.label(cuerpo)
if k:
    tam = nd.sum(cuerpo, lab, range(1, k + 1))
    cuerpo = lab == (1 + int(np.argmax(tam)))
# La paja de abajo: solo las hebras claras quedan sólidas (los huecos entre hebras se ven a través)
paja = yy > 778
cuerpo = (cuerpo & ~paja) | ((mx > 120) & paja)
cuerpo = nd.binary_opening(cuerpo, iterations=1)
cuerpo |= manos   # dedos de las manos levantadas

# Halo: los rayos dorados más brillantes quedan sólidos; lo de alrededor sigue siendo luz
dh = ((xx - 357) / 190) ** 2 + ((yy - 238) / 172) ** 2
halo = (dh < 1) & (mx > 228)
halo = nd.binary_opening(halo, iterations=1)
solido = np.clip(nd.gaussian_filter((cabeza | cuerpo | halo).astype(np.float32), 1.3) * 1.15, 0, 1)
alpha = np.maximum(luz, solido)

# 4) Colores: donde es luz, se quita el negro mezclado; donde es sólido, el color original
A = np.clip(alpha, 1e-3, 1)[..., None]
rgb = np.where(solido[..., None] > .5, a, np.clip(a / A, 0, 255))

rgba = np.dstack([rgb, alpha * 255]).astype(np.uint8)
Image.fromarray(rgba, 'RGBA').save(out, 'WEBP', quality=76, method=6, alpha_quality=70)
print('Listo:', out, rgba.shape)
