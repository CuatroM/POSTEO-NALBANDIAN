"""Historias — Conservadoras y camping FEMA: apertura, una placa por producto y cierre.
Productos: SINCRO PRODUCTOS FEMA BASE (datos/productos_fema.csv), solo con stock y con foto.
Precio = costo BaseLinker + 35 % + envío (10 % del costo, mín. $20.000): todas con envío gratis.
"""
ID = "historias-camping"
CARPETA = ""  # se completa al aprobar

RUBRO = "Camping FEMA"
ENVIO = "ENVÍO GRATIS POR TRANSPORTE CREDIFIN"

# Una placa por producto: (sku, título de la placa, bajada, nombre comercial, detalle)
PLACAS = [
    ("69606739#FEMA", "Conservadora<br><em>24 litros</em>", "Bebidas frías para la escapada.",
     "Conservadora FEMA 24&nbsp;L", "Liviana y fácil de llevar"),
    ("69606743#FEMA", "Conservadora<br><em>57 litros</em>", "Para el finde largo o la familia completa.",
     "Conservadora FEMA 57&nbsp;L", "Gran capacidad para todo el grupo"),
    ("69365405#FEMA", "Reposera<br><em>Cauchito</em>", "Descanso al aire libre, donde quieras.",
     "Reposera Cauchito FEMA", "Plegable, fácil de transportar"),
    ("69365408#FEMA", "Reposera<br><em>Emperador</em>", "Comodidad para la playa y el camping.",
     "Reposera Emperador FEMA", "Plegable, fácil de transportar"),
    ("69380320#FEMA", "Generador<br><em>inverter 800&nbsp;W</em>", "Energía silenciosa para el camping.",
     "Generador inverter FEMA 800&nbsp;W", "220 V, liviano y portátil"),
    ("69380590#FEMA", "Estación de<br><em>energía 1000&nbsp;W</em>", "Cargá todo, sin ruido ni combustible.",
     "Estación de energía recargable FEMA", "1000 W, 960 Wh. Carga solar y 12 V, salidas USB"),
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
    apertura = g.marco(
        '<div class="etiqueta">TEMPORADA DE VERANO</div>'
        '<h1>Todo listo<br>para el<br><em>camping</em></h1>'
        '<div class="bajada">Conservadoras, reposeras y energía<br>para disfrutar al aire libre.</div>'
        + g.iconos([("conservadora", "Conservadoras"), ("reposera", "Reposeras"), ("energia", "Energía")]),
        pie="Equipate para tu próxima escapada.", rubro=RUBRO)

    productos = [g.marco(f'<div class="categoria">{titulo}</div><div class="sub-cat">{sub}</div>'
                         + g.productos([producto(g, sku, nombre, detalle)]), rubro=RUBRO)
                 for sku, titulo, sub, nombre, detalle in PLACAS]

    cierre = g.marco(
        '<h1 style="font-size:124px">Tu próxima<br><em>escapada</em><br>empieza acá</h1>'
        '<div class="bajada">Frío, descanso y energía<br>donde vayas. <b>Vos solo disfrutá.</b></div>'
        f'<div class="contacto"><div class="titulo-c">{g.svg("whatsapp")}Consultanos por WhatsApp</div>'
        '<div class="numeros"><b>3515478486</b><b>3541618395</b></div></div>',
        pie="6 meses de garantía, servicio técnico<br>y envíos a todo el país.", rubro=RUBRO)

    return [apertura, *productos, cierre]
