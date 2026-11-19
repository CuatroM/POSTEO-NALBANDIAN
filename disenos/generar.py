"""
Arma las historias de Alexis Nalbandian como HTML (estilo fijo en historia.css) y las pasa a JPG 1080x1920.

Uso: python3 disenos/generar.py disenos/posteos/historia-robots.py
     -> disenos/salida/<ID>/placa-N.html y NN.jpg
     -> si el archivo define CARPETA, copia los JPG a posts/<CARPETA>/ listos para publicar.

Regla de precio (todas las piezas con envío gratis, salvo que se cambie):
  precio = costo BaseLinker + 35 % + envío, con envío = 10 % del costo (mínimo $20.000).
"""
import csv
import html
import importlib.util
import shutil
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
PRODUCTOS = AQUI / "productos"
BASE = RAIZ / "datos" / "productos_fema.csv"


def e(t):
    return html.escape(str(t))


# ---------- Precios ----------
def precio_envio_gratis(costo, margen=0.35, envio_pct=0.10, envio_min=20000):
    costo = float(costo)
    return round(costo * (1 + margen) + max(costo * envio_pct, envio_min))


def pesos(n):
    return "$" + f"{int(round(n)):,}".replace(",", ".")


# ---------- Base de productos (SINCRO PRODUCTOS FEMA BASE) ----------
def base():
    if not BASE.exists():
        return {}
    with BASE.open(encoding="utf-8-sig") as fh:
        return {f["sku"]: f for f in csv.DictReader(fh, delimiter=";")}


def foto(sku):
    for n in (sku, sku.split("#")[0]):
        for ext in ("png", "jpg", "jpeg", "webp"):
            p = PRODUCTOS / f"{n}.{ext}"
            if p.exists():
                return f"../../productos/{p.name}"
    return None


# ---------- Piezas ----------
ICONOS = {
    "cortacesped": '<path d="M14 66h72l-8-24H30Z" fill="#111"/><circle cx="30" cy="72" r="10" fill="#FF6B00"/><circle cx="72" cy="72" r="10" fill="#FF6B00"/><path d="M40 42l6-12h18l4 12" fill="none" stroke="#111" stroke-width="6"/><path d="M6 92l6-10 6 10 6-10 6 10 6-10 6 10 6-10 6 10 6-10 6 10 6-10 6 10 6-10 6 10" fill="none" stroke="#FF6B00" stroke-width="5"/>',
    "aspiradora": '<circle cx="50" cy="50" r="40" fill="#111"/><circle cx="50" cy="50" r="28" fill="none" stroke="#fff" stroke-width="4"/><circle cx="50" cy="30" r="7" fill="#FF6B00"/><path d="M14 66a40 40 0 0 0 72 0" fill="none" stroke="#FF6B00" stroke-width="7"/>',
    "pileta": '<rect x="22" y="18" width="56" height="44" rx="10" fill="#111"/><rect x="32" y="28" width="36" height="10" rx="5" fill="#FF6B00"/><path d="M6 76q11-10 22 0t22 0 22 0 22 0" fill="none" stroke="#FF6B00" stroke-width="6"/><path d="M6 92q11-10 22 0t22 0 22 0 22 0" fill="none" stroke="#111" stroke-width="6"/>',
    "whatsapp": '<path d="M50 6a43 43 0 0 0-37 65L6 94l24-6A43 43 0 1 0 50 6Z" fill="#FF6B00"/><path d="M36 30c-3 0-7 4-7 10 0 12 16 30 32 30 6 0 10-4 10-7l-1-4-10-5-5 5c-6-2-12-8-14-14l5-5-5-10Z" fill="#fff"/>',
}


def svg(nombre):
    return f'<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">{ICONOS[nombre]}</svg>'


def iconos(items):
    return '<div class="iconos">' + "".join(
        f'<div class="icono"><div class="circulo">{svg(i)}</div><span>{t}</span></div>' for i, t in items) + "</div>"


def tarjeta(p):
    """p: dict con sku, nombre, detalle (opcional), costo (o precio fijo)."""
    img = foto(p["sku"])
    precio = p.get("precio") or precio_envio_gratis(p["costo"])
    return (f'<div class="producto"><div class="foto">{f"<img src={chr(34)}{img}{chr(34)}>" if img else "<div class=pendiente>FOTO<br>PENDIENTE</div>"}</div>'
            f'<div class="datos"><div class="nombre">{p["nombre"]}</div>'
            + (f'<div class="detalle">{p["detalle"]}</div>' if p.get("detalle") else "")
            + f'<div class="precio">{pesos(precio)}</div><div class="envio">ENVÍO GRATIS</div></div></div>')


def productos(lista):
    return f'<div class="productos{" uno" if len(lista) == 1 else ""}">' + "".join(tarjeta(p) for p in lista) + "</div>"


import random


def graffiti(semilla=1):
    """Marcas de spray en gris claro: trazos difuminados, chorreaduras y salpicaduras en los bordes."""
    r = random.Random(semilla)
    g = ['<svg class="graffiti" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">'
         '<defs><filter id="spray" x="-20%" y="-20%" width="140%" height="140%">'
         '<feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" result="r"/>'
         '<feDisplacementMap in="SourceGraphic" in2="r" scale="14"/><feGaussianBlur stdDeviation="2.2"/></filter>'
         '<filter id="niebla"><feGaussianBlur stdDeviation="18"/></filter></defs>']
    # zonas: esquinas y bordes, lejos del centro del texto
    zonas = [(80, 330, 1000, 520), (40, 1150, 520, 1700), (640, 1380, 1060, 1760), (700, 120, 1060, 360)]
    for k, (x0, y0, x1, y1) in enumerate(r.sample(zonas, 3)):
        cx, cy = r.uniform(x0, x1), r.uniform(y0, y1)
        g.append(f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{r.uniform(120, 220):.0f}" ry="{r.uniform(50, 110):.0f}" '
                 f'fill="#D9D9D9" opacity=".35" filter="url(#niebla)"/>')
        # trazo tipo tag
        pts = [(cx + r.uniform(-260, 260), cy + r.uniform(-90, 90)) for _ in range(4)]
        d = f"M{pts[0][0]:.0f} {pts[0][1]:.0f} C" + " ".join(f"{x:.0f} {y:.0f}" for x, y in pts[1:])
        g.append(f'<path d="{d}" fill="none" stroke="#CFCFCF" stroke-width="{r.uniform(22, 38):.0f}" '
                 f'stroke-linecap="round" opacity=".45" filter="url(#spray)"/>')
        # chorreaduras
        for _ in range(r.randint(2, 4)):
            x = r.uniform(min(p[0] for p in pts), max(p[0] for p in pts))
            y = cy + r.uniform(-20, 40)
            largo = r.uniform(60, 180)
            g.append(f'<path d="M{x:.0f} {y:.0f} v{largo:.0f}" stroke="#CFCFCF" stroke-width="{r.uniform(5, 9):.0f}" '
                     f'stroke-linecap="round" opacity=".45"/><circle cx="{x:.0f}" cy="{y + largo:.0f}" r="7" fill="#CFCFCF" opacity=".45"/>')
        # salpicaduras
        for _ in range(r.randint(25, 45)):
            g.append(f'<circle cx="{cx + r.gauss(0, 150):.0f}" cy="{cy + r.gauss(0, 90):.0f}" '
                     f'r="{r.uniform(1.5, 6):.1f}" fill="#C8C8C8" opacity="{r.uniform(.25, .55):.2f}"/>')
    g.append("</svg>")
    return "".join(g)


def marco(cuerpo, pie="", fondo="", rubro="Robots FEMA", semilla=1):
    pie_html = f'<div class="pie-h"><i></i><span>{pie}</span></div>' if pie else ""
    return f'''<!doctype html><html><head><meta charset="utf-8"><meta name="tamano" content="1080x1920">
<link rel="stylesheet" href="../../historia.css"></head>
<body><div class="historia {fondo}">
{graffiti(semilla)}
<div class="marca-h"><div class="nombre">ALEXIS <b>NALBANDIAN</b></div><div class="rubro">{e(rubro)}</div></div>
<div class="cuerpo">{cuerpo}</div>
{pie_html}
</div></body></html>'''


# ---------- Render ----------
def render(carpeta):
    from playwright.sync_api import sync_playwright
    salidas = []
    with sync_playwright() as pw:
        try:
            nav = pw.chromium.launch()
        except Exception:  # noqa: BLE001
            nav = pw.chromium.launch(executable_path="/usr/bin/google-chrome")
        pag = nav.new_page(viewport={"width": 1080, "height": 1920})
        for f in sorted(carpeta.glob("placa-*.html"), key=lambda x: int(x.stem.split("-")[1])):
            pag.goto(f.as_uri())
            pag.evaluate("document.fonts.ready")
            pag.wait_for_timeout(200)
            out = carpeta / f"{int(f.stem.split('-')[1]):02d}.jpg"
            pag.screenshot(path=str(out), type="jpeg", quality=92)
            salidas.append(out)
        nav.close()
    return salidas


def generar(modulo):
    spec = importlib.util.spec_from_file_location("pieza", modulo)
    pieza = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pieza)
    salida = AQUI / "salida" / pieza.ID
    if salida.exists():
        shutil.rmtree(salida)
    salida.mkdir(parents=True)
    for i, pagina in enumerate(pieza.placas(sys.modules[__name__]), 1):
        (salida / f"placa-{i}.html").write_text(pagina, encoding="utf-8")
    jpgs = render(salida)
    destino = getattr(pieza, "CARPETA", "")
    if destino:
        d = RAIZ / "posts" / destino
        d.mkdir(parents=True, exist_ok=True)
        for j in jpgs:
            shutil.copy(j, d / j.name)
        print(f"Copiadas {len(jpgs)} historias a posts/{destino}")
    print(salida)


if __name__ == "__main__":
    generar(sys.argv[1])
