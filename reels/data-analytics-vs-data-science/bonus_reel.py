import pandas as pd

# --- Las 2 lineas para mostrar en pantalla (bloque 4 del reel) ---
df = pd.read_excel("ventas_limpias.xlsx")
grafico = df.groupby("Categoria")["Monto"].sum().sort_values().plot.barh()

grafico.figure.savefig("bonus.png", bbox_inches="tight")
