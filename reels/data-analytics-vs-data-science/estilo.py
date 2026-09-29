"""Estilo comun de los graficos del reel (formato 4:5, 1080x1350 px)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SUPERFICIE = "#fcfcfb"
TEXTO = "#0b0b0b"
TEXTO_SEC = "#52514e"
GRILLA = "#e4e3df"
AZUL = "#2a78d6"     # historico / analytics
NARANJA = "#eb6834"  # prediccion / science


def aplicar():
    plt.rcParams.update({
        "figure.figsize": (10.8, 13.5),
        "figure.dpi": 100,
        "figure.facecolor": SUPERFICIE,
        "axes.facecolor": SUPERFICIE,
        "axes.edgecolor": GRILLA,
        "axes.labelcolor": TEXTO_SEC,
        "axes.titlecolor": TEXTO,
        "axes.titlesize": 30,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.titlepad": 24,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": GRILLA,
        "grid.linewidth": 1,
        "xtick.color": TEXTO_SEC,
        "ytick.color": TEXTO_SEC,
        "xtick.labelsize": 18,
        "ytick.labelsize": 18,
        "font.size": 18,
        "legend.frameon": False,
        "legend.fontsize": 18,
    })


def millones(x, _pos=None) -> str:
    return f"${x / 1e6:,.0f} M".replace(",", ".")
