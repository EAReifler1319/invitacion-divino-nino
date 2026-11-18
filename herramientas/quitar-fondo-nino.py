import sys, numpy as np
from PIL import Image
from scipy import ndimage as nd
src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert('RGB')
W = int(sys.argv[3]) if len(sys.argv) > 3 else 720
im = im.resize((W, round(W*im.height/im.width)), Image.LANCZOS)
a = np.asarray(im).astype(np.float32)
mn, mx = a.min(2), a.max(2)
blanco = (mn > 228) & ((mx - mn) < 18)
lab, k = nd.label(blanco)
borde = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
areas = nd.sum(blanco, lab, range(1, k + 1))
quitar = np.zeros_like(blanco)
for i, ar in enumerate(areas, 1):
    ys = np.where(lab == i)[0]
    if i in borde or (ar > 120 and ys.max() < 0.30 * lab.shape[0]):
        quitar |= lab == i
# alpha suave en la orilla
cerca = nd.binary_dilation(quitar, iterations=3) & ~quitar
alpha = np.ones(mn.shape, np.float32)
alpha[quitar] = 0
blancura = np.clip((255 - mn) / 45, 0, 1)  # 0 = blanco puro
alpha[cerca] = np.minimum(1, blancura[cerca] * 1.2)
alpha = nd.gaussian_filter(alpha, 0.7)
alpha[quitar & (nd.binary_erosion(quitar, iterations=2))] = 0
# quitar halo blanco: des-mezclar con blanco
A = np.clip(alpha, 1e-3, 1)[..., None]
rgb = np.clip((a - (1 - A) * 255) / A, 0, 255)
rgba = np.dstack([rgb, alpha * 255]).astype(np.uint8)
Image.fromarray(rgba, 'RGBA').save(out, 'WEBP', quality=int(sys.argv[4]) if len(sys.argv) > 4 else 80, method=6)
print(rgba.shape)
