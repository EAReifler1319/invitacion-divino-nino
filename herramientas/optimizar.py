"""Ajustes de rendimiento en index.html (se ejecutó una vez; se guarda como referencia)."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
s = open(p, encoding='utf-8').read()

def rep(a, b):
    global s
    assert s.count(a) == 1, a[:80]
    s = s.replace(a, b)

# 1) Precargar las imágenes de la portada con prioridad alta
#    y cargar las letras de Google sin bloquear la página (solo los grosores usados).
rep('<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Great+Vibes&display=swap" rel="stylesheet">',
    '<link rel="preload" as="image" href="img/divino-nino.webp" type="image/webp" fetchpriority="high">\n'
    '<link rel="preload" as="image" href="img/rosas.webp" type="image/webp">\n'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Great+Vibes&display=swap" media="print" onload="this.media=\'all\'">\n'
    '<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Great+Vibes&display=swap"></noscript>')

# 2) Imagen del Niño: prioridad alta y tamaño conocido (evita saltos al cargar)
rep('<img src="img/divino-nino.webp" alt="Imagen del Divino Niño con los brazos abiertos">',
    '<img src="img/divino-nino.webp" width="720" height="964" fetchpriority="high" decoding="async" alt="Imagen del Divino Niño con los brazos abiertos">')

# 3) Adornos en WebP (la mitad de peso)
rep('--m:url(img/adorno1.png)', '--m:url(img/adorno1.webp)')
rep('--m:url(img/adorno3.png)', '--m:url(img/adorno3.webp)')

# 4) Proporción de las rosas con su nuevo tamaño
rep('aspect-ratio:1000/601;background:url(img/rosas.webp)', 'aspect-ratio:800/481;background:url(img/rosas.webp)')

# 5) Las tarjetas de abajo no se dibujan hasta que se acercan a la pantalla
rep('.aparecer{opacity:0;', '.card{content-visibility:auto;contain-intrinsic-size:auto 600px}\n.aparecer{opacity:0;')

open(p, 'w', encoding='utf-8').write(s)
print('ok')
