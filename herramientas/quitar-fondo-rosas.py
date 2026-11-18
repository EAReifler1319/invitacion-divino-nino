import sys, numpy as np
from PIL import Image
from scipy import ndimage as nd
im = Image.open(sys.argv[1]).convert('RGB')
a = np.asarray(im).astype(np.float32)
edge = np.concatenate([a[:8].reshape(-1,3), a[-8:].reshape(-1,3), a[:, :8].reshape(-1,3), a[:, -8:].reshape(-1,3)])
bg = np.median(edge, 0)
raw = np.max((bg - a) / np.maximum(bg, 1), axis=2).clip(0, 1)
mask = raw > 0.05
mask = nd.binary_closing(mask, iterations=3)
holes = nd.binary_fill_holes(mask) & ~mask
lab, k = nd.label(holes)
if k:
    sizes = nd.sum(holes, lab, range(1, k + 1))
    small = np.isin(lab, np.where(sizes < 6000)[0] + 1)
    mask |= small
solid = nd.gaussian_filter(nd.binary_erosion(mask, iterations=2).astype(np.float32), 1.5)
alpha = np.maximum(solid, np.clip(raw * 3, 0, 1))
alpha = np.where(mask | (raw > 0.03), alpha, 0)
A = np.maximum(alpha, 1e-3)[..., None]
un = np.clip((a - (1 - A) * bg) / A, 0, 255)
rgb = np.where(solid[..., None] > 0.99, a, un)
rgba = np.dstack([rgb, alpha * 255]).astype(np.uint8)
img = Image.fromarray(rgba, 'RGBA'); img = img.crop(img.getbbox())
W = int(sys.argv[4]) if len(sys.argv) > 4 else 800
img = img.resize((W, round(W * img.height / img.width)), Image.LANCZOS)
img.save(sys.argv[2], 'WEBP', quality=80, method=6)
bgc = Image.new('RGBA', img.size, (61, 90, 142, 255)); bgc.alpha_composite(img)
bgc.convert('RGB').resize((600, round(600*img.height/img.width))).save(sys.argv[3])
print(img.size)
