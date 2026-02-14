from PIL import Image
import os

BASE = os.path.dirname(os.path.dirname(__file__))
ASSETS = os.path.join(BASE, 'assets')

candidates = [
    os.path.join(ASSETS, 'icon.png'),
    os.path.join(ASSETS, 'icon.ico'),
    os.path.join(ASSETS, 'icon.icns'),
]

src = None
for p in candidates:
    if os.path.exists(p):
        src = p
        break

if not src:
    print('No se encontró fuente de icono en assets (icon.png|icon.ico|icon.icns)')
    raise SystemExit(1)

out_ico = os.path.join(ASSETS, 'app.ico')
print(f'Usando {src} -> generando {out_ico}')

img = Image.open(src)
if img.mode not in ('RGBA', 'RGB'):
    img = img.convert('RGBA')

sizes = [(256,256),(128,128),(64,64),(48,48),(32,32),(16,16)]
# Pillow will create multi-size ICO when passing sizes
img.save(out_ico, format='ICO', sizes=sizes)
print('Generado:', out_ico)
