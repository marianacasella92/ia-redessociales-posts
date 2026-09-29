"""
Genera el Excel "pesado" para el reel Excel vs Python.

Crea ventas_2025.xlsx con:
  - Hoja "Ventas": 100.000 filas de ventas con una columna Total calculada por formula.
  - Hoja "Productos": catalogo con categoria y costo unitario.
  - Hoja "Resumen": SUMIFS / BUSCARX sobre toda la hoja Ventas (lo que hace que Excel se tilde).

Uso:
    python generar_excel.py            # 100.000 filas
    python generar_excel.py 300000     # mas filas para que se tilde mas
"""
import sys
import random
from datetime import date, timedelta
from pathlib import Path

from openpyxl import Workbook
from openpyxl.cell import WriteOnlyCell
from openpyxl.styles import Font, PatternFill, Alignment

BASE = Path(__file__).resolve().parent
DST = BASE / "ventas_2025.xlsx"

N_FILAS = int(sys.argv[1]) if len(sys.argv) > 1 else 100_000
random.seed(42)

SUCURSALES = ["Buenos Aires", "Cordoba", "Rosario", "Mendoza", "La Plata", "Mar del Plata", "Tucuman", "Salta"]
VENDEDORES = [f"V{n:03d}" for n in range(1, 41)]
MEDIOS_PAGO = ["Efectivo", "Debito", "Credito", "Transferencia", "QR"]

# (codigo, producto, categoria, precio, costo)
PRODUCTOS = [
    ("P001", "Notebook 14", "Tecnologia", 850_000, 610_000),
    ("P002", "Monitor 24", "Tecnologia", 240_000, 165_000),
    ("P003", "Mouse inalambrico", "Accesorios", 18_000, 9_500),
    ("P004", "Teclado mecanico", "Accesorios", 65_000, 38_000),
    ("P005", "Auriculares BT", "Accesorios", 45_000, 24_000),
    ("P006", "Silla ergonomica", "Oficina", 320_000, 205_000),
    ("P007", "Escritorio", "Oficina", 280_000, 170_000),
    ("P008", "Lampara LED", "Oficina", 22_000, 11_000),
    ("P009", "Disco SSD 1TB", "Tecnologia", 95_000, 62_000),
    ("P010", "Webcam HD", "Accesorios", 38_000, 21_000),
    ("P011", "Router WiFi 6", "Tecnologia", 120_000, 78_000),
    ("P012", "Impresora", "Oficina", 210_000, 140_000),
    ("P013", "Tablet 10", "Tecnologia", 390_000, 270_000),
    ("P014", "Cable HDMI", "Accesorios", 7_500, 2_800),
    ("P015", "Mochila notebook", "Accesorios", 42_000, 19_000),
]

HEADER_FONT = Font(bold=True, color="FFFFFF")
HEADER_FILL = PatternFill("solid", fgColor="217346")  # verde Excel


def header_row(ws, titulos):
    fila = []
    for t in titulos:
        c = WriteOnlyCell(ws, value=t)
        c.font = HEADER_FONT
        c.fill = HEADER_FILL
        c.alignment = Alignment(horizontal="center")
        fila.append(c)
    ws.append(fila)


def hoja_ventas(wb):
    ws = wb.create_sheet("Ventas")
    ws.freeze_panes = "A2"
    for col, ancho in zip("ABCDEFGHIJ", [10, 12, 16, 10, 10, 20, 10, 12, 16, 14]):
        ws.column_dimensions[col].width = ancho
    header_row(ws, ["ID", "Fecha", "Sucursal", "Vendedor", "Codigo", "Producto",
                    "Cantidad", "Precio", "Medio de pago", "Total"])

    inicio = date(2025, 1, 1)
    for i in range(1, N_FILAS + 1):
        cod, prod, _, precio, _ = random.choice(PRODUCTOS)
        fila = i + 1
        # Algo de "suciedad" realista: precios con descuento/recargo
        precio_final = round(precio * random.uniform(0.9, 1.05))
        ws.append([
            i,
            inicio + timedelta(days=random.randint(0, 364)),
            random.choice(SUCURSALES),
            random.choice(VENDEDORES),
            cod,
            prod,
            random.choices([1, 2, 3, 4, 5], weights=[55, 25, 10, 6, 4])[0],
            precio_final,
            random.choice(MEDIOS_PAGO),
            f"=G{fila}*H{fila}",
        ])


def hoja_productos(wb):
    ws = wb.create_sheet("Productos")
    header_row(ws, ["Codigo", "Producto", "Categoria", "Precio lista", "Costo"])
    for p in PRODUCTOS:
        ws.append(list(p))


def hoja_resumen(wb):
    """Formulas que recorren toda la hoja Ventas: aca es donde Excel empieza a sufrir."""
    ws = wb.create_sheet("Resumen")
    ultima = N_FILAS + 1
    total = f"Ventas!$J$2:$J${ultima}"
    suc = f"Ventas!$C$2:$C${ultima}"
    fec = f"Ventas!$B$2:$B${ultima}"

    header_row(ws, ["Sucursal"] + [f"Mes {m:02d}" for m in range(1, 13)] + ["Total"])
    for r, s in enumerate(SUCURSALES, start=2):
        fila = [s]
        for m in range(1, 13):
            desde = f"DATE(2025,{m},1)"
            hasta = f"EOMONTH(DATE(2025,{m},1),0)"
            fila.append(f'=SUMIFS({total},{suc},$A{r},{fec},">="&{desde},{fec},"<="&{hasta})')
        fila.append(f"=SUM(B{r}:M{r})")
        ws.append(fila)

    ws.append([])
    ws.append(["Venta total", f"=SUM({total})"])
    ws.append(["Ticket promedio", f"=AVERAGE({total})"])
    ws.append(["Operaciones", f"=COUNTA(Ventas!$A$2:$A${ultima})"])


def main():
    wb = Workbook(write_only=True)
    print(f"Generando {N_FILAS:,} filas...".replace(",", "."))
    hoja_ventas(wb)
    hoja_productos(wb)
    hoja_resumen(wb)
    wb.save(DST)
    print(f"OK -> {DST}")


if __name__ == "__main__":
    main()
