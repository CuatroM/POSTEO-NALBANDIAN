"""Historias — Llegaron los robots FEMA (apertura, 3 placas de productos y cierre).
Productos: SINCRO PRODUCTOS FEMA BASE (datos/productos_fema.csv), solo con stock y con foto.
Precio = costo BaseLinker + 35 % + envío (10 % del costo, mín. $20.000): todas con envío gratis.
"""
ID = "historias-robots"
CARPETA = ""  # se completa al tener los productos definitivos, p. ej. "2026-11-20-historias-robots-fema"

# Productos por grupo: (sku, nombre comercial, detalle). El costo sale de la base.
GRUPOS = {
    "cortacesped": [
        ("69383235#FEMA", "Robot cortacésped FR35", "Para jardines de hasta 800 m²"),
        ("69383238#FEMA", "Robot cortacésped FR55", "Para jardines de hasta 1.600 m²"),
        ("69383243#FEMA", "Robot cortacésped FR100", "Hasta 10.000 m². 3 en 1, con batería y cargador 20 V"),
    ],
    "aspiradora": [
        ("69383810#FEMA", "Robot aspiradora FEMA", "Aspira sola toda la casa"),
    ],
    "pileta": [
        ("69606708#FEMA", "Robot limpiador de piletas QD01", "Limpia el fondo de la pileta"),
        ("69606710#FEMA", "Robot limpiador de piletas PC10", "Fondo y paredes"),
        ("69606713#FEMA", "Robot limpiador de superficie QT200", "Limpia la superficie del agua"),
    ],
}
# El stock de los cortacésped en BaseLinker está en 0 (export 19/11): se muestran igual hasta que se decida.
SIN_STOCK_PERMITIDO = {"cortacesped"}


def lista(g, grupo):
    base = g.base()
    filas = []
    for sku, nombre, detalle in GRUPOS[grupo]:
        b = base.get(sku)
        if not b:
            print(f"  {sku}: no está en la base, no se usa")
            continue
        if float(b["stock"] or 0) <= 0 and grupo not in SIN_STOCK_PERMITIDO:
            print(f"  {sku}: sin stock, no se usa")
            continue
        if not g.foto(sku):
            print(f"  {sku}: SIN FOTO (queda marcado como pendiente)")
        filas.append({"sku": sku, "nombre": nombre, "detalle": detalle, "costo": b["costo"]})
    return filas


def placas(g):
    apertura = g.marco(
        '<div class="etiqueta">NUEVO</div>'
        '<h1>Llegaron<br>los <em>robots<br>FEMA</em></h1>'
        '<div class="bajada">Cortan el pasto, aspiran tu casa<br>y limpian tu pileta.</div>'
        + g.iconos([("cortacesped", "Cortacésped"), ("aspiradora", "Aspiradora"), ("pileta", "Pileta")]),
        pie="Tecnología que trabaja por vos.", semilla=11)

    def placa_grupo(grupo, titulo, sub, semilla):
        return g.marco(f'<div class="categoria">{titulo}</div><div class="sub-cat">{sub}</div>'
                       + g.productos(lista(g, grupo)), semilla=semilla)

    cortacesped = placa_grupo("cortacesped", "Robots<br><em>cortacésped</em>", "El pasto siempre corto, sin esfuerzo.", 22)
    aspiradora = placa_grupo("aspiradora", "Robots<br><em>aspiradora</em>", "Tu casa limpia mientras hacés otra cosa.", 33)
    pileta = placa_grupo("pileta", "Robots<br><em>para pileta</em>", "Fondo y paredes limpios, sin sacar una gota.", 44)

    cierre = g.marco(
        '<h1 style="font-size:124px">Los <em>robots<br>FEMA</em><br>ya están acá</h1>'
        '<div class="bajada">Que el pasto, la casa y la pileta<br>se hagan solos. <b>Vos solo disfrutá.</b></div>'
        f'<div class="contacto"><div class="titulo-c">{g.svg("whatsapp")}Consultanos por WhatsApp</div>'
        '<div class="numeros"><b>351 547 8486</b><b>3541 618395</b></div></div>',
        pie="6 meses de garantía, servicio técnico<br>y envíos a todo el país.", semilla=55)

    return [apertura, cortacesped, aspiradora, pileta, cierre]
