"""
Documentación: Matriz de Confusión
Explica cómo construir la matriz de confusión desde las tablas SQL
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Matriz Confusión - Documentación",
    page_icon="",
    layout="wide"
)

st.title("Matriz de Confusión")
st.markdown("---")

# Mostrar el elemento visual tal como aparece en app.py
st.markdown("### Ejemplo Visual")
st.markdown("Así aparece la matriz de confusión en el dashboard:")

# Crear datos de ejemplo para calcular matriz
dates = pd.date_range(start='2025-01-01', periods=100, freq='30min')
df_ejemplo = pd.DataFrame({
    'timestamp': dates,
    'active_alarms': np.random.randint(100, 300, 100),
    'probabilidad_flood': np.random.uniform(0, 1, 100),
})
df_ejemplo['prediccion_flood'] = (df_ejemplo['probabilidad_flood'] >= 0.6).astype(int)
df_ejemplo['flood_actual'] = (df_ejemplo['active_alarms'] >= 225).astype(int)

# Calcular valores de la matriz
tp = ((df_ejemplo['prediccion_flood'] == 1) & (df_ejemplo['flood_actual'] == 1)).sum()
tn = ((df_ejemplo['prediccion_flood'] == 0) & (df_ejemplo['flood_actual'] == 0)).sum()
fp = ((df_ejemplo['prediccion_flood'] == 1) & (df_ejemplo['flood_actual'] == 0)).sum()
fn = ((df_ejemplo['prediccion_flood'] == 0) & (df_ejemplo['flood_actual'] == 1)).sum()

# Mostrar matriz
st.markdown("### Matriz de Confusión")
st.markdown(f"""
<table style='width: 100%; border-collapse: collapse;'>
    <tr style='background-color: #2E9A42; color: white;'>
        <th style='padding: 0.5rem;'></th>
        <th style='padding: 0.5rem;'>Pred No Flood</th>
        <th style='padding: 0.5rem;'>Pred Flood</th>
    </tr>
    <tr>
        <td style='background-color: #F5F5F5; font-weight: 600; padding: 0.5rem;'>Real No Flood</td>
        <td style='padding: 0.5rem; text-align: center;'>{tn:,}</td>
        <td style='padding: 0.5rem; text-align: center; color: #DC143C;'>{fp:,}</td>
    </tr>
    <tr>
        <td style='background-color: #F5F5F5; font-weight: 600; padding: 0.5rem;'>Real Flood</td>
        <td style='padding: 0.5rem; text-align: center; color: #DC143C;'>{fn:,}</td>
        <td style='padding: 0.5rem; text-align: center; color: #2E9A42; font-weight: 600;'>{tp:,}</td>
    </tr>
</table>
""", unsafe_allow_html=True)

st.markdown("---")

st.markdown("""
## Descripción de la Visualización

La **Matriz de Confusión** es una tabla que muestra:
- **True Positives (TP)**: Predijo flood y hubo flood (correcto)
- **True Negatives (TN)**: Predijo no flood y no hubo flood (correcto)
- **False Positives (FP)**: Predijo flood pero no hubo flood (falso positivo)
- **False Negatives (FN)**: Predijo no flood pero hubo flood (falso negativo)

### Características Visuales:
- Tabla 2x2 con etiquetas claras
- Valores numéricos grandes y legibles
- Encabezados descriptivos
""")

st.markdown("---")

st.markdown("## Datos Necesarios")

st.markdown("""
### Tabla: `ypf_flood_alarms`

**Columnas relevantes:**
- `prediccion_flood` (INT) - Predicción del modelo (0 o 1)
- `active_actual` (INT) - Número de alarmas activas
- `umbral_flood` (INT) - Umbral usado para definir flood real
- `probabilidad_flood` (FLOAT) - Para recalcular predicción si es necesario
- `timestamp` (DATETIME) - Para filtrar por período

**Cálculo de Flood Real:**
- Si `active_actual >= umbral_flood` → Flood Real = 1
- Si `active_actual < umbral_flood` → Flood Real = 0
""")

st.markdown("---")

st.markdown("## Consultas SQL")

st.markdown("### Consulta para Obtener Valores de la Matriz")

st.code("""
-- Calcular valores de la matriz de confusión
DECLARE @umbral_flood INT = 225;
DECLARE @umbral_decision FLOAT = 0.6;
DECLARE @dias INT = 30;

WITH datos_evaluacion AS (
    SELECT 
        -- Flood real basado en umbral
        CASE 
            WHEN active_actual >= @umbral_flood THEN 1 
            ELSE 0 
        END AS flood_real,
        -- Predicción basada en umbral de decisión
        CASE 
            WHEN probabilidad_flood >= @umbral_decision THEN 1 
            ELSE 0 
        END AS prediccion_flood
    FROM dbo.ypf_flood_alarms
    WHERE fecha_prediccion >= DATEADD(DAY, -@dias, GETDATE())
)
SELECT 
    -- True Negatives: Pred No Flood, Real No Flood
    SUM(CASE WHEN prediccion_flood = 0 AND flood_real = 0 THEN 1 ELSE 0 END) AS true_negatives,
    -- False Positives: Pred Flood, Real No Flood
    SUM(CASE WHEN prediccion_flood = 1 AND flood_real = 0 THEN 1 ELSE 0 END) AS false_positives,
    -- False Negatives: Pred No Flood, Real Flood
    SUM(CASE WHEN prediccion_flood = 0 AND flood_real = 1 THEN 1 ELSE 0 END) AS false_negatives,
    -- True Positives: Pred Flood, Real Flood
    SUM(CASE WHEN prediccion_flood = 1 AND flood_real = 1 THEN 1 ELSE 0 END) AS true_positives,
    COUNT(*) AS total
FROM datos_evaluacion
""", language="sql")

st.markdown("### Consulta con Porcentajes (Opcional)")

st.code("""
-- Incluir porcentajes en la consulta
WITH matriz AS (
    -- Misma consulta anterior
    SELECT 
        SUM(CASE WHEN prediccion_flood = 0 AND flood_real = 0 THEN 1 ELSE 0 END) AS tn,
        SUM(CASE WHEN prediccion_flood = 1 AND flood_real = 0 THEN 1 ELSE 0 END) AS fp,
        SUM(CASE WHEN prediccion_flood = 0 AND flood_real = 1 THEN 1 ELSE 0 END) AS fn,
        SUM(CASE WHEN prediccion_flood = 1 AND flood_real = 1 THEN 1 ELSE 0 END) AS tp,
        COUNT(*) AS total
    FROM ...
)
SELECT 
    tn,
    fp,
    fn,
    tp,
    total,
    CAST(tn AS FLOAT) / total * 100 AS tn_pct,
    CAST(fp AS FLOAT) / total * 100 AS fp_pct,
    CAST(fn AS FLOAT) / total * 100 AS fn_pct,
    CAST(tp AS FLOAT) / total * 100 AS tp_pct
FROM matriz
""", language="sql")

st.markdown("---")

st.markdown("## Flujo de Datos")

st.markdown("""
```
┌─────────────┐
│  SQL Server │
│ ypf_flood_  │
│   alarms    │
└──────┬──────┘
       │
       │ Calcular TN, FP, FN, TP
       │ con CASE statements
       ▼
┌─────────────┐
│   Backend   │
│   (API)     │
└──────┬──────┘
       │
       │ JSON: {
       │   true_negatives: 120,
       │   false_positives: 12,
       │   false_negatives: 10,
       │   true_positives: 45
       │ }
       ▼
┌─────────────┐
│  Frontend   │
│  Component  │
└─────────────┘
       │
       │ Construir tabla HTML
       │ Aplicar estilos
       ▼
┌─────────────┐
│    Tabla    │
│  Matriz de  │
│  Confusión  │
└─────────────┘
""")

st.markdown("---")

st.markdown("## Interpretación de la Matriz")

st.markdown("""
### ¿Qué significa cada celda?

**True Negatives (TN) - Esquina superior izquierda:**
- El modelo predijo "No Flood" y efectivamente no hubo flood
- **Correcto** - El modelo acertó

**False Positives (FP) - Esquina superior derecha:**
- El modelo predijo "Flood" pero no hubo flood
- **Falso Alarma** - El modelo fue demasiado cauteloso

**False Negatives (FN) - Esquina inferior izquierda:**
- El modelo predijo "No Flood" pero sí hubo flood
- **Error Crítico** - El modelo no detectó un flood real

**True Positives (TP) - Esquina inferior derecha:**
- El modelo predijo "Flood" y efectivamente hubo flood
- **Correcto** - El modelo detectó el flood correctamente

### Objetivo del Modelo

- **Maximizar TP**: Detectar todos los floods reales
- **Minimizar FN**: Evitar no detectar floods (más crítico)
- **Minimizar FP**: Reducir falsas alarmas (menos crítico pero importante)
- **Maximizar TN**: Correctamente identificar cuando no hay flood
""")

st.markdown("---")

st.markdown("## Consideraciones Importantes")

st.markdown("""
1. **Consistencia de Umbrales**: Asegurar que los umbrales usados en SQL sean los mismos que en el frontend
2. **Período de Evaluación**: Permitir al usuario seleccionar el período a evaluar
3. **Formato de Números**: Usar separadores de miles para números grandes
4. **Colores Accesibles**: Asegurar que los colores sean distinguibles para personas con daltonismo
5. **Tooltips**: Considerar agregar tooltips explicativos al pasar el mouse sobre cada celda
6. **Exportación**: Permitir exportar la matriz como imagen o CSV
""")

