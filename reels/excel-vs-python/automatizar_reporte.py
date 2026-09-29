"""
El mismo trabajo que la hoja "Resumen" del Excel, pero en segundos y sin tocar nada a mano.

Lee uno o varios Excel de ventas, limpia los datos, cruza con el catalogo de productos
y genera reporte_ventas.xlsx con:
  - Ventas por sucursal y mes
  - Top 10 productos por ganancia
  - Ventas por medio de pago
  - Un grafico de barras listo para presentar

Uso:
    python automatizar_reporte.py                       # procesa ventas_2025.xlsx
    python automatizar_reporte.py carpeta_con_excels/   # procesa TODOS los .xlsx de la carpeta
"""
import sys
import time
from pathlib import Path

import pandas as pd
from openpyxl.chart import BarChart, Reference
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

BASE = Path(__file__).resolve().parent
ORIGEN = Path(sys.argv[1]) if len(sys.argv) > 1 else BASE / "ventas_2025.xlsx"
DST = BASE / "reporte_ventas.xlsx"

# calamine lee Excel ~10x mas rapido que openpyxl (pip install python-calamine)
try:
    import python_calamine  # noqa: F401
    MOTOR = "calamine"
except ImportError:
    MOTOR = "openpyxl"

MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]


def listar_archivos(origen: Path) -> list[Path]:
    if origen.is_dir():
        return sorted(p for p in origen.glob("*.xlsx") if not p.name.startswith(("~$", "reporte_")))
    return [origen]


def cargar(archivos: list[Path]) -> tuple[pd.DataFrame, pd.DataFrame]:
    ventas, productos = [], []
    for archivo in archivos:
        print(f"  Leyendo {archivo.name}...")
        hojas = pd.read_excel(archivo, sheet_name=["Ventas", "Productos"], engine=MOTOR)
        ventas.append(hojas["Ventas"])
        productos.append(hojas["Productos"])
    return pd.concat(ventas, ignore_index=True), pd.concat(productos).drop_duplicates("Codigo")


def limpiar(df: pd.DataFrame, productos: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates("ID").dropna(subset=["Fecha", "Codigo", "Cantidad", "Precio"])
    df["Fecha"] = pd.to_datetime(df["Fecha"])
    # La columna Total del Excel es una formula: la recalculamos en vez de depender de ella
    df["Total"] = df["Cantidad"] * df["Precio"]
    # El BUSCARV de toda la vida, pero en una linea
    df = df.merge(productos[["Codigo", "Categoria", "Costo"]], on="Codigo", how="left")
    df["Ganancia"] = df["Total"] - df["Cantidad"] * df["Costo"]
    df["Mes"] = df["Fecha"].dt.month
    return df


def resumir(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    por_sucursal = df.pivot_table(index="Sucursal", columns="Mes", values="Total",
                                  aggfunc="sum", fill_value=0)
    por_sucursal.columns = [MESES[m - 1] for m in por_sucursal.columns]
    por_sucursal["Total"] = por_sucursal.sum(axis=1)
    por_sucursal = por_sucursal.sort_values("Total", ascending=False)

    top_productos = (df.groupby(["Producto", "Categoria"], as_index=False)
                       .agg(Unidades=("Cantidad", "sum"), Ventas=("Total", "sum"),
                            Ganancia=("Ganancia", "sum"))
                       .sort_values("Ganancia", ascending=False)
                       .head(10))
    top_productos["Margen %"] = (top_productos["Ganancia"] / top_productos["Ventas"] * 100).round(1)

    medios = (df.groupby("Medio de pago", as_index=False)
                .agg(Operaciones=("ID", "count"), Ventas=("Total", "sum"))
                .sort_values("Ventas", ascending=False))

    kpis = pd.DataFrame({
        "Indicador": ["Venta total", "Ganancia total", "Ticket promedio", "Operaciones"],
        "Valor": [df["Total"].sum(), df["Ganancia"].sum(), round(df["Total"].mean()), len(df)],
    })
    return {"KPIs": kpis, "Por sucursal": por_sucursal.reset_index(),
            "Top productos": top_productos, "Medios de pago": medios}


def dar_formato(ws):
    for celda in ws[1]:
        celda.font = Font(bold=True, color="FFFFFF")
        celda.fill = PatternFill("solid", fgColor="3776AB")  # azul Python
        celda.alignment = Alignment(horizontal="center")
    for i, col in enumerate(ws.columns, start=1):
        ancho = max(len(str(c.value or "")) for c in col)
        ws.column_dimensions[get_column_letter(i)].width = min(ancho + 3, 30)
        for c in col[1:]:
            if isinstance(c.value, (int, float)):
                c.number_format = "#,##0"
    ws.freeze_panes = "A2"


def agregar_grafico(ws):
    filas = ws.max_row
    col_total = ws.max_column
    grafico = BarChart()
    grafico.title = "Ventas anuales por sucursal"
    grafico.y_axis.title = "Pesos"
    grafico.height, grafico.width = 9, 18
    grafico.add_data(Reference(ws, min_col=col_total, min_row=1, max_row=filas), titles_from_data=True)
    grafico.set_categories(Reference(ws, min_col=1, min_row=2, max_row=filas))
    grafico.legend = None
    ws.add_chart(grafico, f"A{filas + 3}")


def exportar(tablas: dict[str, pd.DataFrame]):
    with pd.ExcelWriter(DST, engine="openpyxl") as writer:
        for nombre, tabla in tablas.items():
            tabla.to_excel(writer, sheet_name=nombre, index=False)
            dar_formato(writer.sheets[nombre])
        agregar_grafico(writer.sheets["Por sucursal"])


def main():
    inicio = time.perf_counter()
    archivos = listar_archivos(ORIGEN)
    if not archivos:
        sys.exit(f"No encontre archivos .xlsx en {ORIGEN}")

    print(f"Procesando {len(archivos)} archivo(s)")
    ventas, productos = cargar(archivos)
    df = limpiar(ventas, productos)
    tablas = resumir(df)
    exportar(tablas)

    segundos = time.perf_counter() - inicio
    print(f"\n{len(df):,} filas procesadas en {segundos:.1f} s".replace(",", "."))
    print(tablas["KPIs"].to_string(index=False))
    print(f"\nReporte listo -> {DST}")


if __name__ == "__main__":
    main()
