# Reel: Excel vs Python con grandes volúmenes de datos

## Archivos

| Archivo | Qué es |
|---|---|
| `ventas_2025.xlsx` | El Excel "pesado": 100.000 ventas + catálogo + hoja **Resumen** con `SUMIFS` sobre toda la tabla (la parte que tilda el Excel). |
| `automatizar_reporte.py` | El mismo resumen en Python: lee, limpia, cruza con el catálogo (el BUSCARV) y genera `reporte_ventas.xlsx` con formato y gráfico. ~4 s. |
| `reporte_ventas.xlsx` | Resultado del script: KPIs, ventas por sucursal y mes, top 10 productos, medios de pago y gráfico. |
| `generar_excel.py` | Regenera `ventas_2025.xlsx`. `python generar_excel.py 300000` para que se tilde todavía más. |

```bash
pip install -r requirements.txt
python automatizar_reporte.py              # un archivo
python automatizar_reporte.py carpeta/     # todos los .xlsx de una carpeta (la automatización)
```

## Guion sugerido (≈30 s)

1. **Hook (0-3 s):** abrir `ventas_2025.xlsx`, ir a la hoja Resumen → Excel "No responde".
   Texto en pantalla: *"Cuando tu Excel tiene 100.000 filas…"*
2. **Problema (3-8 s):** scroll por la hoja Ventas; mostrar las fórmulas `SUMIFS` de Resumen.
3. **Cambio (8-18 s):** terminal → `python automatizar_reporte.py` → aparece
   *"100.000 filas procesadas en 3.7 s"*.
4. **Resultado (18-25 s):** abrir `reporte_ventas.xlsx` con el gráfico y el top de productos.
5. **Automatización (25-30 s):** `python automatizar_reporte.py carpeta/` procesando varios meses de una.
   Texto: *"Y el mes que viene, lo mismo con un comando."*

## Caption

Cuando pasás de 'hacer que funcione' a manipular grandes volúmenes de datos, te das cuenta de que las planillas tradicionales tienen un techo. Python no solo te ahorra horas de espera, sino que te permite automatizar procesos para no volver a repetir el mismo trabajo dos veces.

📌 Guardá este post para la próxima vez que se te tilde el Excel.

## Primer comentario (hashtags)

#python #excel #pandas #automatizacion #analisisdedatos #datos #programacion #aprendeprogramacion #productividad #dev
