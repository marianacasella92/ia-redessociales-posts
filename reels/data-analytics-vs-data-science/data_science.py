"""
DATA SCIENCE: usar esos mismos datos para predecir el futuro.

Toma ventas_limpias.xlsx (sale de data_analytics.py: sin datos limpios no hay modelo),
arma la serie de ventas mensuales y ajusta un modelo de regresion con
tendencia + estacionalidad mensual para proyectar los proximos 6 meses.
Mide el error del modelo con los ultimos 3 meses reales antes de proyectar.

Uso:
    python data_analytics.py   # primero
    python data_science.py
"""
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter

import estilo

BASE = Path(__file__).resolve().parent
ORIGEN = BASE / "ventas_limpias.xlsx"
GRAFICO = BASE / "grafico_prediccion.png"
MESES_A_PREDECIR = 6
MESES_DE_PRUEBA = 3
MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]


def mes_corto(d) -> str:
    return f"{MESES[d.month - 1]} {d:%y}"


def features(fechas: pd.DatetimeIndex, inicio: pd.Timestamp) -> np.ndarray:
    """Tendencia (meses desde el inicio) + una columna por mes del año (estacionalidad)."""
    t = (fechas.year - inicio.year) * 12 + (fechas.month - inicio.month)
    meses = np.eye(12)[fechas.month - 1]
    return np.column_stack([t, meses])


def entrenar(serie: pd.Series) -> np.ndarray:
    X = features(serie.index, serie.index[0])
    # Regresion lineal con un toque de regularizacion (ridge) para no sobreajustar con pocos datos
    lam = 1e-3
    return np.linalg.solve(X.T @ X + lam * np.eye(X.shape[1]), X.T @ serie.values)


def predecir(coef: np.ndarray, fechas: pd.DatetimeIndex, inicio: pd.Timestamp) -> np.ndarray:
    return features(fechas, inicio) @ coef


def main():
    df = pd.read_excel(ORIGEN, parse_dates=["Fecha"])
    serie = df.set_index("Fecha")["Monto"].resample("MS").sum()
    inicio = serie.index[0]

    # 1. Validacion: entrenamos sin los ultimos meses y comparamos contra lo real
    train, test = serie[:-MESES_DE_PRUEBA], serie[-MESES_DE_PRUEBA:]
    pred_test = predecir(entrenar(train), test.index, inicio)
    mape = np.mean(np.abs(pred_test - test.values) / test.values) * 100
    print(f"Error medio del modelo en los ultimos {MESES_DE_PRUEBA} meses: {mape:.1f} %")

    # 2. Reentrenamos con todo y proyectamos
    coef = entrenar(serie)
    futuro = pd.date_range(serie.index[-1] + pd.offsets.MonthBegin(), periods=MESES_A_PREDECIR, freq="MS")
    pred = pd.Series(predecir(coef, futuro, inicio), index=futuro)
    residuos = serie.values - predecir(coef, serie.index, inicio)
    # Desvio corregido por los grados de libertad: con 13 parametros y ~21 meses el error "en casa" subestima
    n, k = len(serie), len(coef)
    banda = 1.96 * np.sqrt((residuos ** 2).sum() / (n - k))

    print("\nProyeccion de ventas:")
    print(pred.map(estilo.millones).rename(mes_corto).to_string())

    graficar(serie, pred, banda)


def graficar(serie: pd.Series, pred: pd.Series, banda: float):
    estilo.aplicar()
    fig, ax = plt.subplots()
    ax.plot(serie.index, serie.values, color=estilo.AZUL, linewidth=3, label="Ventas reales")
    # La prediccion arranca desde el ultimo dato real para que la linea sea continua
    unida = pd.concat([serie.iloc[-1:], pred])
    ax.plot(unida.index, unida.values, color=estilo.NARANJA, linewidth=3, linestyle="--", label="Prediccion")
    ax.fill_between(pred.index, pred.values - banda, pred.values + banda,
                    color=estilo.NARANJA, alpha=0.15, linewidth=0, label="Rango probable (95 %)")
    ax.scatter(pred.index, pred.values, color=estilo.NARANJA, s=70, zorder=3,
               edgecolor=estilo.SUPERFICIE, linewidth=2)
    ax.annotate(estilo.millones(pred.max()), (pred.idxmax(), pred.max()),
                textcoords="offset points", xytext=(0, 18), ha="center",
                color=estilo.TEXTO, fontsize=20, fontweight="bold")

    ax.set_title("Ventas mensuales\ny proyeccion a 6 meses")
    ax.yaxis.set_major_formatter(FuncFormatter(estilo.millones))
    ax.set_ylim(0, None)
    ax.grid(axis="x", visible=False)
    ax.legend(loc="upper left")
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: mes_corto(mdates.num2date(x))))
    fig.text(0.02, 0.015, "Data Science: ¿que va a pasar?", color=estilo.TEXTO_SEC, fontsize=18)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(GRAFICO)
    print(f"\nGrafico -> {GRAFICO}")


if __name__ == "__main__":
    main()
