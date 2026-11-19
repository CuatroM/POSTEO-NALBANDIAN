"""Historias — Llegaron los robots FEMA: apertura, una placa por producto y cierre.
Productos: SINCRO PRODUCTOS FEMA BASE (datos/productos_fema.csv), solo con stock y con foto.
Precio = costo BaseLinker + 35 % + envío (10 % del costo, mín. $20.000): todas con envío gratis.
"""
ID = "historias-robots"
CARPETA = ""  # se completa al aprobar, p. ej. "2026-11-20-historias-robots-fema"

# Una placa por producto: (sku, título de la placa, bajada, nombre comercial, detalle)
PLACAS = [
    ("69383247#FEMA", "Robot<br><em>cortacésped</em>", "El pasto siempre corto, sin esfuerzo.",
     "Robot cortacésped FEMA con cámara", "Sin cable perimetral: navega con cámara e IA, control por app Wi-Fi. Batería 5 Ah"),
    ("69383810#FEMA", "Robot<br><em>aspiradora</em>", "Tu casa limpia mientras hacés otra cosa.",
     "Robot aspiradora FEMA", "Aspira sola toda la casa"),
    ("69606708#FEMA", "Robot<br><em>para pileta</em>", "El fondo limpio, sin cables.",
     "Robot limpiador de piletas QD01", "Limpia el fondo de la pileta"),
    ("69606710#FEMA", "Robot<br><em>para pileta</em>", "Fondo y paredes limpios, sin sacar una gota.",
     "Robot limpiador de piletas PC10", "Fondo y paredes"),
    ("69606713#FEMA", "Robot<br><em>para pileta</em>", "La superficie del agua siempre limpia.",
     "Robot limpiador de superficie QT200", "Limpia la superficie del agua"),
]

# Costos que todavía no están en la base de BaseLinker (informados a mano)
COSTOS_MANUALES = {"69383247#FEMA": 1324998.40}

ENVIO = "ENVÍO GRATIS POR TRANSPORTE CREDIFIN"


def producto(g, sku, nombre, detalle):
    b = g.base().get(sku)
    costo = COSTOS_MANUALES.get(sku) or (b and b["costo"])
    if b and float(b["stock"] or 0) <= 0:
        print(f"  ATENCIÓN {sku}: sin stock en la base")
    if not g.foto(sku):
        print(f"  ATENCIÓN {sku}: sin foto")
    if not costo:
        return {"sku": sku, "nombre": nombre, "detalle": detalle, "precio_pendiente": True, "envio": ENVIO}
    return {"sku": sku, "nombre": nombre, "detalle": detalle, "costo": costo, "envio": ENVIO}


def placas(g):
    apertura = g.marco(
        '<div class="etiqueta">NUEVO</div>'
        '<h1>Llegaron<br>los <em>robots<br>FEMA</em></h1>'
        '<div class="bajada">Cortan el pasto, aspiran tu casa<br>y limpian tu pileta.</div>'
        + g.iconos([("cortacesped", "Cortacésped"), ("aspiradora", "Aspiradora"), ("pileta", "Pileta")]),
        pie="Tecnología que trabaja por vos.")

    productos = [g.marco(f'<div class="categoria">{titulo}</div><div class="sub-cat">{sub}</div>'
                         + g.productos([producto(g, sku, nombre, detalle)]))
                 for sku, titulo, sub, nombre, detalle in PLACAS]

    cierre = g.marco(
        '<h1 style="font-size:124px">Los <em>robots<br>FEMA</em><br>ya están acá</h1>'
        '<div class="bajada">Que el pasto, la casa y la pileta<br>se hagan solos. <b>Vos solo disfrutá.</b></div>'
        f'<div class="contacto"><div class="titulo-c">{g.svg("whatsapp")}Consultanos por WhatsApp</div>'
        '<div class="numeros"><b>3515478486</b><b>3541618395</b></div></div>',
        pie="6 meses de garantía, servicio técnico<br>y envíos a todo el país.")

    return [apertura, *productos, cierre]
