"""
Documentación: Métricas del Modelo
Explica cómo calcular y mostrar las métricas del modelo desde las tablas SQL
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Métricas Modelo - Documentación",
    page_icon="",
    layout="wide"
)

st.title("Métricas del Modelo")
st.markdown("---")

# Mostrar el elemento visual tal como aparece en app.py
st.markdown("### Ejemplo Visual")
st.markdown("Así aparecen las métricas del modelo en el dashboard:")

# Crear datos de ejemplo para calcular métricas
dates = pd.date_range(start='2025-01-01', periods=100, freq='30min')
df_ejemplo = pd.DataFrame({
    'timestamp': dates,
    'active_alarms': np.random.randint(100, 300, 100),
    'probabilidad_flood': np.random.uniform(0, 1, 100),
})
df_ejemplo['prediccion_flood'] = (df_ejemplo['probabilidad_flood'] >= 0.6).astype(int)
df_ejemplo['flood_actual'] = (df_ejemplo['active_alarms'] >= 225).astype(int)

# Calcular métricas
tp = ((df_ejemplo['prediccion_flood'] == 1) & (df_ejemplo['flood_actual'] == 1)).sum()
tn = ((df_ejemplo['prediccion_flood'] == 0) & (df_ejemplo['flood_actual'] == 0)).sum()
fp = ((df_ejemplo['prediccion_flood'] == 1) & (df_ejemplo['flood_actual'] == 0)).sum()
fn = ((df_ejemplo['prediccion_flood'] == 0) & (df_ejemplo['flood_actual'] == 1)).sum()

total = len(df_ejemplo)
accuracy = (tp + tn) / total if total > 0 else 0
precision = tp / (tp + fp) if (tp + fp) > 0 else 0
recall = tp / (tp + fn) if (tp + fn) > 0 else 0
f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

# Mostrar métricas
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Métricas del Modelo")
    st.metric("Accuracy", f"{accuracy:.2%}")
    st.metric("Precision", f"{precision:.2%}")
    st.metric("Recall", f"{recall:.2%}")
    st.metric("F1-Score", f"{f1:.2%}")

st.markdown("---")

st.markdown("""
## Descripción de la Visualización

Las **Métricas del Modelo** muestran el rendimiento del modelo de Machine Learning en términos de:
- **Accuracy** (Precisión General)
- **Precision** (Precisión)
- **Recall** (Sensibilidad)
- **F1-Score** (Puntuación F1)

Estas métricas se calculan comparando las predicciones del modelo con los valores reales de flood.

### Características Visuales:
- Tarjetas o métricas individuales
- Valores en formato porcentual
- Fácil de leer y comparar
""")

st.markdown("---")

st.markdown("## Datos Necesarios")

st.markdown("""
### Tabla: `ypf_flood_alarms`

**Columnas relevantes:**
- `prediccion_flood` (INT) - Predicción del modelo (0 o 1)
- `probabilidad_flood` (FLOAT) - Probabilidad usada para la predicción
- `active_actual` (INT) - Número de alarmas activas (para calcular flood real)
- `umbral_flood` (INT) - Umbral usado para definir flood real
- `timestamp` (DATETIME) - Para filtrar por período

**Nota**: El "flood real" se calcula comparando `active_actual` con `umbral_flood`:
- Si `active_actual >= umbral_flood` → Flood Real = 1
- Si `active_actual < umbral_flood` → Flood Real = 0
""")

st.markdown("---")

st.markdown("## Consultas SQL")

st.markdown("### Consulta para Calcular Métricas")

st.code("""
-- Calcular métricas del modelo en un período específico
DECLARE @umbral_flood INT = 225;  -- Umbral configurado
DECLARE @umbral_decision FLOAT = 0.6;  -- Umbral de probabilidad
DECLARE @dias INT = 30;  -- Período a evaluar

WITH datos_con_flood_real AS (
    SELECT 
        timestamp,
        active_actual,
        probabilidad_flood,
        prediccion_flood,
        -- Calcular flood real basado en umbral
        CASE 
            WHEN active_actual >= @umbral_flood THEN 1 
            ELSE 0 
        END AS flood_real,
        -- Recalcular predicción basada en umbral de decisión
        CASE 
            WHEN probabilidad_flood >= @umbral_decision THEN 1 
            ELSE 0 
        END AS prediccion_recalculada
    FROM dbo.ypf_flood_alarms
    WHERE fecha_prediccion >= DATEADD(DAY, -@dias, GETDATE())
)
SELECT 
    -- True Positives: Predijo flood y hubo flood
    SUM(CASE WHEN prediccion_recalculada = 1 AND flood_real = 1 THEN 1 ELSE 0 END) AS true_positives,
    -- True Negatives: Predijo no flood y no hubo flood
    SUM(CASE WHEN prediccion_recalculada = 0 AND flood_real = 0 THEN 1 ELSE 0 END) AS true_negatives,
    -- False Positives: Predijo flood pero no hubo flood
    SUM(CASE WHEN prediccion_recalculada = 1 AND flood_real = 0 THEN 1 ELSE 0 END) AS false_positives,
    -- False Negatives: Predijo no flood pero hubo flood
    SUM(CASE WHEN prediccion_recalculada = 0 AND flood_real = 1 THEN 1 ELSE 0 END) AS false_negatives,
    COUNT(*) AS total_registros
FROM datos_con_flood_real
""", language="sql")

st.markdown("### Consulta Simplificada (si ya tienes flood_real calculado)")

st.code("""
-- Si ya tienes una columna flood_real en la tabla
SELECT 
    SUM(CASE WHEN prediccion_flood = 1 AND flood_real = 1 THEN 1 ELSE 0 END) AS tp,
    SUM(CASE WHEN prediccion_flood = 0 AND flood_real = 0 THEN 1 ELSE 0 END) AS tn,
    SUM(CASE WHEN prediccion_flood = 1 AND flood_real = 0 THEN 1 ELSE 0 END) AS fp,
    SUM(CASE WHEN prediccion_flood = 0 AND flood_real = 1 THEN 1 ELSE 0 END) AS fn,
    COUNT(*) AS total
FROM dbo.ypf_flood_alarms
WHERE fecha_prediccion >= DATEADD(DAY, -30, GETDATE())
""", language="sql")

st.markdown("---")

st.markdown("## Cálculo de Métricas")

st.markdown("""
### Fórmulas

Una vez obtenidos los valores de TP, TN, FP, FN desde SQL:

**Accuracy (Precisión General):**
```
Accuracy = (TP + TN) / (TP + TN + FP + FN)
```

**Precision (Precisión):**
```
Precision = TP / (TP + FP)
```
*Nota: Si TP + FP = 0, Precision = 0*

**Recall (Sensibilidad):**
```
Recall = TP / (TP + FN)
```
*Nota: Si TP + FN = 0, Recall = 0*

**F1-Score:**
```
F1-Score = 2 * (Precision * Recall) / (Precision + Recall)
```
*Nota: Si Precision + Recall = 0, F1-Score = 0*

### Interpretación

- **Accuracy**: Porcentaje de predicciones correctas (0-100%)
- **Precision**: De todas las predicciones de flood, cuántas fueron correctas
- **Recall**: De todos los floods reales, cuántos fueron detectados
- **F1-Score**: Media armónica de Precision y Recall (balance entre ambos)
""")

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
       │ Calcular TP, TN, FP, FN
       │ con CASE statements
       ▼
┌─────────────┐
│   Backend   │
│   (API)     │
└──────┬──────┘
       │
       │ Calcular métricas
       │ (Accuracy, Precision, etc.)
       │
       │ JSON: {
       │   accuracy: 0.85,
       │   precision: 0.78,
       │   ...
       │ }
       ▼
┌─────────────┐
│  Frontend   │
│  Component  │
└─────────────┘
       │
       │ Formateo a porcentaje
       │ y renderizado
       ▼
┌─────────────┐
│   Tarjetas  │
│  de Métricas│
└─────────────┘
""")

st.markdown("---")

st.markdown("## Consideraciones Importantes")

st.markdown("""
1. **División por Cero**: Siempre validar que los denominadores no sean cero antes de calcular
2. **Período de Evaluación**: Permitir al usuario seleccionar el período (7, 30, 90 días)
3. **Umbrales**: Los umbrales deben ser configurables y consistentes
4. **Performance**: Si hay muchos datos, considerar calcular métricas en el backend y cachearlas
5. **Contexto**: Mostrar el número total de muestras evaluadas
6. **Tendencias**: Considerar mostrar cómo han cambiado las métricas en el tiempo
""")

