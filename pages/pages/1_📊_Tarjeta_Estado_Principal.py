"""
Documentación: Tarjeta de Estado Principal
Explica cómo construir la tarjeta de alerta de flood desde las tablas SQL
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Tarjeta Estado Principal - Documentación",
    page_icon="",
    layout="wide"
)

st.title("Tarjeta de Estado Principal")
st.markdown("---")

# Mostrar el elemento visual tal como aparece en app.py
st.markdown("### Ejemplo Visual")
st.markdown("Así aparece la tarjeta de estado principal en el dashboard:")

# Crear datos de ejemplo
dates = pd.date_range(start='2025-01-01', periods=100, freq='30min')
df_ejemplo = pd.DataFrame({
    'timestamp': dates,
    'active_alarms': np.random.randint(100, 300, 100),
    'probabilidad_flood': np.random.uniform(0, 1, 100),
    'prediccion_flood': 0,
    'flood_actual': 0
})
df_ejemplo['prediccion_flood'] = (df_ejemplo['probabilidad_flood'] >= 0.6).astype(int)
df_ejemplo['flood_actual'] = (df_ejemplo['active_alarms'] >= 225).astype(int)
df_ejemplo['timestamp'] = pd.to_datetime(df_ejemplo['timestamp'])

# Obtener último estado
estado_ejemplo = df_ejemplo.iloc[-1].copy()
estado_ejemplo['prediccion_flood'] = 1 if estado_ejemplo['probabilidad_flood'] >= 0.6 else 0

# Mostrar tarjeta
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    if estado_ejemplo['prediccion_flood'] == 1:
        st.markdown("""
        <div style='background-color: #DC143C; color: white; padding: 2rem; border-radius: 12px; text-align: center;'>
            <h1 style='color: white; margin: 0; font-size: 3rem;'>ALERTA DE FLOOD</h1>
            <p style='font-size: 1.2rem; margin-top: 1rem;'>Se predice flood de alarmas en las próximas 2 horas</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='background-color: #3DCD58; color: white; padding: 2rem; border-radius: 12px; text-align: center;'>
            <h1 style='color: white; margin: 0; font-size: 3rem;'>ESTADO NORMAL</h1>
            <p style='font-size: 1.2rem; margin-top: 1rem;'>No se predice flood en las próximas 2 horas</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background-color: #FFFFFF; padding: 1.5rem; border-radius: 12px; border: 2px solid #E5E5E5; text-align: center;'>
        <div style='color: #333333; font-size: 0.9rem; margin-bottom: 0.5rem;'>PROBABILIDAD DE FLOOD</div>
        <div style='color: #2E9A42; font-size: 3rem; font-weight: 700;'>{:.1f}%</div>
        <div style='color: #666666; font-size: 0.8rem; margin-top: 0.5rem;'>Próximas 2 horas</div>
    </div>
    """.format(estado_ejemplo['probabilidad_flood'] * 100), unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='background-color: #FFFFFF; padding: 1.5rem; border-radius: 12px; border: 2px solid #E5E5E5; text-align: center;'>
        <div style='color: #333333; font-size: 0.9rem; margin-bottom: 0.5rem;'>ALARMAS ACTIVAS</div>
        <div style='color: #2E9A42; font-size: 3rem; font-weight: 700;'>{}</div>
        <div style='color: #666666; font-size: 0.8rem; margin-top: 0.5rem;'>En este momento</div>
    </div>
    """.format(int(estado_ejemplo['active_alarms'])), unsafe_allow_html=True)

st.markdown("---")

st.markdown("""
## Descripción de la Visualización

La **Tarjeta de Estado Principal** es el elemento más prominente del dashboard. Muestra una alerta grande 
que indica si el sistema predice un flood de alarmas o si está en estado normal.

### Características Visuales:
- Estado ALERTA: Indicador visual de alerta
- Estado NORMAL: Indicador visual de normalidad
- Tamaño grande y centrado para máxima visibilidad
- Mensaje descriptivo del estado
""")

st.markdown("---")

st.markdown("## Datos Necesarios")

st.markdown("""
### Tabla: `ypf_flood_alarms`

Esta tabla contiene las predicciones del modelo de Machine Learning.

**Columnas relevantes:**
- `timestamp` (DATETIME) - Fecha y hora de la predicción
- `prediccion_flood` (INT) - 0 = No flood, 1 = Flood
- `probabilidad_flood` (FLOAT) - Probabilidad entre 0.0 y 1.0
- `estado_alerta` (VARCHAR) - 'NORMAL' o 'ALERTA'
- `fecha_prediccion` (DATETIME) - Cuándo se guardó la predicción
""")

st.markdown("---")

st.markdown("## Consulta SQL")

st.code("""
-- Obtener el estado más reciente del sistema
SELECT TOP 1
    timestamp,
    prediccion_flood,
    probabilidad_flood,
    estado_alerta,
    active_actual,
    fecha_prediccion
FROM dbo.ypf_flood_alarms
ORDER BY fecha_prediccion DESC
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
       │ Consulta SQL
       │ (último registro)
       ▼
┌─────────────┐
│   Backend   │
│   (API)     │
└──────┬──────┘
       │
       │ JSON Response
       │ {
       │   prediccion_flood: 1,
       │   estado_alerta: "ALERTA",
       │   probabilidad_flood: 0.85
       │ }
       ▼
┌─────────────┐
│  Frontend   │
│  Component  │
└─────────────┘
       │
       │ Renderizado
       │ Condicional
       ▼
┌─────────────┐
│   Tarjeta   │
│   Visual    │
└─────────────┘
""")

st.markdown("---")

st.markdown("## Consideraciones Importantes")

st.markdown("""
1. **Performance**: Cachear el resultado en el frontend para evitar llamadas excesivas
2. **Fallback**: Si no hay datos, mostrar un estado "Sin datos disponibles"
3. **Transiciones**: Usar animaciones suaves al cambiar de estado (fade in/out)
4. **Accesibilidad**: Asegurar contraste adecuado y texto legible
5. **Testing**: Probar ambos estados (ALERTA y NORMAL) con datos reales
""")

