"""
Genera el "archivo gigante e incomprensible" del reel Data Analytics vs Data Science.

Crea ventas_tienda_online.xlsx con ~60.000 pedidos (ene-2024 a sep-2025) y la suciedad
tipica de un export real, para que la limpieza tenga sentido:
  - pedidos duplicados
  - montos vacios
  - categorias escritas de distintas formas ("Electronica", " electronica", "ELECTRONICA")
  - montos negativos (devoluciones mal cargadas)

Uso:
    python generar_datos.py
"""
import random
from datetime import date, timedelta
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

BASE = Path(__file__).resolve().parent
DST = BASE / "ventas_tienda_online.xlsx"
N_PEDIDOS = 60_000
random.seed(9)

INICIO, FIN = date(2024, 1, 1), date(2025, 9, 30)
DIAS = (FIN - INICIO).days + 1

# categoria: (ticket promedio, peso en las ventas)
CATEGORIAS = {
    "Electronica": (150_000, 10),
    "Hogar": (55_000, 20),
    "Moda": (38_000, 30),
    "Deportes": (62_000, 16),
    "Libros": (18_000, 14),
    "Juguetes": (29_000, 10),
}
REGIONES = {"AMBA": 45, "Centro": 20, "Cuyo": 10, "Patagonia": 9, "NOA": 9, "NEA": 7}
CANALES = ["Web", "App", "Marketplace"]
# Estacionalidad: picos en Hot Sale (mayo), Dia del Nino (agosto), Cyber Monday (nov) y fiestas
ESTACIONALIDAD = {1: 0.8, 2: 0.75, 3: 0.9, 4: 0.95, 5: 1.25, 6: 1.0,
                  7: 1.05, 8: 1.2, 9: 0.95, 10: 1.0, 11: 1.35, 12: 1.5}


def fecha_aleatoria() -> date:
    """Elige una fecha con tendencia creciente (el negocio crece) y estacionalidad."""
    while True:
        d = INICIO + timedelta(days=random.randrange(DIAS))
        crecimiento = 1 + 0.6 * (d - INICIO).days / DIAS
        if random.random() < crecimiento * ESTACIONALIDAD[d.month] / 2.5:
            return d


def canal_aleatorio(d: date) -> str:
    """La App gana terreno con el tiempo; la Web lo pierde."""
    avance = (d - INICIO).days / DIAS
    return random.choices(CANALES, weights=[55 - 25 * avance, 20 + 30 * avance, 25])[0]


def ensuciar_categoria(cat: str) -> str:
    r = random.random()
    if r < 0.05:
        return cat.upper()
    if r < 0.10:
        return f" {cat.lower()}"
    return cat


def main():
    wb = Workbook()
    ws = wb.active
    ws.title = "Pedidos"
    ws.append(["Pedido", "Fecha", "Cliente", "Region", "Canal", "Categoria", "Unidades", "Monto"])
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="217346")
    ws.freeze_panes = "A2"

    nombres = list(CATEGORIAS)
    pesos = [p for _, p in CATEGORIAS.values()]
    filas = []
    for i in range(1, N_PEDIDOS + 1):
        cat = random.choices(nombres, weights=pesos)[0]
        ticket, _ = CATEGORIAS[cat]
        unidades = random.choices([1, 2, 3, 4], weights=[70, 20, 7, 3])[0]
        monto = round(ticket * unidades * random.uniform(0.6, 1.4), -1)
        if random.random() < 0.02:
            monto = None
        elif random.random() < 0.005:
            monto = -monto
        fecha = fecha_aleatoria()
        region = random.choices(list(REGIONES), weights=list(REGIONES.values()))[0]
        filas.append([f"PED-{i:06d}", fecha, f"CLI-{random.randint(1, 18_000):05d}",
                      region, canal_aleatorio(fecha),
                      ensuciar_categoria(cat), unidades, monto])

    # ~1,5% de pedidos duplicados, como pasa al unir exports
    filas += random.sample(filas, k=int(N_PEDIDOS * 0.015))
    filas.sort(key=lambda f: f[1])
    for f in filas:
        ws.append(f)
    for col, ancho in zip("ABCDEFGH", [13, 12, 11, 11, 13, 14, 10, 12]):
        ws.column_dimensions[col].width = ancho

    wb.save(DST)
    print(f"{len(filas):,} filas -> {DST}".replace(",", "."))


if __name__ == "__main__":
    main()
