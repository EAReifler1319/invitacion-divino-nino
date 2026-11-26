"""Crea img/compartir.jpg (1200x630): la imagen que sale cuando se comparte el link por WhatsApp.
Uso (desde la carpeta INVITACION):  python herramientas/portada-compartir.py"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1200, 630
F = 'C:/Windows/Fonts/'

# Fondo azul con resplandor (los mismos colores de la invitación)
y, x = np.mgrid[0:H, 0:W].astype(np.float32)
d = np.sqrt(((x - 860) / 700) ** 2 + ((y - 230) / 520) ** 2)
c1, c2, c3 = np.array([75, 106, 160]), np.array([61, 90, 142]), np.array([51, 77, 124])
t = np.clip(d, 0, 1)[..., None]
bg = np.where(t < .45, c1 + (c2 - c1) * (t / .45), c2 + (c3 - c2) * ((t - .45) / .55))
img = Image.fromarray(bg.astype(np.uint8), 'RGB').convert('RGBA')

# Halo de luz detrás del Niño
halo = Image.new('L', (W, H), 0)
ImageDraw.Draw(halo).ellipse((620, -40, 1100, 480), fill=200)
halo = halo.filter(ImageFilter.GaussianBlur(90))
img = Image.composite(Image.new('RGBA', (W, H), (238, 244, 255, 255)), img, halo)

# Rosas en dos esquinas
rosas = Image.open('img/rosas.webp').convert('RGBA')
r = rosas.resize((520, round(520 * rosas.height / rosas.width)), Image.LANCZOS)
for ang, pos in ((135, (-300, -280)), (-45, (W - 300, H - 250))):
    rr = r.rotate(ang, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(rr, (pos[0], pos[1]))

# El Niño
nino = Image.open('img/nino-jesus.webp').convert('RGBA')
nh = 600
n = nino.resize((round(nh * nino.width / nino.height), nh), Image.LANCZOS)
glow = Image.new('RGBA', n.size, (255, 255, 255, 0))
glow.putalpha(n.getchannel('A').filter(ImageFilter.GaussianBlur(14)).point(lambda v: v * .6))
nx = 860 - n.width // 2
img.alpha_composite(glow, (nx, 22))
img.alpha_composite(n, (nx, 22))

# Textos
dr = ImageDraw.Draw(img)
blanco, oro, rosa = (255, 250, 246), (249, 220, 146), (255, 227, 234)
cx = 368
def centro(txt, yy, font, fill, sp=0):
    w = dr.textlength(txt, font=font) + sp * (len(txt) - 1)
    xx = cx - w / 2
    for ch in txt:
        dr.text((xx + 2, yy + 3), ch, font=font, fill=(15, 25, 55, 110))
        dr.text((xx, yy), ch, font=font, fill=fill)
        xx += dr.textlength(ch, font=font) + sp
centro('GRAN FIESTA DEL', 150, ImageFont.truetype(F + 'georgia.ttf', 38), blanco, 7)
centro('NIÑO JESÚS', 205, ImageFont.truetype(F + 'georgia.ttf', 66), blanco, 3)
dr.line((cx - 210, 315, cx + 210, 315), fill=(233, 207, 143), width=2)
centro('24 DE DICIEMBRE', 338, ImageFont.truetype(F + 'georgiab.ttf', 36), oro, 4)
centro('6:00 P. M.', 390, ImageFont.truetype(F + 'georgia.ttf', 28), rosa, 5)
dr.line((cx - 210, 440, cx + 210, 440), fill=(233, 207, 143), width=2)
centro('Emily Lamar te invita', 462, ImageFont.truetype(F + 'Gabriola.ttf', 62), rosa)

img.convert('RGB').save('img/compartir.jpg', 'JPEG', quality=84, optimize=True, progressive=True)
print('Listo: img/compartir.jpg')
