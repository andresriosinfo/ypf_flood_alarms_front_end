"""
Documentación: Gráfico de Tendencias
Explica cómo construir el gráfico de tendencias desde las tablas SQL
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Gráfico Tendencias - Documentación",
    page_icon="",
    layout="wide"
)

st.title("Gráfico de Tendencias")
st.markdown("---")

# Mostrar el elemento visual tal como aparece en app.py
st.markdown("### Ejemplo Visual")
st.markdown("Así aparece el gráfico de tendencias en el dashboard:")

# Crear datos de ejemplo
dates = pd.date_range(start='2025-01-15', periods=48, freq='30min')
df_ejemplo = pd.DataFrame({
    'timestamp': dates,
    'active_alarms': np.random.randint(150, 280, 48),
    'probabilidad_flood': np.random.uniform(0.3, 0.8, 48),
})
df_ejemplo['timestamp'] = pd.to_datetime(df_ejemplo['timestamp'])

# Crear gráfico
flood_threshold = 225
df_recent = df_ejemplo.copy()

fig = go.Figure()

# Línea de alarmas activas
fig.add_trace(go.Scatter(
    x=df_recent['timestamp'],
    y=df_recent['active_alarms'],
    mode='lines',
    name='Alarmas Activas',
    line=dict(color='#3DCD58', width=3),
    fill='tozeroy',
    fillcolor='rgba(61, 205, 88, 0.1)',
    hovertemplate='%{x}<br>Alarmas: %{y}<extra></extra>'
))

# Umbral de flood
fig.add_hline(
    y=flood_threshold,
    line_dash="dash",
    line_color="#DC143C",
    line_width=2,
    annotation_text=f"Umbral: {flood_threshold}",
    annotation_position="right"
)

# Probabilidad de flood (eje secundario)
fig.add_trace(go.Scatter(
    x=df_recent['timestamp'],
    y=df_recent['probabilidad_flood'] * 100,
    mode='lines',
    name='Probabilidad Flood (%)',
    line=dict(color='#2E9A42', width=2, dash='dot'),
    yaxis='y2',
    hovertemplate='%{x}<br>Probabilidad: %{y:.1f}%<extra></extra>'
))

fig.update_layout(
    xaxis_title='Tiempo',
    yaxis_title='Alarmas Activas',
    yaxis2=dict(
        title='Probabilidad Flood (%)',
        overlaying='y',
        side='right',
        range=[0, 100]
    ),
    hovermode='x unified',
    template='plotly_white',
    height=400,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    margin=dict(l=50, r=50, t=20, b=50),
    plot_bgcolor='#FFFFFF',
    paper_bgcolor='#FFFFFF'
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.markdown("""
## Descripción de la Visualización

El **Gráfico de Tendencias** muestra la evolución temporal de:
- **Alarmas Activas**: Línea con área sombreada
- **Umbral de Flood**: Línea horizontal punteada
- **Probabilidad de Flood**: Línea punteada en eje secundario (derecha)

### Características Visuales:
- Gráfico de líneas interactivo
- Dos ejes Y (alarmas a la izquierda, probabilidad % a la derecha)
- Tooltips al pasar el mouse
- Zoom y pan habilitados
- Responsive
""")

st.markdown("---")

st.markdown("## Datos Necesarios")

st.markdown("""
### Tabla: `ypf_flood_alarms`

**Columnas relevantes:**
- `timestamp` (DATETIME) - Fecha y hora de cada punto
- `active_actual` (INT) - Número de alarmas activas
- `probabilidad_flood` (FLOAT) - Probabilidad (0.0 a 1.0)
- `fecha_prediccion` (DATETIME) - Para filtrar por fecha

**Parámetros del usuario:**
- `horas_visualizar` - Número de horas a mostrar (6, 12, 24, 48)
- `flood_threshold` - Umbral de alarmas para considerar flood
""")

st.markdown("---")

st.markdown("## Consultas SQL")

st.markdown("### Consulta Principal para el Gráfico")

st.code("""
-- Obtener datos de las últimas N horas
DECLARE @horas INT = 24;  -- Parámetro del usuario

SELECT 
    timestamp,
    active_actual,
    probabilidad_flood,
    prediccion_flood
FROM dbo.ypf_flood_alarms
WHERE fecha_prediccion >= DATEADD(HOUR, -@horas, GETDATE())
ORDER BY timestamp ASC
""", language="sql")

st.markdown("### Consulta con Filtro de Fecha Específica")

st.code("""
-- Obtener datos desde una fecha específica
SELECT 
    timestamp,
    active_actual,
    probabilidad_flood,
    prediccion_flood
FROM dbo.ypf_flood_alarms
WHERE timestamp >= DATEADD(HOUR, -24, GETDATE())
  AND timestamp <= GETDATE()
ORDER BY timestamp ASC
""", language="sql")

st.markdown("### Consulta para Obtener Umbral (si está en la tabla)")

st.code("""
-- Si el umbral está almacenado en cada registro
SELECT TOP 1
    umbral_flood
FROM dbo.ypf_flood_alarms
WHERE umbral_flood IS NOT NULL
ORDER BY fecha_prediccion DESC

-- O usar un valor fijo configurado en el frontend
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
       │ SELECT timestamp, active_actual, probabilidad_flood
       │ WHERE fecha_prediccion >= DATEADD(HOUR, -24, GETDATE())
       │ ORDER BY timestamp
       ▼
┌─────────────┐
│   Backend   │
│   (API)     │
└──────┬──────┘
       │
       │ JSON Array con puntos de datos
       │ [{timestamp, active_actual, probabilidad_flood}, ...]
       ▼
┌─────────────┐
│  Frontend   │
│  Component  │
└─────────────┘
       │
       │ Transformación y Configuración
       │ - Convertir timestamps
       │ - Convertir probabilidad a %
       │ - Configurar series
       ▼
┌─────────────┐
│  Librería   │
│  Gráficos   │
│ (Plotly.js) │
└─────────────┘
       │
       │ Renderizado
       ▼
┌─────────────┐
│   Gráfico    │
│  Interactivo │
└─────────────┘
""")

st.markdown("---")

st.markdown("## Consideraciones Importantes")

st.markdown("""
1. **Performance con Muchos Datos**: 
   - Si hay más de 1000 puntos, considerar agregación o muestreo
   - Usar virtualización o paginación

2. **Formato de Fechas**: 
   - Asegurar que las fechas se parseen correctamente
   - Considerar zona horaria del servidor vs cliente

3. **Actualización en Tiempo Real**: 
   - Agregar nuevos puntos sin recargar todo el gráfico
   - Usar animaciones suaves para nuevos datos

4. **Manejo de Datos Faltantes**: 
   - Mostrar gaps o interpolar según corresponda
   - No conectar puntos si hay saltos grandes de tiempo

5. **Accesibilidad**: 
   - Asegurar que los colores sean distinguibles
   - Agregar texto alternativo para lectores de pantalla
   - Hacer el gráfico navegable con teclado
""")
