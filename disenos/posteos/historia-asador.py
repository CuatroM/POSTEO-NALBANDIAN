"""Historias — Asador y parrilla FEMA: solo placas de producto (una por producto).
Productos: SINCRO PRODUCTOS FEMA BASE (datos/productos_fema.csv), solo con stock y con foto.
Precio = costo BaseLinker + 35 % + envío (10 % del costo, mín. $20.000): todas con envío gratis.
"""
ID = "historias-asador"
CARPETA = ""  # se completa al aprobar

RUBRO = "Parrilla FEMA"
ENVIO = "ENVÍO GRATIS POR TRANSPORTE CREDIFIN"

# (sku, título de la placa, bajada, nombre comercial, detalle)
PLACAS = [
    ("69606789#FEMA", "Kit<br><em>asador</em>", "Lo justo para manejar el fuego.",
     "Kit asador FEMA 3 piezas", "Tenedor 35&nbsp;cm, paleta 35&nbsp;cm y pinza 30&nbsp;cm"),
    ("69606790#FEMA", "Kit<br><em>asador XL</em>", "Más largo, más lejos del calor.",
     "Kit asador FEMA 3 piezas XL", "Tenedor 39&nbsp;cm, paleta 40&nbsp;cm y pinza 42&nbsp;cm"),
    ("69606792#FEMA", "Kit asador<br><em>con estuche</em>", "Listo para llevar a cualquier asado.",
     "Kit asador FEMA con estuche", "Tenedor 33&nbsp;cm, cuchillo 33&nbsp;cm y pinza 35&nbsp;cm"),
    ("69606799#FEMA", "Guante<br><em>alta temperatura</em>", "Manos protegidas frente a la parrilla.",
     "Guante siliconado FEMA", "Resiste hasta 800&nbsp;°C"),
    ("69606797#FEMA", "Cepillo<br><em>limpia parrilla</em>", "La parrilla impecable para el próximo asado.",
     "Cepillo de acero FEMA", "12 x 10 x 6&nbsp;cm"),
    ("69606775#FEMA", "Botella<br><em>térmica</em>", "Frío o caliente, todo el día.",
     "Botella térmica FEMA 500&nbsp;ml", "Acero inoxidable"),
]

COSTOS_MANUALES = {}


def producto(g, sku, nombre, detalle):
    b = g.base().get(sku)
    costo = COSTOS_MANUALES.get(sku) or (b and b["costo"])
    if b and float(b["stock"] or 0) <= 0:
        print(f"  ATENCIÓN {sku}: sin stock en la base")
    if not g.foto(sku):
        print(f"  ATENCIÓN {sku}: sin foto")
    d = {"sku": sku, "nombre": nombre, "detalle": detalle, "envio": ENVIO}
    if costo:
        d["costo"] = costo
    else:
        d["precio_pendiente"] = True
    return d


def placas(g):
    return [g.marco(f'<div class="categoria">{titulo}</div><div class="sub-cat">{sub}</div>'
                    + g.productos([producto(g, sku, nombre, detalle)]), rubro=RUBRO)
            for sku, titulo, sub, nombre, detalle in PLACAS]
