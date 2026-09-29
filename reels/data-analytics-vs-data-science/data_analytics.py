"""
DATA ANALYTICS: datos del pasado y del presente -> preguntas concretas de negocio.

1. Carga el export crudo.
2. Lo limpia (duplicados, montos vacios/negativos, categorias mal escritas).
3. Responde: cuanto vendimos, que categoria y region mueven el negocio, que canal crece.
4. Guarda ventas_limpias.xlsx (la base para Data Science) y grafico_analytics.png.

Uso:
    python data_analytics.py
"""
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

import estilo

BASE = Path(__file__).resolve().parent
ORIGEN = BASE / "ventas_tienda_online.xlsx"
LIMPIO = BASE / "ventas_limpias.xlsx"
GRAFICO = BASE / "grafico_analytics.png"

try:
    import python_calamine  # noqa: F401  lectura ~10x mas rapida
    MOTOR = "calamine"
except ImportError:
    MOTOR = "openpyxl"


def limpiar(df: pd.DataFrame) -> pd.DataFrame:
    antes = len(df)
    df = df.drop_duplicates("Pedido")
    df = df.dropna(subset=["Monto"])
    df = df[df["Monto"] > 0]
    df["Categoria"] = df["Categoria"].str.strip().str.capitalize()
    df["Fecha"] = pd.to_datetime(df["Fecha"])
    print(f"Limpieza: {antes:,} -> {len(df):,} filas ({antes - len(df):,} descartadas)".replace(",", "."))
    return df


def responder(df: pd.DataFrame):
    total = df["Monto"].sum()
    print(f"\nVenta total: ${total:,.0f}".replace(",", "."))
    print(f"Ticket promedio: ${df['Monto'].mean():,.0f}".replace(",", "."))

    print("\n¿Que categoria mueve el negocio?")
    cat = df.groupby("Categoria")["Monto"].sum().sort_values(ascending=False)
    print((cat / total * 100).round(1).astype(str).add(" %").to_string())

    print("\n¿Que region vende mas?")
    print(df.groupby("Region")["Monto"].sum().sort_values(ascending=False).map(estilo.millones).to_string())

    print("\n¿Que canal crece? (ventas ene-sep 2025 vs ene-sep 2024)")
    periodo = df[df["Fecha"].dt.month <= 9]
    canal = periodo.pivot_table(index="Canal", columns=periodo["Fecha"].dt.year, values="Monto", aggfunc="sum")
    print(((canal[2025] / canal[2024] - 1) * 100).round(1).astype(str).add(" %").to_string())
    return cat


def graficar(cat: pd.Series):
    estilo.aplicar()
    fig, ax = plt.subplots()
    cat = cat.sort_values()
    barras = ax.barh(cat.index, cat.values, color=estilo.AZUL, height=0.6)
    ax.bar_label(barras, labels=[estilo.millones(v) for v in cat.values],
                 padding=10, color=estilo.TEXTO, fontsize=20)
    ax.set_title("Ventas por categoria\nene 2024 - sep 2025")
    # Cada barra ya tiene su valor: el eje X sobra
    ax.xaxis.set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.grid(False)
    ax.tick_params(axis="y", labelsize=22, length=0)
    ax.set_xlim(0, cat.max() * 1.25)
    fig.text(0.02, 0.015, "Data Analytics: ¿que paso y que hacemos hoy?", color=estilo.TEXTO_SEC, fontsize=18)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(GRAFICO)
    print(f"\nGrafico -> {GRAFICO}")


def main():
    df = limpiar(pd.read_excel(ORIGEN, engine=MOTOR))
    df.to_excel(LIMPIO, index=False)
    print(f"Datos limpios -> {LIMPIO}")
    graficar(responder(df))


if __name__ == "__main__":
    main()
