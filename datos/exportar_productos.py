"""
Conexión con SINCRO PRODUCTOS FEMA BASE (solo lectura).

Lee de BaseLinker el inventario que mantiene actualizado la sincronización
(INVENTARIO COMPLETO FEMA 2026 MATIAS) y guarda la base de productos para los
contenidos de Alexis Nalbandian en datos/productos_fema.csv:

    sku ; nombre ; costo ; stock ; foto

- costo = precio del grupo "GRUPO DE PRECIO COMPLETO FEMA 2026 MATIAS" (el que informa la sincronización)
- stock = depósito "ALMACEN COMPLETO FEMA 2026 MATIAS"
- foto  = "si" si existe disenos/productos/<SKU>.jpg

No escribe nada en BaseLinker. Necesita el secreto BL_TOKEN.
"""
import csv
import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

INVENTARIO = 61608        # INVENTARIO COMPLETO FEMA 2026 MATIAS
GRUPO_PRECIO = "65271"    # GRUPO DE PRECIO COMPLETO FEMA 2026 MATIAS
DEPOSITO = "bl_75994"     # ALMACEN COMPLETO FEMA 2026 MATIAS
URL = "https://api.baselinker.com/connector.php"

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "datos" / "productos_fema.csv"
FOTOS = RAIZ / "disenos" / "productos"

TOKEN = os.environ.get("BL_TOKEN", "").strip()
if not TOKEN:
    sys.exit("ERROR: falta el secreto BL_TOKEN (token de API de BaseLinker).")


def llamar(metodo, params):
    for intento in range(1, 4):
        time.sleep(0.7)
        try:
            r = requests.post(URL, headers={"X-BLToken": TOKEN},
                              data={"method": metodo, "parameters": json.dumps(params)}, timeout=120)
            d = r.json()
        except Exception as e:  # noqa: BLE001
            print(f"{metodo}: error de conexión ({e}), intento {intento}/3")
            time.sleep(10 * intento)
            continue
        if d.get("status") == "SUCCESS":
            return d
        msg = f"{d.get('error_code')}: {d.get('error_message')}"
        if "limit" in msg.lower():
            time.sleep(60)
            continue
        sys.exit(f"BaseLinker {metodo} -> {msg}")
    sys.exit(f"BaseLinker {metodo}: sin respuesta")


def main():
    ids, pagina = [], 1
    while True:
        lote = llamar("getInventoryProductsList", {"inventory_id": INVENTARIO, "page": pagina}).get("products") or {}
        ids += list(lote)
        if len(lote) < 1000:
            break
        pagina += 1
    print(f"Productos en el inventario: {len(ids)}")

    filas = []
    for k in range(0, len(ids), 100):
        d = llamar("getInventoryProductsData",
                   {"inventory_id": INVENTARIO, "products": [int(x) for x in ids[k:k + 100]]})
        for p in (d.get("products") or {}).values():
            sku = (p.get("sku") or "").strip()
            if not sku:
                continue
            costo = (p.get("prices") or {}).get(GRUPO_PRECIO)
            stock = (p.get("stock") or {}).get(DEPOSITO, 0)
            base = sku.split("#")[0]
            foto = any((FOTOS / f"{n}.jpg").exists() for n in (sku, base))
            filas.append({"sku": sku, "nombre": (p.get("text_fields") or {}).get("name", ""),
                          "costo": costo if costo is not None else "", "stock": stock,
                          "foto": "si" if foto else "no"})

    filas.sort(key=lambda f: f["sku"])
    SALIDA.parent.mkdir(exist_ok=True)
    with SALIDA.open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=["sku", "nombre", "costo", "stock", "foto"], delimiter=";")
        w.writeheader()
        w.writerows(filas)
    hora = datetime.now(timezone(timedelta(hours=-3))).strftime("%d/%m/%Y %H:%M")
    con_stock = sum(1 for f in filas if float(f["stock"] or 0) > 0)
    (RAIZ / "datos" / "ultima-actualizacion.txt").write_text(
        f"{hora} (Argentina) - {len(filas)} productos, {con_stock} con stock\n", encoding="utf-8")
    print(f"Guardado {SALIDA.relative_to(RAIZ)}: {len(filas)} productos, {con_stock} con stock.")


if __name__ == "__main__":
    main()
