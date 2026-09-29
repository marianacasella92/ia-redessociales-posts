# Reel: Data Analytics vs Data Science

Viernes 09/10 · Feed (Reel educativo / comparación) · Keyword: `DATA` · ~45-55 s

## Archivos

| Archivo | Qué es |
|---|---|
| `ventas_tienda_online.xlsx` | El "archivo gigante e incomprensible": ~61.000 pedidos de una tienda online (ene-2024 a sep-2025) con duplicados, montos vacíos o negativos y categorías mal escritas. |
| `data_analytics.py` | **Data Analytics**: limpia los datos y responde preguntas de negocio (qué categoría, región y canal venden más). Genera `ventas_limpias.xlsx` y `grafico_analytics.png`. |
| `data_science.py` | **Data Science**: con los datos limpios entrena un modelo (tendencia + estacionalidad), mide su error y proyecta 6 meses. Genera `grafico_prediccion.png`. |
| `bonus_reel.py` | Las **2 líneas** del bonus (bloque 4) → `bonus.png`. |
| `generar_datos.py` / `estilo.py` | Regenera el Excel crudo / estilo común de los gráficos (4:5, 1080×1350). |

```bash
pip install -r requirements.txt
python data_analytics.py    # primero: limpia y analiza
python data_science.py      # después: predice (necesita ventas_limpias.xlsx)
python bonus_reel.py
```

## Qué mostrar en cada bloque del guion

| Bloque | Tiempo | Material |
|---|---|---|
| 1. Hook | 00:00-00:06 | Mariana a cámara + texto *"Data Analytics vs. Data Science"*. |
| 2. Comparación | 00:06-00:22 | **Data Analyst** → `grafico_analytics.png` (o la salida de `data_analytics.py` en la terminal: *"Limpieza: 60.900 → 58.519 filas"*, *"App +104 %, Web −9 %"*). **Data Scientist** → `grafico_prediccion.png` con la línea naranja hacia el futuro. |
| 3. ¿Por dónde arrancar? | 00:22-00:35 | Opcional de fondo: scroll de `ventas_tienda_online.xlsx` mostrando la suciedad (celdas vacías, " electronica", "MODA"). Refuerza "si no sabés limpiar, ningún modelo funciona". |
| 4. Bonus | 00:35-00:43 | Las 2 líneas de `bonus_reel.py` en pantalla → corte a `bonus.png`. |
| 5. Cierre + CTA | 00:43-00:52 | Mariana a cámara + texto flotante *"Comentá DATA"*. |

Las 2 líneas del bonus:

```python
df = pd.read_excel("ventas_limpias.xlsx")
df.groupby("Categoria")["Monto"].sum().sort_values().plot.barh()
```

## Caption

Data Analytics vs. Data Science: ¿Cuál es la diferencia real? 📊🐍

Todos los confunden, pero responden a necesidades muy distintas en el mercado. Mientras el Analytics limpia y explora información del presente para tomar decisiones de negocio hoy, la Ciencia de Datos construye modelos hacia el futuro.

Si querés dar tus primeros pasos en el mundo de los datos, dominar el análisis es la base sólida e indispensable para cualquier camino técnico.

📌 Guardá este post para consultarlo cuando tengas dudas sobre qué perfil elegir.

## Primer comentario (hashtags)

> Responder al primer comentario del post con los hashtags, NUNCA en la descripción.

#DataAnalytics #DataScience #Python #Programacion #AprenderAProgramar #Developer #DataAnalysis #Code #Pythonic
