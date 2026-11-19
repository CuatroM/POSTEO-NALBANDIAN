"""Historias — Llegaron los robots FEMA (apertura, 3 placas de productos y cierre).
Productos: SINCRO PRODUCTOS FEMA BASE (datos/productos_fema.csv), solo con stock y con foto.
Precio = costo BaseLinker + 35 % + envío (10 % del costo, mín. $20.000): todas con envío gratis.
"""
ID = "historias-robots"
CARPETA = ""  # se completa al tener los productos definitivos, p. ej. "2026-11-20-historias-robots-fema"

# Productos por grupo: (sku, nombre comercial, detalle). El costo sale de la base.
GRUPOS = {
    "cortacesped": [],
    "aspiradora": [],
    "pileta": [],
}

# Solo para probar el diseño mientras no está la base (se ignora si GRUPOS tiene productos)
MUESTRA = {"sku": "MUESTRA", "nombre": "Robot de muestra", "detalle": "Dato técnico principal", "costo": 500000}


def lista(g, grupo):
    base = g.base()
    filas = []
    for sku, nombre, detalle in GRUPOS[grupo]:
        b = base.get(sku)
        if not b or float(b["stock"] or 0) <= 0 or not g.foto(sku):
            print(f"  {sku}: sin stock o sin foto, no se usa")
            continue
        filas.append({"sku": sku, "nombre": nombre, "detalle": detalle, "costo": b["costo"]})
    return filas or [MUESTRA]


def placas(g):
    apertura = g.marco(
        '<div class="etiqueta">NUEVO</div>'
        '<h1>Llegaron<br>los <em>robots<br>FEMA</em></h1>'
        '<div class="bajada">Cortan el pasto, aspiran tu casa<br>y limpian tu pileta.</div>'
        + g.iconos([("cortacesped", "Cortacésped"), ("aspiradora", "Aspiradora"), ("pileta", "Pileta")]),
        pie="Tecnología que trabaja por vos.")

    def placa_grupo(grupo, titulo, sub):
        return g.marco(f'<div class="categoria">{titulo}</div><div class="sub-cat">{sub}</div>'
                       + g.productos(lista(g, grupo)), rubro="Robots FEMA")

    cortacesped = placa_grupo("cortacesped", "Robots<br><em>cortacésped</em>", "El pasto siempre corto, sin esfuerzo.")
    aspiradora = placa_grupo("aspiradora", "Robots<br><em>aspiradora</em>", "Tu casa limpia mientras hacés otra cosa.")
    pileta = placa_grupo("pileta", "Robots<br><em>para pileta</em>", "Fondo y paredes limpios, sin sacar una gota.")

    cierre = g.marco(
        '<h1 style="font-size:124px">Los <em>robots<br>FEMA</em><br>ya están acá</h1>'
        '<div class="bajada">Que el pasto, la casa y la pileta<br>se hagan solos. <b>Vos solo disfrutá.</b></div>'
        f'<div class="contacto"><div class="titulo-c">{g.svg("whatsapp")}Consultanos por WhatsApp</div>'
        '<div class="numeros"><b>351 547 8486</b><b>3541 618395</b></div></div>',
        pie="6 meses de garantía, servicio técnico<br>y envíos a todo el país.")

    return [apertura, cortacesped, aspiradora, pileta, cierre]
