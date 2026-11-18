#!/bin/sh
# Crea compartir/Invitacion-Divino-Nino.html: la invitación en un solo archivo,
# con todas las imágenes adentro (para mandarla sin la carpeta img/).
# Uso (desde la carpeta INVITACION):  sh herramientas/armar-archivo-unico.sh
cd "$(dirname "$0")/.." || exit 1
B=$(base64 -w0 img/divino-nino.webp); R=$(base64 -w0 img/rosas.webp)
A1=$(base64 -w0 img/adorno1.webp);   A3=$(base64 -w0 img/adorno3.webp)
awk -v b="data:image/webp;base64,$B" -v r="data:image/webp;base64,$R" \
    -v a1="data:image/webp;base64,$A1" -v a3="data:image/webp;base64,$A3" '
  /<link rel="preload" as="image"/ { next }   # en el archivo único las imágenes ya van adentro
  {
    gsub(/src="img\/divino-nino.webp"/, "src=\"" b "\"")
    gsub(/url\(img\/rosas.webp\)/, "url(" r ")")
    gsub(/url\(img\/adorno1.webp\)/, "url(" a1 ")")
    gsub(/url\(img\/adorno3.webp\)/, "url(" a3 ")")
    print
  }' index.html > compartir/Invitacion-Divino-Nino.html
echo "Listo: compartir/Invitacion-Divino-Nino.html"
